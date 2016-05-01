#!/usr/bin/python
# coding=utf-8
from __future__ import unicode_literals

import os
import sys
from argparse import ArgumentParser

from vagrant import VagrantIndex
from properties import modifiers
from workflow import Workflow, ICON_WARNING


logger = None
SEP = '►'
# TODO: make this configurable
VAGRANT_HOME = os.path.expanduser('~/.vagrant.d')
VAGRANT_INDEX = os.path.join(VAGRANT_HOME, 'data', 'machine-index', 'index')


def show_dummy(machine_id, action, wf):
    wf.add_item(title='Confirm',
                subtitle='You will loose all the data on the machine',
                modifier_subtitles=modifiers,
                arg='{action} {id}'.format(id=machine_id, action=action),
                icon=ICON_WARNING,
                valid=True)


def show_machines(query, wf):
    with open(VAGRANT_INDEX) as fh:
        vi = VagrantIndex(fh)

    for machine_id, machine in vi(query):
        wf.add_item(title=machine.name,
                    subtitle=machine.vagrantfile_path,
                    autocomplete=machine_id[0:8] + ' ' + SEP + ' ',
                    icon=machine.icon,
                    valid=False)


def show_actions(machine_id, query, wf):
    with open(VAGRANT_INDEX) as fh:
        vi = VagrantIndex(fh)

    machine = vi[machine_id]
    for action in machine(query):
        if action.confirm:
            autocomplete = machine_id + ' ' + SEP + ' ' + action.name + ' ' + SEP + ' '
        else:
            autocomplete = machine_id + ' ' + SEP + ' ' + action.name

        wf.add_item(title=action.name,
                    subtitle=action.description,
                    modifier_subtitles=modifiers,
                    autocomplete=autocomplete,
                    arg='{action} {id}'.format(id=machine_id, action=action.name),
                    icon=action.icon,
                    valid=(not action.confirm))


def do_list(args, wf):
    query = ' '.join(args).strip() if len(args) is not 0 else ''
    count = query.count(SEP)
    if count == 0:
        show_machines(query, wf)
    elif count == 1:
        show_actions(query.split(SEP)[0].strip(), query.split(SEP)[1].strip(), wf)
    else:
        show_dummy(query.split(SEP)[0].strip(), query.split(SEP)[1].strip(), wf)


def do_execute(args, env=False):
    action, machine_id = args
    with open(VAGRANT_INDEX) as fh:
        vi = VagrantIndex(fh)
    machine = vi[machine_id]
    machine.run(action, env)


def get_parser():
    """
    Parse command line argument and return parser object
    """
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list',
                       nargs='*',
                       metavar='QUERY',
                       help='List Vagrant machines and actions. '
                            'If %(metavar)s is provided, will filter results '
                            'by fuzzy searching')
    group.add_argument('--execute',
                       nargs=2,
                       metavar=('COMMAND', 'ID'),
                       help='Execute command on specific VM in the background')
    group.add_argument('--env',
                       nargs=2,
                       metavar=('COMMAND', 'ID'),
                       help='Execute command on entire environment in the background')
    return parser


def main(wf):
    """
    Main program entry point
    """
    parser = get_parser()
    args = parser.parse_args(wf.args)

    if args.list is not None:
        do_list(args.list, wf)
    elif args.execute:
        do_execute(args.execute)
    elif args.env:
        do_execute(args.env, env=True)

    wf.send_feedback()

if __name__ == '__main__':
    workflow = Workflow()
    logger = workflow.logger
    sys.exit(workflow.run(main))
