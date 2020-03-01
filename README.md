# arpwitch

[![PyPi](https://img.shields.io/pypi/v/arpwitch.svg)](https://pypi.python.org/pypi/arpwitch/)
[![Python Versions](https://img.shields.io/pypi/pyversions/arpwitch.svg)](https://github.com/verbnetworks/arpwitch/)
[![Build Status](https://api.travis-ci.org/verbnetworks/arpwitch.svg?branch=master)](https://travis-ci.org/verbnetworks/arpwitch/)
[![License](https://img.shields.io/github/license/ndejong/arpwitch.svg)](https://github.com/ndejong/arpwitch)

A modern arpwatch replacement with JSON formatted outputs and easy options to exec commands when network changes are 
observed.  Includes a hard coded convenience `--exec` that invokes nmap when new network-addresses are observed.

## Project
* https://github.com/verbnetworks/arpwitch/

## Install
#### via PyPi
```bash
pip3 install arpwitch
```

#### via Source
```bash
git clone https://github.com/verbnetworks/arpwitch
cd arpwitch
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 setup.py clean
python3 setup.py test
python3 setup.py install
```

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

**Example 1**: Use the built-in nmap `--exec` definition to nmap scan new hosts when they are first observed.  Additionally
use `--debug` logging output and pipe the JSON outputs through `jq` for pretty formatting. 
```bash
ndejong@laptop:$ sudo arpwitch --debug --nmap --datafile /tmp/arpwitch.dat | jq .
2020-02-29T21:18:28+00:00 - INFO - arpwitch v0.2.1
2020-02-29T21:18:28+00:00 - DEBUG - do_sniffer(datafile=/tmp/arpwitch.dat, save_interval=30, request_select=new, reply_select=new, exec=nmap -n -T4 -Pn -oX arpwitch-nmap-{IP}-{ts}.xml {IP}, exec_user=None)
2020-02-29T21:18:28+00:00 - DEBUG - ArpWitchDataFile.read(filename=/tmp/arpwitch.dat)
2020-02-29T21:18:28+00:00 - WARNING - ArpWitchDataFile.read() - no existing data file found
2020-02-29T21:18:28+00:00 - DEBUG - arpwitch: 0.2.2
2020-02-29T21:18:28+00:00 - DEBUG - starts: 0
2020-02-29T21:18:28+00:00 - DEBUG - ts_first: 2020-02-29T21:18:28+00:00
2020-02-29T21:18:28+00:00 - DEBUG - ts_last: 2020-02-29T21:18:28+00:00
2020-02-29T21:18:28+00:00 - DEBUG - hw_count: 0
2020-02-29T21:18:28+00:00 - DEBUG - ip_count: 0
{
  "op": "request",
  "ip": {
    "addr": "192.168.1.1",
    "new": true
  },
  "hw": {
    "addr": "cc:32:e5:00:00:00",
    "new": true
  },
  "trigger": "new_ip_request"
}
2020-02-29T21:18:32+00:00 - DEBUG - ArpWitch.async_command_exec(<exec_command>, <packet_data>, <as_user>)
2020-02-29T21:18:32+00:00 - DEBUG - ArpWitch.command_exec(command_line="nmap -n -T4 -Pn -oX arpwitch-nmap-192.168.1.1-20200229Z211832.xml 192.168.1.1")
2020-02-29T21:18:32+00:00 - DEBUG - ArpWitch.async_command_exec_threads_wait(wait_max=30)
2020-02-29T21:18:41+00:00 - DEBUG - ArpWitch.async_command_exec_threads_wait() - done
2020-02-29T21:18:59+00:00 - DEBUG - ArpWitchDataFile.write(filename=/tmp/arpwitch.dat, data=<data>)
2020-02-29T21:18:59+00:00 - DEBUG - ArpWitchDataFile.write() - datafile written

ndejong@laptop:$
ndejong@laptop:$ ls -al arpwitch-nmap-*
-rw-r--r--   1 root    root     5304 Feb 29 17:01 arpwitch-nmap-192.168.1.1-20200229Z211832.xml
```


**Example 2**: Query the datafile to extract data about the address supplied.
```bash
ndejong@laptop:$ arpwitch -f /tmp/arpwitch.dat -q 192.168.1.1
{
  "ip": {
    "192.168.1.1": {
      "cc:32:e5:00:00:00": {
        "count": 5,
        "ts_first": "2020-02-29T21:18:28+00:00",
        "ts_last": "2020-02-29T21:19:57+00:00",
        "hw_vendor": "TP-LINK TECHNOLOGIES CO.,LTD."
      }
    }
  }
}
```

## Authors
* [Nicholas de Jong](https://nicholasdejong.com)
* Managed by [Verb Networks](https://github.com/verbnetworks).

## License
BSD-2-Clause - see LICENSE file for full details.
NB: License change from Apache-2.0 to BSD-2-Clause in February 2020 at version 0.2.0
