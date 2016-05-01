from argparse import ArgumentParser
from subprocess import Popen, PIPE, STDOUT

from workflow import Workflow
from commons import send_notification

logger = Workflow().logger


def spawn_process(action, flags=None, machine_name=None):
    command = ['vagrant', action]

    if flags:
        command += ['-' + str(flag) for flag in flags]

    if machine_name:
        command.append(machine_name)

    logger.debug('Calling ' + str(command))
    return Popen(command, stdout=PIPE, stderr=STDOUT)


def parse_process_output(process):
    while True:
        line = process.stdout.readline()
        if not line:
            break
        logger.debug(line.strip())
    return_code = process.wait()
    logger.debug('Return code: ' + str(return_code))

    return 'finished succesfully' if return_code == 0 else 'failed'


def parse_arguments():
    """
    Parse command line argument and return parser object
    """

    description = """This script will run the actual Vagrant commands.
    It works under the assumption that the PATH & HOME variables are set correctly and that CWD
    is the correct Vagrant directory.
    """

    parser = ArgumentParser(description=description)
    parser.add_argument('-a', '--action', required=True, help='Vagrant action to execute')
    parser.add_argument('-f', '--flags', nargs='?', action='append', default=[], help='Vagrant command flags')
    parser.add_argument('-n', '--name', help='Vagrant machine name')
    return parser.parse_args()


def main():
    args = parse_arguments()

    process = spawn_process(action=args.action, flags=args.flags, machine_name=args.name)
    message = parse_process_output(process)
    send_notification('{0} {1}'.format(args.action, message))


if __name__ == '__main__':
    main()
