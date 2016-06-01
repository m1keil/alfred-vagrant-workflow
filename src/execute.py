from argparse import ArgumentParser
from subprocess import Popen, PIPE, STDOUT

from workflow import Workflow
from commons import send_notification


def spawn_process(action, flags=None, machine_name=None):
    """
    Spaws subprocess.

    Args:
        action (str): Vagrant action.
        flags (optional): An iterable of vagrant command flags.
        machine_name (optional[str]): Vagrant machine name.

    Returns:
        Popen: Popen instance
    """
    command = ['vagrant', action]

    if flags:
        command += ['-{0}'.format(flag) for flag in flags]

    if machine_name:
        command.append(machine_name)

    logger.debug('Calling: %s', command)
    return Popen(command, stdout=PIPE, stderr=STDOUT)


def parse_process_output(process):
    """
    Logs subprocess's stdout.

    Args:
        process (Popen): the process the log output from.
    """
    while True:
        line = process.stdout.readline()
        if not line:
            break
        logger.debug(line.strip())


def parse_arguments():
    """
    Parse command line argument and return argparse.Namespace object.

    Returns:
        argparse.Namespace: Parsed arguments Namespace object.
    """

    description = """
    This will run Vagrant executable.
    Works under the assumption that the PATH & HOME variables are set
    correctly and that CWD is relevant Vagrant environmnet directory.
    """

    parser = ArgumentParser(description=description)

    parser.add_argument('-a', '--action',
                        required=True,
                        help='Vagrant action to execute')

    parser.add_argument('-f', '--flags',
                        nargs='?',
                        action='append',
                        default=[],
                        help='Vagrant command flags')

    parser.add_argument('-n', '--name', help='Vagrant machine name')

    return parser.parse_args()


def main():
    """
    Main program entry point. Parse command line, execute subprocess and
    send notification at the end.
    """
    args = parse_arguments()

    process = spawn_process(action=args.action,
                            flags=args.flags,
                            machine_name=args.name)
    parse_process_output(process)

    return_code = process.wait()
    logger.debug('Return code: %s', return_code)
    message = 'finished succesfully' if return_code == 0 else 'failed'

    send_notification('{0} {1}'.format(args.action, message))


if __name__ == '__main__':
    logger = Workflow().logger
    main()
