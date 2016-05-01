# Dict contains all Vagrant actions this workflow supports and metadata:
# ---
# 'desc': description field showed in alfred
# 'flags': additional command line flags for vagrant command (without hyphen)
# 'state': machine state for which this action needs to be showed
# 'dir_action': flag to mark if action is possible on entire vagrant dir
# 'confirm': flag to mark if action needs to be confirmed before execution
actions = {
    'up': {
        'desc': 'Starts and provisions the vagrant environment',
        'state': ['paused', 'stopped'],
    },
    'halt': {
        'desc': 'Stops the machine',
        'state': ['running', 'paused'],
    },
    'resume': {
        'desc': 'Resume a suspended machine',
        'state': ['paused'],
    },
    'suspend': {
        'desc': 'Suspends the machine',
        'state': ['running'],
    },
    'provision': {
        'desc': 'Provisions the machine',
        'state': ['running'],
    },
    'rdp': {
        'desc': 'Connects to machine via RDP',
        'state': ['running'],
        'dir_action': False,
    },
    'ssh': {
        'desc': 'Connects to machine via SSH',
        'state': ['running'],
        'dir_action': False,
    },
    'destroy': {
        'desc': 'Stops and deletes all traces of the machine',
        'flags': ['f'],
        'state': ['running', 'paused', 'stopped'],
        'confirm': True
    }
}

# Normalization dictionary
states = {
    ('running', 'up', 'on'): 'running',
    ('paused', 'suspended', 'saved'): 'paused',
    ('stopped', 'poweroff', 'not running', 'down'): 'stopped',
    'not created': 'missing',
}

# Modifiers
modifiers = {
    'cmd': 'Run command on the whole environment'
}
