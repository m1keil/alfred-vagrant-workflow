# Alfred Vagrant Workflow

This is a workflow for Alfred2 which enables quick control over [Vagrant](vagrantup.com).

## Functionality:
* Listing all existing Vagrant machines
* Filtering VMs by name, provider, vagrantfile path
* Running actions (up, halt, provision, etc) on specific machines or whole environents
* Connecting to machines via SSH or RDP

## How does it work?
Since Vagrant 1.6 it's possible to list all Vagrant running environments via `vagrant global-status` command.
My workflow utilize this command to get a list of current Vagrant state.

**Note:** Currently the implemantation of `global-status` is still a bit buggy (machine status isn't being updated in some cases) so I'm going to add few workarounds in my code.

## Screenshots:
![Screenshot](/screenshot.jpg?raw=true "Vagrant global-status")

**Note:** This is work in progress.
