import mock
import unittest
from commons import external_trigger, run_alfred, run_vagrant, open_terminal, \
    send_notification


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

    @mock.patch('commons.call')
    def test_run_alfred(self, mock_call):
        run_alfred('action')
        mock_call.assert_called_once_with(['/usr/bin/osascript',
                                           '-e',
                                           'tell application "Alfred 2" to '
                                           'search "action"'])

    @mock.patch('commons.external_trigger')
    def test_run_vagrant(self, mock_call):
        run_vagrant('arg')
        mock_call.assert_called_once_with('run_vagrant', 'arg')

    @mock.patch('commons.external_trigger')
    def test_open_terminal(self, mock_call):
        open_terminal('path')
        mock_call.assert_called_once_with('open_dir', 'path')

    @mock.patch('commons.external_trigger')
    def test_send_notification(self, mock_call):
        send_notification('msg')
        mock_call.assert_called_once_with('send_notification', 'msg')
