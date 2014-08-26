import os
import sys
from argparse import ArgumentParser
from json import load
from workflow import Workflow, MATCH_ALL, MATCH_ALLCHARS
from workflow.background import run_in_background, is_running
from commons import run_alfred, send_notification, actions

logger = None
VAGRANT_DEFAULT_INDEX = '~/.vagrant.d/data/machine-index/index'
ICONS_STATES_PATH = 'icons/states'
ICONS_ACTION_PATH = 'icons/actions'

#todo: rdp & ssh commands
#todo:
#todo: convert all paths to absolute
#todo: open terminal in vagrantfile dir
#todo: handle vagrant bug with global-status and suspend


def _get_index_data():
    try:
        index_path = os.path.join(os.environ['VAGRANT_HOME'],
                                  'data/machine-index/index')
    except KeyError:
        index_path = VAGRANT_DEFAULT_INDEX
    return _read_index(index_path)


def _read_index(path):
    try:
        with open(os.path.expanduser(path)) as index:
            return load(index)
    except IOError:
        raise Exception('Index file {} not found!'.format(path))
    except ValueError:
        raise Exception('Index file {} is corrupted!'.format(path))


def _get_state_icon(state, provider):
    """
    Return appropriate icon path for state
    """
    norm_state = _normalize_state(state)
    icon = '{}/{}.{}.png'.format(ICONS_STATES_PATH, provider, norm_state)
    if not os.path.isfile(icon):
        icon = '{}/{}.{}.png'.format(ICONS_STATES_PATH, 'vagrant', norm_state)
        if not os.path.isfile(icon):
            icon = None

    return icon


def _get_action_icon(action):
    """
    Return icon path for action
    """
    icon = '{}/{}.png'.format(ICONS_ACTION_PATH, action)
    if not os.path.isfile(icon):
        icon = None
    return icon


def _normalize_state(state):
    """
    (try to) normalize provider states
    """
    if state in ('running', 'up', 'on'):
        out = 'running'
    elif state in ('paused', 'suspended', 'saved'):
        out = 'paused'
    elif state in ('stopped', 'poweroff', 'not running', 'down'):
        out = 'stopped'
    elif state in 'not created':
        out = 'missing'
    else:
        out = 'unexpected'

    #logger.debug('normalized state. in: {}, out: {}'.format(state, out))
    return out


def _get_search_key(machine):
    """
    Return search key to be used by Workflow.filter
    """
    fields = [machine['name'],
              machine['vagrantfile_path'],
              machine['provider']]
    return ' '.join(fields)


def _list_machines(machines, wf):
    subtitles_dict = {'cmd': 'Run commands on whole environment'}

    for item in machines:
        wf.add_item(title=item['name'],
                    subtitle=item['vagrantfile_path'],
                    modifier_subtitles=subtitles_dict,
                    arg=item['id'],
                    uid=item['id'],
                    valid=True,
                    icon=_get_state_icon(item['state'], item['provider']))


def _list_machine_actions(mid, data, wf):
    try:
        for action, info in actions.iteritems():
            norm_state = _normalize_state(data['machines'][mid]['state'])
            if norm_state in info['state']:
                wf.add_item(title=action,
                            subtitle=info['desc'],
                            uid=action,
                            arg='{} {!r}'.format(
                                mid, ' '.join([action, info['flags'] or ''])),
                            icon=_get_action_icon(action),
                            valid=True)
    except KeyError:
        raise Exception('Machine doesn\'t exists')


def _list_dir_actions(path, wf):
    for action, info in actions.iteritems():
        if info['directory']:
            wf.add_item(title=action,
                        subtitle=info['desc'],
                        uid=action,
                        arg='{} {!r}'.format(
                            path, ' '.join([action, info['flags'] or ''])),
                        icon=_get_action_icon(action),
                        valid=True)


def _validate_version(version):
    if version != 1:
        raise Exception('Unsupported Vagrant index version')


def _rearrange_data(data):
    """Returns a list of machines dicts with machine's key as an id field"""
    machines_dict = data['machines']
    result_list = []
    for key, val in machines_dict.iteritems():
        new_val = val.copy()
        new_val.update({'id': key})
        result_list.append(new_val)
    return result_list


def main(wf):
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list',
                       nargs='?',
                       const='',
                       metavar='FILTER',
                       help='List Vagrant environments. '
                            'If %(metavar)s is provided, will filter results '
                            'by fuzzy searching')
    group.add_argument('--set',
                       metavar='MACHINE_ID',
                       help='Store %(metavar)s to be retrived later')
    group.add_argument('--setenv',
                       metavar='ENV_PATH',
                       help='Store %(metavar)s to be retrived later as env dir')
    group.add_argument('--get',
                       action='store_true',
                       help='Get value which was previously stored')
    group.add_argument('--execute',
                       nargs=2,
                       metavar=('ID', 'COMMAND'),
                       help='Execute command on specific VM or entire'
                            ' environment in the background')
    args = parser.parse_args(wf.args)
    # logger.debug('args: {}'.format(args))

    raw_data = _get_index_data()
    # logger.debug('raw data: {}'.format(raw_data))

    _validate_version(raw_data['version'])
    modified_data = _rearrange_data(raw_data)
    # logger.debug('modified data: {}'.format(modified_data))

    if args.list is not None:
        # logger.debug('listing vagrant boxes')
        if args.list:
            modified_data = wf.filter(args.list, modified_data,
                                      _get_search_key,
                                      match_on=MATCH_ALL ^ MATCH_ALLCHARS)
            # logger.debug('filtered data: {}'.format(modified_data))
        _list_machines(modified_data, wf)
    elif args.set:
        logger.debug('saving id: {}'.format(args.set))
        wf.settings['id'] = args.set
        run_alfred(':vagrant-id')
    elif args.setenv:
        vagrant_dir = raw_data['machines'][args.setenv]['vagrantfile_path']
        logger.debug('saving id: {}'.format(vagrant_dir))
        wf.settings['id'] = vagrant_dir
        run_alfred(':vagrant-id')
    elif args.get:
        mid = wf.settings.get('id')
        logger.debug('retrieved id: {}'.format(mid))
        if os.path.isdir(mid):
            _list_dir_actions(mid, wf)
        else:
            _list_machine_actions(mid, raw_data, wf)
    elif args.execute:
        vpath = args.execute[0]
        if not os.path.isdir(vpath):
            vpath = raw_data['machines'][args.execute[0]]['vagrantfile_path']

        task_name = 'exec_{}'.format(hash(vpath))
        cmd = ['/usr/bin/python', 'execute.py'] + args.execute
        if not is_running(task_name):
            run_in_background(task_name, cmd)
        else:
            send_notification('Task in progress. \nAborting')

    wf.send_feedback()


if __name__ == '__main__':
    workflow = Workflow()
    logger = workflow.logger
    sys.exit(workflow.run(main))
