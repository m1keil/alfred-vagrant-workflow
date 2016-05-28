import mock
import unittest
from commons import external_trigger


class Test(unittest.TestCase):
    @mock.patch('commons.call')
    def test_external_trigger(self, mock_call):
        external_trigger('name', 'argument')
        mock_call.assert_called_once_with(['/usr/bin/osascript',
                                           '-e',
                                           'tell application "Alfred 2" to '
                                           'run trigger "name" in workflow '
                                           '"com.sverdlik.michael" with '
                                           'argument "argument"'])
