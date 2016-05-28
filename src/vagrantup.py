#!/usr/bin/python
# coding=utf-8
from __future__ import unicode_literals

import sys
from argparse import ArgumentParser

from vagrant import Index
from properties import modifiers, path
from commons import opensettings
from workflow import Workflow, ICON_WARNING, ICON_INFO
from workflow.background import is_running


logger = None
SEP = '►'

WORKFLOW_URL = 'https://github.com/m1keil/alfred-vagrant-workflow'


def add_warning(wf, machine_id, action):
    """
    Add warning item to Workflow object.

    Args:
        wf (Workflow): Workflow object.
        machine_id (unicode): Vagrant's machine ID.
        action (unicode): Vagrant's action.
    """
    wf.add_item(title='Are you sure?',
                subtitle='This action is not recoverable',
                modifier_subtitles=modifiers,
                arg='{action} {mid}'.format(mid=machine_id, action=action),
                icon=ICON_WARNING,
                valid=True)


def add_machines(wf, query=None):
    """
    Add machine items to Workflow object. If query provided, filter out items
    by fuzzy searching with the query string.

    Args:
        wf (Workflow): Workflow object.
        query (optional[unicode]): Fuzzy search query.
    """
    with open(wf.settings['PATH']['INDEX']) as fh:
        vi = Index(fh)

    for machine_id, machine in vi(query):
        autocomplete = '{mid} {sep} '.format(mid=machine_id[0:8], sep=SEP)
        wf.add_item(title=machine.name,
                    subtitle=machine.vagrantfile_path,
                    autocomplete=autocomplete,
                    icon=machine.icon,
                    valid=False)


def add_actions(wf, machine_id, query=None):
    """
    Add action items to Workflow object. If query is provided, filter out
    items by fuzzy searching with the query string.

    Args:
        wf (Workflow): Workflow object.
        machine_id (unicode): Vagrant's machine ID.
        query (optional[unicode]): Fuzzy search query.
    """
    with open(wf.settings['PATH']['INDEX']) as fh:
        vi = Index(fh)

    machine = vi[machine_id]
    task_name = 'exec{0}'.format(hash(machine.vagrantfile_path))

    if is_running(task_name):
        subtitle = 'A task already running on {env_path} environemnt' \
                   ''.format(env_path=machine.vagrantfile_path)
        wf.add_item(title='Please wait..',
                    subtitle=subtitle,
                    icon=ICON_INFO,
                    valid=False)
    else:
        for action in machine(query):
            autocomplete = '{mid} {sep} {action}'.format(mid=machine_id,
                                                         sep=SEP,
                                                         action=action.name)
            if action.confirm:
                autocomplete += ' {sep} '.format(sep=SEP)

            wf.add_item(title=action.name,
                        subtitle=action.description,
                        modifier_subtitles=modifiers,
                        autocomplete=autocomplete,
                        arg='{action} {mid}'.format(mid=machine_id,
                                                    action=action.name),
                        icon=action.icon,
                        valid=not action.confirm)


def do_list(wf, args):
    """
    Depanding on the arguments, will run the appropriate functions to add
    machine, action or warning item(s) to Workflow object.

    Args:
        wf (Workflow): Workflow object.
        args (list): List of arguments.
    """
    def _safe_get(l, i):
        try:
            return l[i]
        except IndexError:
            return None

    count = args.count(SEP)
    if count == 0:
        add_machines(wf, _safe_get(args, 0))
    elif count == 1:
        add_actions(wf, args[0], _safe_get(args, 2))
    else:
        add_warning(wf, args[0], _safe_get(args, 4))


def do_execute(wf, args, env=False):
    """
    Executes Vagrant's commands. If env is True, execute command on the entire
    Vagrant environemnt.

    Args:
        wf (Workflow): Workflow object.
        args (list): A list in the form of [action, machine_id].
        env (bool): If True, execute comman on the entire environment. Else
                    execute only on the machine.
    """
    action, machine_id = args
    with open(wf.settings['PATH']['INDEX']) as fh:
        vi = Index(fh)
    machine = vi[machine_id]
    machine.run(action, env)


def parse_args(args):
    """
    Parse command line argument and return parsed Namespace object.

    Args:
        args (list): List of arguments.

    Returns:
        argparse.Namespace: Parsed arguments Namespace object.
    """
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list',
                       nargs='*',
                       metavar='QUERY',
                       help='List Vagrant machines and actions. '
                            'If %(metavar)s is provided, will filter results '
                            'by fuzzy searching.')
    group.add_argument('--machine',
                       nargs=2,
                       metavar=('COMMAND', 'ID'),
                       help='Execute command on specific machine.')
    group.add_argument('--env',
                       nargs=2,
                       metavar=('COMMAND', 'ID'),
                       help='Execute command on entire environment.')

    return parser.parse_args(args)


def main(wf):
    """
    Main program entry point.

    Args:
        wf (Workflow): Workflow object.
    """
    args = parse_args(wf.args)
    if args.machine:
        do_execute(wf, args.machine)
    elif args.env:
        do_execute(wf, args.env, env=True)
    else:
        do_list(wf, args.list)
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(help_url=WORKFLOW_URL, default_settings={'PATH': path})

    wf.magic_arguments['settings'] = lambda: opensettings(wf.settings_path)

    logger = wf.logger
    sys.exit(wf.run(main))
