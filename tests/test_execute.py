import mock
import unittest
import tempfile
from execute import parse_argv, spawn_process, Popen, parse_process_output


class Test(unittest.TestCase):
    def test_parse_argv(self):
        argv = ['', 'this', 'is test']
        self.assertEqual(tuple([argv[1], argv[2].split(' ')]),
                         parse_argv(argv))

    @mock.patch('execute.Popen')
    def test_get_process_with_dir(self, mock):
        spawn_process(tempfile.gettempdir(), ['cmd'])
        mock.assert_called_with(['vagrant', 'cmd'],
                                cwd=tempfile.gettempdir(),
                                stderr=-1,
                                stdout=-1)

    @mock.patch('execute.Popen')
    def test_get_process_with_eid(self, mock):
        spawn_process('eid', ['cmd', 'flag'])
        mock.assert_called_with(['vagrant', 'cmd', 'flag', 'eid'],
                                cwd=None,
                                stderr=-1,
                                stdout=-1)

    @mock.patch('execute.logger')
    def test_parse_process_output(self, mock_logger):
        process = mock.MagicMock(spec=Popen)
        process.communicate.return_value = (None, None)
        process.poll.return_value = 0
        message = parse_process_output(process)
        mock_logger.debug.assert_called_once_with('exec output:\nstdout:'
                                                  ' None\nstderrNone')
        self.assertEqual(message, 'finished succesfully')

        process.poll.return_value = -1
        message = parse_process_output(process)
        self.assertEqual(message, 'failed')