from mock import patch
import unittest
import commons


class Test(unittest.TestCase):
    @patch('commons.call')
    def test_external_trigger(self, mocked_call):
        with patch.dict('os.environ', {'alfred_version': '3.0',
                                       'alfred_workflow_bundleid': 'a.b.c'}):
            commons.external_trigger('name', 'argument')
        mocked_call.assert_called_once()
