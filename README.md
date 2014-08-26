# VagrantUP

This is a workflow for [Alfred2](http://www.alfredapp.com) which provides quick control for [Vagrant](vagrantup.com).

## Functionality:
* List all existing Vagrant environments
* Filtering environments by name, provider, path
* Execute actions (up, halt, provision, etc) on specific virtual machines or whole environment

## Downloads
You can download this workflow from [Packal](http://www.packal.org/workflow/vagrantup) or directly from [GitHub](https://github.com/m1keil/alfred-vagrant-workflow/raw/master/bundle/vagrantup.alfredworkflow)

## Screenshots:
![Screenshot](screenshots/global-status.jpg?raw=true "Vagrant global-status")
![Screenshot](screenshots/machine-actions.jpg?raw=true "Vagrant actions")
![Screenshot](screenshots/notifications.jpg?raw=true "Notifications")

## Todo:
* Add SSH/RDP quick connect
* Handle Vagrant suspend bug (prune cache on list)
* Add tests

## How does it work?
Since Vagrant 1.6 it's possible to list all Vagrant running environments via `global-status` sub-command.
This workflow utilize this command to get a list of current Vagrant environments.

**Note:** Currently the implemantation of `global-status` is still a bit buggy (machine status isn't being updated in some cases).
