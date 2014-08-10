import sys
import logging
from os.path import isdir
from os import devnull
from subprocess import call
from workflow import background


def output_to_alfred(msg):
    print msg


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    # print 'argv: {}'.format(sys.argv)
    logger.debug('argv: {}'.format(sys.argv))
    if len(sys.argv) != 3:
        output_to_alfred('Error')
        sys.exit(1)

    actions = 'up halt resume suspend provision rdp ssh destroy'.split(' ')
    if sys.argv[1] not in actions:
        output_to_alfred('Error')
        sys.exit(1)

    if isdir(sys.argv[2]):
        pass
    else:
        out = call(['vagrant'] + sys.argv[1:], stdout=open(devnull, 'w'))
        logger.debug(out)
    sys.exit(1)


if __name__ == '__main__':
    main()