import sys
import os
from subprocess import check_output, CalledProcessError
from workflow import Workflow
from commons import send_notification


def main(wf):
    env_id = sys.argv[1]
    action = sys.argv[2].split(' ')[0]
    flags = sys.argv[2].strip().split(' ')[1:]

    if os.path.isdir(env_id):
        vagrant_path = env_id
        command = ['vagrant', action] + flags
    else:
        vagrant_path = None
        command = ['vagrant', action] + flags + [env_id]

    try:
        out = check_output(command, cwd=vagrant_path)
        wf.logger.debug('finished: {}'.format(out))
    except CalledProcessError as e:
        wf.logger.debug('error: {}'.format(e))
        send_notification('{} failed'.format(action))
    else:
        send_notification('{} finished succesfully'.format(action))

if __name__ == '__main__':
    workflow = Workflow()
    workflow.run(main)