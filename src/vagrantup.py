import os
import sys
from argparse import ArgumentParser
from json import load
from workflow import Workflow, MATCH_ALL, MATCH_ALLCHARS
from workflow.background import run_in_background, is_running
from commons import run_alfred, send_notification, actions, states

logger = None
VAGRANT_HOME = os.path.expanduser('~/.vagrant.d')
VAGRANT_INDEX = os.path.join('data', 'machine-index', 'index')
ICONS_STATES_PATH = os.path.join(Workflow().workflowdir, 'icons', 'states')
ICONS_ACTION_PATH = os.path.join(Workflow().workflowdir, 'icons', 'actions')


def get_machine_data():
    vagrant_home = os.environ.get('VAGRANT_HOME', VAGRANT_HOME)
    index_path = os.path.join(vagrant_home, VAGRANT_INDEX)
    with open(index_path) as index:
        data = load(index)
    validate_version(data['version'])
    return data['machines']


def get_state_icon(state, provider):
    """
    Return appropriate icon path for state
    """
    norm_state = normalize_state(state)
    icon = os.path.join(ICONS_STATES_PATH,
                        '{0}.{1}.png'.format(provider, norm_state))
    default = os.path.join(ICONS_STATES_PATH,
                           'vagrant.{0}.png'.format(norm_state))

    if os.path.isfile(icon):
        return icon
    elif os.path.isfile(default):
        return default
    else:
        return None


def get_action_icon(action):
    """
    Return icon path for action
    """
    icon = os.path.join(ICONS_ACTION_PATH, '{0}.png'.format(action))
    if os.path.isfile(icon):
        return icon
    else:
        return None


def normalize_state(state):
    """
    Normalize environment state
    """
    for states_tup, output in states.iteritems():
        if state in states_tup:
            return output

    return 'unexpected'


def get_search_key(machine):
    """
    Return search key to be used by Workflow.filter
    """
    meta = machine[1]
    fields = [meta['name'],
              meta['vagrantfile_path'],
              meta['provider']]
    return ' '.join(fields)


def list_machines(machines, wf):
    subtitles_dict = {'cmd': 'Run commands on whole environment'}

    for mid, meta in machines.iteritems():
        wf.add_item(title=meta['name'],
                    subtitle=meta['vagrantfile_path'],
                    modifier_subtitles=subtitles_dict,
                    arg=mid,
                    uid=mid,
                    valid=True,
                    icon=get_state_icon(meta['state'], meta['provider']))


def list_actions(eid, wf):
    if os.path.isdir(eid):
        def test(info):
            return not info['dir_action']
    else:
        machine_data = get_machine_data()
        state = normalize_state(machine_data[eid]['state'])
        norm_state = normalize_state(state)

        def test(info):
            return norm_state not in info['state']

    for action, prop in actions.iteritems():
        if test(prop):
            continue
        wf.add_item(title=action,
                    subtitle=prop['desc'],
                    uid=action,
                    arg='{0} {1!r}'.format(
                        eid, ' '.join([action, prop['flags'] or ''])),
                    icon=get_action_icon(action),
                    valid=True)


def validate_version(version):
    if version != 1:
        raise Exception('Unsupported index version')


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
                       help='Store %(metavar)s '
                            'to be retrived later as env dir')
    group.add_argument('--get',
                       action='store_true',
                       help='Get value which was previously stored')
    group.add_argument('--execute',
                       nargs=2,
                       metavar=('ID', 'COMMAND'),
                       help='Execute command on specific VM or entire'
                            ' environment in the background')
    args = parser.parse_args(wf.args)

    if args.list is not None:
        machine_data = get_machine_data()
        if args.list:
            machine_data = dict(wf.filter(query=args.list,
                                          items=machine_data.items(),
                                          key=get_search_key,
                                          match_on=MATCH_ALL ^ MATCH_ALLCHARS))
        list_machines(machine_data, wf)
    elif args.set:
        logger.debug('saving id: {0}'.format(args.set))
        wf.cache_data('id', args.set)
        run_alfred(':vagrant-id')
    elif args.setenv:
        machine_data = get_machine_data()
        vagrant_dir = machine_data[args.setenv]['vagrantfile_path']
        logger.debug('saving id: {0}'.format(vagrant_dir))
        wf.cache_data('id', vagrant_dir)
        run_alfred(':vagrant-id')
    elif args.get:
        eid = wf.cached_data('id', max_age=2)
        vpath = eid
        if not os.path.isfile(eid):
            machine_data = get_machine_data()
            vpath = machine_data[eid]['vagrantfile_path']
        task_name = 'exec_{0}'.format(hash(vpath))
        logger.debug('retrieved id: {0}'.format(eid))
        if eid is None:
            raise RuntimeError('No environment id cached')
        elif is_running(task_name):
            raise Exception('Task in progress')
        else:
            list_actions(eid, wf)
    elif args.execute:
        machine_data = get_machine_data()
        vpath = args.execute[0]
        if not os.path.isdir(vpath):
            vpath = machine_data[args.execute[0]]['vagrantfile_path']
        task_name = 'exec_{0}'.format(hash(vpath))
        cmd = ['/usr/bin/python', 'execute.py'] + args.execute
        run_in_background(task_name, cmd)

    wf.send_feedback()


if __name__ == '__main__':
    workflow = Workflow()
    logger = workflow.logger
    sys.exit(workflow.run(main))
