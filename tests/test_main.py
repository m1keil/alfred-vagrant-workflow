import os
import string
import random
import unittest
import tempfile
from copy import deepcopy
from json import dump

import vagrantup
import commons
import workflow


class Test(unittest.TestCase):
    def test_validate_version(self):
        self.assertTrue(vagrantup.validate_version(1) is None)
        self.assertRaises(Exception, vagrantup.validate_version, 0)

    def test_normalize_state(self):
        for states, output in commons.states.items():
            for state in states:
                self.assertEqual(vagrantup.normalize_state(state), output)
        self.assertEqual(vagrantup.normalize_state('bla'), 'unexpected')

    def test_get_state_icon(self):
        providers = ['virtualbox', 'vmware_fusion']
        states = ['not created', 'paused', 'running', 'stopped', 'unknown']

        for provider in providers:
            for state in states:
                icon_path = vagrantup.get_state_icon(state, provider)
                icon_name = os.path.basename(icon_path)
                self.assertFalse(icon_path is None)
                self.assertEqual(icon_name.split('.')[-3], provider)
                self.assertTrue(os.path.isfile(icon_path))

        for state in states:
            icon_path = vagrantup.get_state_icon('unknown', state)
            self.assertFalse(icon_path is None)
            self.assertTrue(os.path.isfile(icon_path))

        vagrantup.ICONS_STATES_PATH = os.getcwd()
        self.assertTrue(vagrantup.get_state_icon('x', 'y') is None)

    def test_get_action_icon(self):
        actions = ['destroy', 'halt', 'provision',
                   'rdp', 'resume', 'ssh', 'suspend', 'up']
        for action in actions:
            icon_path = vagrantup.get_action_icon(action)
            self.assertFalse(icon_path is None)
            self.assertTrue(os.path.isfile(icon_path))

        self.assertTrue(vagrantup.get_action_icon('x') is None)

    def test_list_machines(self):
        wf = workflow.Workflow()
        machines = generate_index()['machines']
        vagrantup.list_machines(machines, wf)
        for item in wf._items:
            mid, vagrantfile_path = item.arg.split(' ')
            meta = machines[mid]
            self.assertTrue(mid in machines.keys())
            self.assertTrue(item.uid in machines.keys())
            self.assertEqual(item.title, meta['name'])
            self.assertEqual(item.subtitle, meta['vagrantfile_path'])
            self.assertEqual(vagrantfile_path, meta['vagrantfile_path'])
            self.assertEqual(item.valid, True)
            self.assertFalse(item.icon, None)

    def test_empty_machine_index(self):
        wf = workflow.Workflow()
        old_get = vagrantup.get_machine_data
        vagrantup.get_machine_data = lambda: generate_index(0)['machines']
        vagrantup.do_list([], wf)
        vagrantup.get_machine_data = old_get
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].valid, False)

    def test_get_search_key(self):
        machine = generate_machine().items()[0]
        meta = machine[1]
        self.assertEqual(' '.join([meta['name'],
                                   meta['vagrantfile_path'],
                                   meta['provider']]),
                         vagrantup.get_search_key(machine))


class TestVagrantHome(unittest.TestCase):
    def setUp(self):
        self.original_environ = deepcopy(os.environ)
        self.index_content = generate_index()
        self.vagrant_home = create_vagrant_home(self.index_content)

    def tearDown(self):
        os.environ = self.original_environ

    def test_get_machine_data_with_env(self):
        os.environ['VAGRANT_HOME'] = self.vagrant_home
        index_data = vagrantup.get_machine_data()
        self.assertEqual(self.index_content['machines'], index_data)

    def test_get_machine_data(self):
        vagrantup.VAGRANT_HOME = self.vagrant_home
        index_data = vagrantup.get_machine_data()
        self.assertEqual(self.index_content['machines'], index_data)


class TestCommandLine(unittest.TestCase):
    def setUp(self):
        parser = vagrantup.get_parser()
        self.parser = parser

    def test_with_empty_args(self):
        self.assertRaises(SystemExit, self.parser.parse_args, [])

    def test_with_help_args(self):
        self.assertRaises(SystemExit, self.parser.parse_args, ['--help'])


def create_vagrant_home(index_content):
    vagrant_home = tempfile.mkdtemp()
    path, file_name = os.path.split(vagrantup.VAGRANT_INDEX)
    os.makedirs(os.path.join(vagrant_home, path))
    full_path = os.path.join(vagrant_home, path, file_name)
    with open(full_path, 'w') as f:
        dump(index_content, f)
    return vagrant_home


def generate_index(machine_number=3):
    index = {
        'version': 1,
        'machines': {}
    }
    for _ in range(machine_number):
        index['machines'].update(generate_machine())
    return index


def id_generator(size=32, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_machine():
    return {
        id_generator(): {
            'extra_data': {
                'box': {
                    'name': 'ubuntu/trusty64',
                    'provider': 'virtualbox',
                    'version': '1.0',
                },
            },
            'local_data_path': '/tmp/file/.vagrant',
            'name': 'default',
            'provider': 'virtualbox',
            'state': 'running',
            'updated_at': None,
            'vagrantfile_name': None,
            'vagrantfile_path': '/tmp/file',
        }
    }

if __name__ == '__main__':
    unittest.main()
