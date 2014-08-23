import sys
from os.path import isdir
from subprocess import call, check_output, CalledProcessError
from workflow import Workflow
from commons import send_notification


def main(wf):
    wf.logger.debug('argv: {}'.format(sys.argv))

    env_id = sys.argv[1]
    cmd = sys.argv[2:]

    actions = 'up halt resume suspend provision destroy'.split(' ')
    if cmd[0] not in actions:
        wf.logger.debug('Error, invalid action')
        sys.exit(1)

    if isdir(env_id):
        pass
    else:
        command = ['vagrant'] + cmd + [env_id]
        try:
            out = check_output(command)
        except CalledProcessError as e:
            wf.logger.debug('error: {}'.format(e))
            send_notification('{} failed'.format(cmd[0]))
        wf.logger.debug('finished: {}'.format(out))
        send_notification('{} finished succesfully'.format(cmd[0]))


if __name__ == '__main__':
    wf = Workflow()
    wf.run(main)