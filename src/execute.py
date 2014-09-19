import sys
import os
import tempfile
from subprocess import check_output, CalledProcessError
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

    try:
        out = check_output(command, cwd=vagrant_path)
        wf.logger.debug('finished: {}'.format(out))
    except CalledProcessError as e:
        wf.logger.debug('error: {}'.format(e))
        if show_notification:
            send_notification('{} failed'.format(action))
    else:
        if show_notification:
            send_notification('{} finished succesfully'.format(action))

if __name__ == '__main__':
    workflow = Workflow()
    workflow.run(main)