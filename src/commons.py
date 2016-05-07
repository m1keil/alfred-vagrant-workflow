from subprocess import call


def external_trigger(name, argument):
    """
    Call to external trigger in Alfred.

    Args:
        name (str): Name of the trigger.
        argument: Argument to the trigger.
    """
    call(['/usr/bin/osascript', '-e',
          'tell application "Alfred 2" to run trigger "{0}" '
          'in workflow "com.sverdlik.michael" '
          'with argument "{1}"'.format(name, argument)])


def send_notification(msg):
    """
    Trigger notification with msg as content.

    Args:
        msg (str): Notification msg.
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
    return 'Opening workflow settings...'
