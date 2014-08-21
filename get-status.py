import os
import sys
from argparse import ArgumentParser
from subprocess import call
from json import load
from workflow import Workflow, MATCH_ALL, MATCH_ALLCHARS, ICON_ERROR

logger = None
VAGRANT_DEFAULT_INDEX = '~/.vagrant.d/data/machine-index/index'
ICONS_STATES_PATH = 'icons/states'
ICONS_ACTION_PATH = 'icons/actions'


# TODO: vagrant_index should check env variable VAGRANT_HOME
def _get_index_data():
    return _read_index(VAGRANT_DEFAULT_INDEX)


# TODO: handle invalid json
def _read_index(path):
    with open(os.path.expanduser(path)) as index:
        return load(index)


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

    logger.debug('normalized state. in: {}, out: {}'.format(state, out))
    return out


def _get_search_key(machine):
    """
    Return search key to be used by Workflow.filter
    """
    fields = []
    fields.append(machine['name'])
    fields.append(machine['vagrantfile_path'])
    fields.append(machine['provider'])
    logger.debug('search string: {}'.format(fields))
    return ' '.join(fields)


def _list_machines(machines, workflow):
    subtitles_dict = {'cmd': 'Run commands on whole environment'}

    for item in machines:
        workflow.add_item(title=item['name'],
                          subtitle=item['vagrantfile_path'],
                          modifier_subtitles=subtitles_dict,
                          arg=item['id'],
                          uid=item['id'],
                          valid=True,
                          icon=_get_state_icon(item['state'], item['provider']))


def _list_machine_actions(mid, data, workflow):
    actions = {
        'up': {
            'desc': 'Starts and provisions the vagrant environment',
            'flags': None,
            'state': ['paused', 'stopped']
        },
        'halt': {
            'desc': 'Stops the machine',
            'flags': None,
            'state': ['running', 'paused']
        },
        'resume': {
            'desc': 'Resume a suspended machine',
            'flags': None,
            'state': ['paused']
        },
        'suspend': {
            'desc': 'Suspends the machine',
            'flags': None,
            'state': ['running']
        },
        'provision': {
            'desc': 'Provisions the machine',
            'flags': None,
            'state': ['running']
        },
        'rdp': {
            'desc': 'Connects to machine via RDP',
            'flags': None,
            'state': ['running']
        },
        'ssh': {
            'desc': 'Connects to machine via SSH',
            'flags': None,
            'state': ['running']
        },
        'destroy': {
            'desc': 'Stops and deletes all traces of the machine',
            'flags': '-f',
            'state': ['running', 'paused', 'stopped']
        }
    }

    if mid in data['machines']:
        for action, info in actions.iteritems():
            if _normalize_state(data['machines'][mid]['state']) in info['state']:
                workflow.add_item(title=action,
                                  subtitle=info['desc'],
                                  uid=action,
                                  arg='{} {}'.format(action, mid),
                                  icon=_get_action_icon(action),
                                  valid=True)
    else:
        workflow.add_item(title="Machine doesn't exits",
                          subtitle='',
                          icon=ICON_ERROR,
                          valid=False)


def _validate_version(version):
    logger.debug('index file version: {}'.format(version))
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


# TODO: handle possible failiure of osascript?
def _run_alfred(action):
    """Launch Alfred 2 via AppleScript and search for 'action'"""
    call(['osascript', '-e',
          'tell application "Alfred 2" to search "{}"'.format(action)])


def main(wf):
    logger.debug('wf.args: {}'.format(wf.args))

    parser = ArgumentParser()
    # group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('--list', action='store_true',
                        help='List vagrant machines')
    parser.add_argument('--filter', nargs='?', help='Filter by FILTER')
    parser.add_argument('--id', help='Show actions for specific machine')
    parser.add_argument('--get', action='store_true', help='blah')
    args = parser.parse_args(wf.args)
    logger.debug('args: {}'.format(args))

    raw_data = _get_index_data()
    logger.debug('raw data: {}'.format(raw_data))

    _validate_version(raw_data['version'])
    modified_data = _rearrange_data(raw_data)
    logger.debug('modified data: {}'.format(modified_data))

    if args.list:
        logger.debug('listing vagrant boxes')
        if args.filter:
            logger.debug('filter: {}'.format(args.filter))
            modified_data = wf.filter(args.filter, modified_data,
                                      _get_search_key,
                                      match_on=MATCH_ALL ^ MATCH_ALLCHARS)
            logger.debug('filtered data: {}'.format(modified_data))
        _list_machines(modified_data, wf)
    elif args.id:
        logger.debug('saving id: {}'.format(args.id))
        wf.settings['id'] = args.id
        _run_alfred(':vagrant-id')
    elif args.get:
        mid = wf.settings.get('id')
        logger.debug('retrieved id: {}'.format(mid))
        _list_machine_actions(mid, raw_data, wf)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    logger = wf.logger
    sys.exit(wf.run(main))
