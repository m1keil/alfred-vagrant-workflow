from subprocess import call

actions = {
    'up': {
        'desc': 'Starts and provisions the vagrant environment',
        'flags': None,
        'state': ['paused', 'stopped']
    },
    'halt': {
        'desc': 'Stops the machine',
        'flags': None,
        'state': ['running', 'paused']
    },
    'resume': {
        'desc': 'Resume a suspended machine',
        'flags': None,
        'state': ['paused']
    },
    'suspend': {
        'desc': 'Suspends the machine',
        'flags': None,
        'state': ['running']
    },
    'provision': {
        'desc': 'Provisions the machine',
        'flags': None,
        'state': ['running']
    },
    'rdp': {
        'desc': 'Connects to machine via RDP',
        'flags': None,
        'state': ['running']
    },
    'ssh': {
        'desc': 'Connects to machine via SSH',
        'flags': None,
        'state': ['running']
    },
    'destroy': {
        'desc': 'Stops and deletes all traces of the machine',
        'flags': '-f',
        'state': ['running', 'paused', 'stopped']
    }
}


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