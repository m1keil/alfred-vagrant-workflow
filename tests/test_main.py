import unittest
import execute, vagrantup, commons


class Test(unittest.TestCase):

    def test_normalize_state(self):
        for states, output in commons.states.items():
            for state in states:
                self.assertEqual(vagrantup._normalize_state(state), output)
        self.assertEqual(vagrantup._normalize_state('bla'), 'unexpected')


if __name__ == '__main__':
    unittest.main()