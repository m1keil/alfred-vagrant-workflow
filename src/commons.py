import os
from workflow import Workflow
from subprocess import call

logger = Workflow().logger


def external_trigger(name, argument):
    """
    Call to external trigger in Alfred.

    Args:
        name (str): Name of the trigger.
        argument: Argument to the trigger.
    """
    if 'alfred_version' not in os.environ:
        logger.debug('"alfred_version" env var not found. Exiting')
        return

    major_version = os.environ['alfred_version'].split('.')[0]
    logger.debug('Alfred major version: {0}'.format(major_version))
    osascript = 'tell application "Alfred {version}" to run trigger "{name}" ' \
                'in workflow "{uuid}" with argument "{arg}"' \
        .format(version=major_version,
                name=name,
                uuid=os.environ['alfred_workflow_bundleid'],
                arg=argument)

    try:
        call(['/usr/bin/osascript', '-e', osascript])
    except OSError as e:
        logger.error('Calling osascript failed: {code} {message}'
                     .format(code=e.errno, message=e.message))


def send_notification(msg):
    """
    Trigger notification with msg as content.

    Args:
        msg (str): Notification message.
    """
    external_trigger('send_notification', msg)


def run_vagrant(arg):
    """
    Trigger running Vagrant in terminal.

    Args:
        arg (str): Vagrant command line arguments in one string.
    """
    external_trigger('run_vagrant', arg)


def opensettings(workflow_settings):
    """
    Open settings.json file with system's default editor
    Args:
        workflow_settings: settings.json file path
    """
    call(['/usr/bin/open', workflow_settings])
