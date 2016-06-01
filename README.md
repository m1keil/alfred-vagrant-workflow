# VagrantUP
[![Build Status](https://travis-ci.org/m1keil/alfred-vagrant-workflow.svg?branch=master)](https://travis-ci.org/m1keil/alfred-vagrant-workflow) [![Coverage Status](https://coveralls.io/repos/m1keil/alfred-vagrant-workflow/badge.svg)](https://coveralls.io/r/m1keil/alfred-vagrant-workflow)

A workflow for [Alfred2/3](http://www.alfredapp.com) which provides quick control over [Vagrant](vagrantup.com).

## Functionality
* List existing Vagrant environments
* Filter environments by name, path or id
* Execute actions on single machines or the whole environment

## Demo:
![Screenshot](screenshots/demo.gif?raw=true "Vagrant global-status")

## Downloads & Install
Download this workflow from [GitHub](https://github.com/m1keil/alfred-vagrant-workflow/releases) (recommended) or from [Packal](http://www.packal.org/workflow/vagrantup).

Install by double clicking the downloaded file. 

For additional instructions about installing workflows, check [Alfred's support](http://support.alfredapp.com/workflows:installing).

## Usage
#### List Vagrant environments
To list all existing Vagrant environments, use keyword `vagrant`.

#### Filtering list
You can filter the list by `machine name`,`environment path` or `machine id`.

Filtering is done with [fuzzy search](http://en.wikipedia.org/wiki/Approximate_string_matching).

#### Executing actions
To execute Vagrant commands directly from Alfred just choose the machine and press Enter (or Tab). You will get a list of possible actions for the chosen machine.

Avaliable actions will vary depending on machine's state. For example, if machine is stopped, you cannot run provision.

It also possible to run commands on [multi machine Vagrantfile](https://docs.vagrantup.com/v2/multi-machine/index.html). Choose any action and hold the Command key while pressing enter.

**NOTE:** RDP & SSH actions will use Alfred's default terminal app which is configured in Alfred's setting.

## Settings
Because environment variables are not propagated into OS X applications, the workflow comes with its own defaults:

- **Vagrant Index**: the file where Vagrant stores it's internal state (`~/.vagrant.d/data/machine-index/index` by default)
- **PATH**: the PATH variable specifies a set of directories where executable programs are located. It is where `vagrant` or `VBoxManage` executables are expected to be found (`/usr/bin:/usr/local/bin` by default)

If your setup is different, you should adjust these settings in the config file.

To open the config file - open Alfred and type `vagrant workflow:settings`.

In case you wish to reset setting to default type `vagrant workflow:delsettings`.

## Requirements
1. Python 2.7 (Installed in OS X by default since 10.7)
2. Alfred 2/3
3. Vagrant (Preferebly 1.7+)

## Troubleshooting
In case something isn't right, check the logs by typing `vagrant workflow:openlog`.
I assume most of the issues will occur due to path variables.

Feel free to submit bug reports in the issue tracker, please include as much details as possible with logs.

## Special Thanks
Special thanks to **Deanishe** and his awesome [alfred-workflow](http://www.deanishe.net/alfred-workflow/index.html) library which does most of the heavy lifting here.
