import sys
import os
from subprocess import Popen
from workflow import Workflow
from commons import send_notification, run_vagrant


def main(wf):
    env_id = sys.argv[1]
    action = sys.argv[2].split(' ')[0]
    flags = sys.argv[2].strip().split(' ')[1:]

    vagrant_path = None

    if os.path.isdir(env_id):
        vagrant_path = env_id
        command = ['vagrant', action] + flags
    elif action in ('ssh', 'rdp'):
        run_vagrant('{0} {1}'.format(action, env_id))
        return
    else:
        command = ['vagrant', action] + flags + [env_id]

    process = Popen(command, cwd=vagrant_path)
    output, unused_err = process.communicate()
    retcode = process.poll()
    message = 'finished succesfully'
    if retcode:
        wf.logger.debug('execution failed:\n{0}'.format(output))
        message = 'failed'
    send_notification('{0} {1}'.format(action, message))


if __name__ == '__main__':
    workflow = Workflow()
    workflow.run(main)
