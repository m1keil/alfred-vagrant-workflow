import os
import unittest
import tempfile
from copy import deepcopy
from json import dump

import vagrantup
import commons


class Test(unittest.TestCase):
    def test_validate_version(self):
        self.assertTrue(vagrantup._validate_version(1) is None)
        self.assertRaises(Exception, vagrantup._validate_version, 0)

    def test_normalize_state(self):
        for states, output in commons.states.items():
            for state in states:
                self.assertEqual(vagrantup._normalize_state(state), output)
        self.assertEqual(vagrantup._normalize_state('bla'), 'unexpected')

    def test_get_state_icon(self):
        providers = ['virtualbox', 'vmware_fusion']
        states = ['not created', 'paused', 'running', 'stopped', 'unknown']

        for provider in providers:
            for state in states:
                icon_path = vagrantup._get_state_icon(state, provider)
                icon_name = os.path.basename(icon_path)
                self.assertFalse(icon_path is None)
                self.assertEqual(icon_name.split('.')[-3], provider)
                self.assertTrue(os.path.isfile(icon_path))

        for state in states:
            icon_path = vagrantup._get_state_icon('unknown', state)
            self.assertFalse(icon_path is None)
            self.assertTrue(os.path.isfile(icon_path))

        vagrantup.ICONS_STATES_PATH = os.getcwd()
        self.assertTrue(vagrantup._get_state_icon('x', 'y') is None)

    def _get_action_icon(self):
        actions = ['destroy', 'halt', 'provision',
                   'rdp', 'resume', 'ssh', 'suspend', 'up']
        for action in actions:
            icon_path = vagrantup._get_action_icon(action)
            self.assertFalse(icon_path is None)
            self.assertTrue(os.path.isfile(icon_path))

        self.assertTrue(vagrantup._get_action_icon('x') is None)


class TestVagrantHome(unittest.TestCase):
    def setUp(self):
        self.original_environ = deepcopy(os.environ)
        self.index_content = {'version': 1, 'machines': {'test': 'data'}}
        self.vagrant_home = create_vagrant_home(self.index_content)

    def tearDown(self):
        os.environ = self.original_environ

    def test_get_machine_data_with_env(self):
        os.environ['VAGRANT_HOME'] = self.vagrant_home
        index_data = vagrantup._get_machine_data()
        self.assertEqual({'test': 'data'}, index_data)

    def test_get_machine_data(self):
        vagrantup.VAGRANT_HOME = self.vagrant_home
        index_data = vagrantup._get_machine_data()
        self.assertEqual(self.index_content['machines'], index_data)


def create_vagrant_home(index_content):
    vagrant_home = tempfile.mkdtemp()
    path, file_name = os.path.split(vagrantup.VAGRANT_INDEX)
    os.makedirs(os.path.join(vagrant_home, path))
    full_path = os.path.join(vagrant_home, path, file_name)
    with open(full_path, 'w') as f:
        dump(index_content, f)
    return vagrant_home

if __name__ == '__main__':
    unittest.main()
