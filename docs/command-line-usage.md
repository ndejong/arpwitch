# arpwitch

## Command Line Usage
Arpwitch always requires a datafile `--datafile` to either write network-addresses observed -or- read and 
query `--query` addresses from.

Output is provided as JSON which makes it easy to chain arpwitch with other tools.

### arpwitch
```shell
usage: arpwitch [-h] [-f <datafile>] [-i <seconds>] [-req | -noreq | -allreq] [-rep | -norep | -allrep] [-e <command>] [-n] [-u <user>] [-q <address>] [-v]
                [-w] [-d]

A modern arpwatch replacement with JSON formatted outputs and easy options to 
execute commands when network changes are observed.

optional arguments:
  -h, --help            show this help message and exit
  -req, --new-request   Select ARP request packet events that include new ip/hw
                        addresses not yet observed (DEFAULT).
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
                        The arpwitch datafile where ARP event data is stored as
                        a JSON formatted file (REQUIRED). The datafile is also 
                        easy to manually query and inspect with external tools
                        such as `jq`
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
                        User to exec commands with, if not set this will be the
                        same user context as arpwitch.

run-mode arguments:
  Switches that invoke run-modes other than ARP capture.

  -q <address>, --query <address>
                        Query the <datafile> for an IPv4 or HW address and 
                        return results in JSON formatted output and exit.
  -v, --version         Return the arpwitch version and exit.
  -w, --witch           Supply one witch to <stdout> and exit.
  -d, --debug           Debug messages to stdout.

arpwitch v0.3.4
```
