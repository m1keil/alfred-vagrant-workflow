import os
import json

from commons import run_vagrant
from properties import actions, states

from workflow import Workflow
from workflow.background import run_in_background

ICONS_STATES_PATH = os.path.join(Workflow().workflowdir, 'icons', 'states')
ICONS_ACTION_PATH = os.path.join(Workflow().workflowdir, 'icons', 'actions')

logger = Workflow().logger


class Machine:
    """
    A Vagrant machine.
    """
    def __init__(self, **kwargs):
        self.key = kwargs['key']
        self.name = kwargs['name']
        self.provider = kwargs['provider']
        self.state = kwargs['state']
        self.vagrantfile_path = kwargs['vagrantfile_path']
        self.normalized_state = self.normalize_state(self.state)

    @property
    def actions(self):
        def f(state):
            return self.normalized_state in state

        return [Action(action) for action, props in actions.iteritems()
                if f(props['state'])]

    @property
    def icon(self):
        icon = os.path.join(ICONS_STATES_PATH,
                            '{0}.{1}.png'.format(self.provider, self.normalized_state))
        default = os.path.join(ICONS_STATES_PATH,
                               'vagrant.{0}.png'.format(self.normalized_state))

        if os.path.isfile(icon):
            return icon
        elif os.path.isfile(default):
            return default
        else:
            return None

    @staticmethod
    def normalize_state(state):
        for states_tup, output in states.iteritems():
            if state in states_tup:
                return output

        raise Exception('Unable to normalize state: {state}'.format(state=state))

    def run(self, action, env=False):
        action = Action(action)
        if not filter(lambda x: x.name == action.name, self.actions):
            raise Exception("Action not found. Instance changed state?")

        task_name = 'exec{0}'.format(hash(self.vagrantfile_path))

        if action.name in ('rdp', 'ssh'):
            run_vagrant('{action} {machine_id}'.format(action=action.name,
                                                       machine_id=self.key))
            return

        cur_dir = os.path.dirname(os.path.realpath(__file__))
        cmd = ['python', os.path.join(cur_dir, 'execute.py'), '--action', action.name]

        if action.flags:
            cmd += ['-f {0}'.format(flag) for flag in action.flags]
        if not env:
            cmd += ['--name', self.name]

        logger.debug('Running in background: ' + str(cmd))
        new_env = os.environ.copy()
        new_env['HOME'] = os.path.expanduser('~')
        new_env['PATH'] = Workflow().settings['PATH']['VAR']
        run_in_background(task_name,
                          cmd,
                          env=new_env,
                          cwd=self.vagrantfile_path)

    def __call__(self, query=None):
        if not query:
            return self.actions
        return Workflow().filter(query=query,
                                 items=self.actions,
                                 key=lambda x: x.name)


class Action:
    """
    A Vagrant machine action.
    """
    def __init__(self, action):
        if action not in actions:
            raise Exception('Unknown action type')

        self.name = action
        self.description = actions[action].get('desc', '')
        self.flags = actions[action].get('flags', None)
        self.dir_action = actions[action].get('dir_action', True)
        self.confirm = actions[action].get('confirm', False)

    @property
    def icon(self):
        icon = os.path.join(ICONS_ACTION_PATH, '{0}.png'.format(self.name))
        if os.path.isfile(icon):
            return icon
        else:
            return None


class Index:
    """
    A Vagrant Index.
    """
    @staticmethod
    def parse_v1_machines(mdict):
        return {key: Machine(key=key, **val) for key, val in mdict.iteritems()}

    def __init__(self, fh):
        content = json.load(fh)

        self.version = content['version']
        if self.version == 1:
            self.machines = self.parse_v1_machines(content['machines'])
            # TODO: this is just a hack
            self.test = {key[0:8]: key for key in self.machines.iterkeys()}
        else:
            raise Exception('Vagrant index version {0} is not supported'.format(self.version))

    def __iter__(self):
        return self.machines.iteritems()

    def __call__(self, query=None):
        if not query:
            return self.__iter__()
        return Workflow().filter(query=query,
                                 items=self.__iter__(),
                                 key=lambda x: x[1].name + x[1].vagrantfile_path + x[1].key)

    def __getitem__(self, machine_id):
        if machine_id in self.machines:
            return self.machines[machine_id]
        elif machine_id in self.test:
            return self.machines[self.test[machine_id]]
        else:
            raise Exception("Machine not found")
