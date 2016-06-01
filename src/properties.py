import os

# Dict contains all Vagrant actions this workflow supports and metadata:
# ---
# 'desc': description field showed in alfred
# 'flags': additional command line flags for vagrant command (without hyphen)
# 'state': machine state for which this action needs to be showed
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
    },
    'ssh': {
        'desc': 'Connects to machine via SSH',
        'state': ['running'],
    },
    'destroy': {
        'desc': 'Stops and deletes all traces of the machine',
        'flags': ['f'],
        'state': ['running', 'paused', 'stopped'],
        'confirm': True,
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

# Default paths used by the workflow
# - VAGRANT_HOME is the path where vagrant stores it's state.
#   By default it's ~/.vagrant.d however it's user configurable
# - PATH contains the PATH variable which will be set at subprocess call
path = {
    'INDEX': os.path.expanduser('~/.vagrant.d/data/machine-index/index'),
    'VAR': '/usr/bin:/usr/local/bin'
}
