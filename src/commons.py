import os
from workflow import Workflow
from subprocess import call

logger = Workflow().logger


def external_trigger(name, argument):
    """
    Call to external trigger in Alfred.

    This utilize apple script functionality to trigger in Alfred.


    Args:
        name (str): Name of the trigger.
        argument: Argument to the trigger.

    Returns:
        int: Return code from osascript exec
    """
    major_version = os.environ['alfred_version'].split('.')[0]

    osascript = 'tell application "Alfred {version}" to run trigger ' \
                '"{name}" in workflow "{uuid}" with argument "{arg}"' \
        .format(version=major_version,
                name=name,
                uuid=os.environ['alfred_workflow_bundleid'],
                arg=argument)

    cmd = ['/usr/bin/osascript', '-e', osascript]
    logger.debug('Sending notification: {0}'.format(cmd))
    return call(cmd)


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
