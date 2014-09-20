import sys
import os
import tempfile
from subprocess import Popen
from workflow import Workflow
from commons import send_notification


def main(wf):
    env_id = sys.argv[1]
    action = sys.argv[2].split(' ')[0]
    flags = sys.argv[2].strip().split(' ')[1:]

    vagrant_path = None
    show_notification = True

    if os.path.isdir(env_id):
        vagrant_path = env_id
        command = ['vagrant', action] + flags
    elif action in ('ssh', 'rdp'):
        tmp = tempfile.mkstemp(suffix='.command')[1]
        os.chmod(tmp, 0700)
        with open(tmp, 'w') as f:
            f.write('clear; vagrant {} {}'.format(action, env_id))
        command = ['open', tmp]
        show_notification = False
    else:
        command = ['vagrant', action] + flags + [env_id]

    process = Popen(command, cwd=vagrant_path)
    output, unused_err = process.communicate()
    retcode = process.poll()
    message = 'finished succesfully'
    if retcode:
        wf.logger.debug('execution failed:\n{}'.format(output))
        message = 'failed'
    if show_notification:
        send_notification('{} {}'.format(action, message))


if __name__ == '__main__':
    workflow = Workflow()
    workflow.run(main)
