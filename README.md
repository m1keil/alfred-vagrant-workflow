# VagrantUP

A workflow for [Alfred2](http://www.alfredapp.com) which provides quick control over [Vagrant](vagrantup.com).

[![Build Status](https://travis-ci.org/m1keil/alfred-vagrant-workflow.svg?branch=master)](https://travis-ci.org/m1keil/alfred-vagrant-workflow)

## Functionality
* List existing Vagrant environments
* Filter environments by name, provider, path
* Execute actions on specific VM or whole environment
* Open terminal in environment path

## Downloads & Install
You can download this workflow from [Packal](http://www.packal.org/workflow/vagrantup) or directly from [GitHub](https://github.com/m1keil/alfred-vagrant-workflow/releases).

To install workflow, simply double click the file you just downloaded. For additional instructions about installing workflows, check [Alfred's support](http://support.alfredapp.com/workflows:installing).

## Usage
#### List Vagrant environments
To list all existing Vagrant environments, use keyword `vagrant`.

#### Filtering list
You can filter the list by machine name, provider name or path. 
Filtering is done with [fuzzy search](http://en.wikipedia.org/wiki/Approximate_string_matching). Enter your filter string after `vagrant` keyword to filter the list.

**Examples:**
 - `vagrant virtualbox` - Will show only machines running under Virtualbox provider
 - `vagrant default` - Will match any machines named `default` or any machines that `default` is part of their Vagrantfile path.

#### Executing actions
To execute Vagrant commands directly from Alfred just choose the machine and press Enter. You will get a list of possible actions for the chosen machine.

Actions will vary depending on the state of the machine. So if machine is stopped, you cannot run provision for example.

It also possible to run commands on all of the machines in Vagrantfile (multi-machine environment). Just choose one machine from the environment and press enter while holding the Command key.

**NOTE:** RDP & SSH actions will open Alfred's default terminal app which is configured in Alfred's setting. 

#### Open terminal in Vagrantfile's directory
Choose machine from the list and press Enter while holding Shift key. 

**NOTE:** This will open Alfred's default terminal app which is configured in Alfred's setting. 

## Screenshots:
![Screenshot](screenshots/global-status.jpg?raw=true "Vagrant global-status")
![Screenshot](screenshots/machine-actions.jpg?raw=true "Vagrant actions")
![Screenshot](screenshots/notifications.jpg?raw=true "Notifications")

## How does it work?
Since Vagrant 1.6 it's possible to list all Vagrant running environments via `global-status` subcommand.
This workflow utilize this command to get a list of current Vagrant environments.

**Note:** ~~Currently the implementation of `global-status` is still a bit buggy (machine status isn't being updated in some cases).~~ Vagrant 1.7 seems to fix a lot of issues related to global status.
