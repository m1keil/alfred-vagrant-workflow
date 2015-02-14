import sys
import os
from subprocess import Popen, PIPE
from workflow import Workflow
from commons import send_notification, run_vagrant

logger = None


def parse_argv(args):
    return args[1], args[2].split(' ')


def spawn_process(env_id, action):
    vagrantfile_path = None
    if os.path.isdir(env_id):
        vagrantfile_path = env_id
        command = ['vagrant'] + action
    else:
        command = ['vagrant'] + action + [env_id]
    return Popen(command, cwd=vagrantfile_path, stdout=PIPE, stderr=PIPE)


def parse_process_output(process):
    stdout, stderr = process.communicate()
    return_code = process.poll()
    logger.debug('exec output:\nstdout: {0}\nstderr{1}'.format(stdout, stderr))
    if return_code:
        message = 'failed'
    else:
        message = 'finished succesfully'
    return message


def main():
    env_id, action = parse_argv(sys.argv)

    if action[0] in ('ssh', 'rdp'):
        run_vagrant('{0} {1}'.format(action[0], env_id))
        return
    else:
        process = spawn_process(env_id, action)

    message = parse_process_output(process)
    send_notification('{0} {1}'.format(action[0], message))


if __name__ == '__main__':
    logger = Workflow().logger
    main()
