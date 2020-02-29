# arpwitch

[![PyPi](https://img.shields.io/pypi/v/arpwitch.svg)](https://pypi.python.org/pypi/arpwitch/)
[![Python Versions](https://img.shields.io/pypi/pyversions/arpwitch.svg)](https://github.com/verbnetworks/arpwitch/)
[![Build Status](https://api.travis-ci.org/verbnetworks/arpwitch.svg?branch=master)](https://travis-ci.org/verbnetworks/arpwitch/)
[![License](https://img.shields.io/github/license/ndejong/arpwitch.svg)](https://github.com/ndejong/arpwitch)

A modern arpwatch replacement with JSON formatted outputs and easy options to exec commands when network changes are 
observed.  Includes a hard coded convenience `--exec` that invokes nmap when new network-addresses are observed.

## Project
* https://github.com/verbnetworks/arpwitch/

## Versions
Legacy versions based on year-date (eg v2018.2) have been hard-deprecated in favour of a backward incompatible 
standard versioning scheme (eg v0.2.0).  With this major revision change the arguments are quite different to 
previous versions however they are based on what-works-well in the field.

## Usage
```text
usage: arpwitch [-h] [-f <datafile>] [-i <seconds>] [-req | -noreq | -allreq]
                [-rep | -norep | -allrep] [-e <command>] [-n] [-u <user>]
                [-q <address>] [-v] [-w] [-d]

arpwitch v0.2.0

optional arguments:
  -h, --help            show this help message and exit
  -req, --new-request   Select ARP request packet events that include new
                        ip/hw addresses not yet observed (DEFAULT).
  -noreq, --no-request  Ignore all ARP request packet events.
  -allreq, --all-request
                        Select all ARP request packet events regardless if
                        addresses have been previously observed.
  -rep, --new-reply     Select only reply packet events that include new ip/hw
                        addresses not yet observed (DEFAULT).
  -norep, --no-reply    Ignore all ARP reply packet events.
  -allrep, --all-reply  Select all ARP reply packet events regardless if the
                        addresses have been previously observed.

datafile arguments:
  -f <datafile>, --datafile <datafile>
                        The arpwitch datafile where ARP event data is stored
                        as a JSON formatted file (REQUIRED). The datafile is
                        also easy to manually query and inspect with external
                        tools such as `jq`
  -i <seconds>, --interval <seconds>
                        Interval seconds between writing to the datafile
                        (DEFAULT: 30)

ARP event command execution arguments:
  The following exec command substitutions are available: {IP}=ipv4-address,
  {HW}=hardware-address, {TS}=timestamp-utc, {ts}=timestamp-utc-short

  -e <command>, --exec <command>
                        Command line to exec on selected ARP events. Commands
                        are run async
  -n, --nmap            A hard coded convenience --exec that causes nmap to be
                        run against the IPv4 target with nmap-XML formatted
                        output written to the current-working-directory. This
                        option cannot be used in conjunction with --exec.
  -u <user>, --user <user>
                        User to exec commands with, if not set this will be
                        the same user context as arpwitch.

run-mode arguments:
  Switches that invoke run-modes other than ARP capture.

  -q <address>, --query <address>
                        Query the <datafile> for an IPv4 or HW address and
                        return results in JSON formatted output and exit.
  -v, --version         Return the arpwitch version and exit.
  -w, --witch           Supply one witch to <stdout> and exit.
  -d, --debug           Debug messages to stdout.

A modern arpwatch replacement with JSON formatted outputs and easy options to
execute commands when network changes are observed.
```

## Examples
```bash
ndejong@laptop:$ sudo ./bin/arpwitch -n -f /dev/null | jq .
2020-02-29T10:01:55+00:00 - INFO - arpwitch v0.2.0
2020-02-29T10:01:55+00:00 - WARNING - ArpWitchDataFile.read() - no existing data file found
{
  "op": "request",
  "ip": {
    "addr": "192.168.1.1",
    "new": true
  },
  "hw": {
    "addr": "44:03:2c:00:00:00",
    "new": true
  },
  "trigger": "new_ip_request"
}
{
  "op": "reply",
  "ip": {
    "addr": "192.168.1.100",
    "new": true
  },
  "hw": {
    "addr": "cc:32:e5:00:00:00",
    "new": true
  },
  "trigger": "new_ip_reply"
}

ndejong@laptop:$
ndejong@laptop:$ ls -al arpwitch-nmap-*
-rw-r--r--   1 root    root     5304 Feb 29 17:01 arpwitch-nmap-192.168.1.1-20200229Z100135.xml
-rw-r--r--   1 root    root     6229 Feb 29 17:01 arpwitch-nmap-192.168.1.100-20200229Z100157.xml

```

## Authors
This code is written by [Nicholas de Jong](https://github.com/ndejong) via the [Verb Networks](https://github.com/verbnetworks) lab project.

## License
MIT licensed. See LICENSE file for full details.
