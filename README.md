# arpwitch

[![PyPi](https://img.shields.io/pypi/v/arpwitch.svg)](https://pypi.python.org/pypi/arpwitch/)
[![Python Versions](https://img.shields.io/pypi/pyversions/arpwitch.svg)](https://github.com/verbnetworks/arpwitch/)
[![Build Status](https://api.travis-ci.org/verbnetworks/arpwitch.svg?branch=master)](https://travis-ci.org/verbnetworks/arpwitch/)
[![Read the Docs](https://img.shields.io/readthedocs/arpwitch)](https://arpwitch.readthedocs.io)
![License](https://img.shields.io/github/license/verbnetworks/arpwitch.svg)

A modern arpwatch replacement with JSON formatted outputs and easy options to exec commands when network changes are 
observed.

Includes a convenience `--exec` definition to invoke nmap when new network-addresses are observed.

## Features
* Uses the Python `scapy` module to watch for network ARPs
* Filter ARP events based on new addresses only, or select all ARP events
* Easy to define `--exec` actions on arp related events
* Quick to use `--nmap` action to invoke nmap if installed, easy network device landscaping.
* Lookup of hardware addresses against the OUI database for manufacturer resolution.
* Logging available to STDERR
* Easy installation using PyPI `pip`
* Plenty of documentation and examples - https://arpwitch.readthedocs.io

## Installation
```shell
user@computer:~$ pip install arpwitch
```

## Command Line Usage
Use arpwitch to nmap all new hosts on the network
```shell
user@computer:~$ arpwitch --nmap --datafile /tmp/arpwitch.dat
```

## Project
* Github - [github.com/ndejong/env-alias](https://github.com/ndejong/env-alias)
* PyPI - [pypi.python.org/pypi/env-alias](https://pypi.python.org/pypi/env-alias/)
* TravisCI - [travis-ci.org/github/ndejong/env-alias](https://travis-ci.org/github/ndejong/env-alias)
* ReadTheDocs - [env-alias.readthedocs.io](https://env-alias.readthedocs.io)

---
Copyright &copy; 2020 Nicholas de Jong
