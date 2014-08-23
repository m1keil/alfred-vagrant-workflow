from subprocess import call


def send_notification(msg):
    call(['osascript', '-e',
          'tell application "Alfred 2" to run trigger "send_notification" '
          'in workflow "com.alfredapp.sverdlik.michael" '
          'with argument "{}"'.format(msg)])


# TODO: handle possible failiure of osascript?
def run_alfred(action):
    """Launch Alfred 2 via AppleScript and search for 'action'"""
    call(['osascript', '-e',
          'tell application "Alfred 2" to search "{}"'.format(action)])