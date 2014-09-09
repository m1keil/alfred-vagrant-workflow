from subprocess import call

# TODO: handle possible failiure of osascript

# Dict contains all Vagrant actions this workflow supports and metadata:
# ---
# 'desc': description field showed in alfred
# 'flags': additional command line flags for vagrant command
# 'state': machine state for which this action needs to be showed
# 'directory': flag to mark if action is possible on entire vagrant dir
actions = {
    'up': {
        'desc': 'Starts and provisions the vagrant environment',
        'flags': None,
        'state': ['paused', 'stopped'],
        'directory': True,
    },
    'halt': {
        'desc': 'Stops the machine',
        'flags': None,
        'state': ['running', 'paused'],
        'directory': True,
    },
    'resume': {
        'desc': 'Resume a suspended machine',
        'flags': None,
        'state': ['paused'],
        'directory': True,
    },
    'suspend': {
        'desc': 'Suspends the machine',
        'flags': None,
        'state': ['running'],
        'directory': True,
    },
    'provision': {
        'desc': 'Provisions the machine',
        'flags': None,
        'state': ['running'],
        'directory': True,
    },
    'rdp': {
        'desc': 'Connects to machine via RDP',
        'flags': None,
        'state': ['running'],
        'directory': False,
    },
    'ssh': {
        'desc': 'Connects to machine via SSH',
        'flags': None,
        'state': ['running'],
        'directory': False,
    },
    'destroy': {
        'desc': 'Stops and deletes all traces of the machine',
        'flags': '-f',
        'state': ['running', 'paused', 'stopped'],
        'directory': True,
    }
}


def send_notification(msg):
    call(['osascript', '-e',
          'tell application "Alfred 2" to run trigger "send_notification" '
          'in workflow "com.sverdlik.michael" '
          'with argument "{}"'.format(msg)])


def run_alfred(action):
    """Launch Alfred 2 via AppleScript and search for 'action'"""
    call(['osascript', '-e',
          'tell application "Alfred 2" to search "{}"'.format(action)])