# arpwitch

A modern arpwatch tool with JSON formatted oututs and easy options to exec commands when network changes are observed.

#### datafile arguments:
**-f <datafile>**   The arpwitch datafile - all arp event data is stored in this file in a simpe JSON format making it easy to query and inspect with external tools such as jq - this argument is required.
                 
**-s <seconds>**    Seconds interval between datafile write to file - default is 30 seconds.

#### arp mapping event selection arguments:
**-a**              Select all ARP mapping events packets regardless if they have been previously observed.
                 
**-n**              Select only new ARP mapping events that have not been previously observed.

#### arp mapping event terminal output arguments:
event data is output to <stdout> as one event per line in a JSON format which facilitates easy chaining to other tools, such as jq and others.

**-i**              Output to terminal the event data for ip-address (IP) arp packet events.
                 
**-h**              Output to terminal the event data for network-hardware (HW) arp packet events.

#### arp mapping event command exec arguments:
the following exec command data substitutions are available: `{IP}=ip-address, {HW}=network-address, {hw}=network-address-short, {TS}=timestamp-utc`

**-I <command>**   Command to exec on ip-address (IP) arp packet events.

**-H <command>**   Command to exec on network-hardware (HW) arp packet events.

**-U <user>**      User to exec commands under, if not set this will be the same user that arpwitch is running.

#### optional arguments:
**-q <address>**    Query the <datafile> for an IP or HW address and return results in JSON formatted output and exit.

**-v**              Return the arpwitch version and exit.

**-w**              Supply one witch to the terminal and exit.

**-d**              Enable debug log output to <stderr> in the terminal.

#### examples:
 - example #1 : output new ip-address ARP data events
```bash
arpwitch -n -f /var/lib/arpwitch/arpwitch.dat -i
```

- example #2 : invoke nmap on new network-hardware ARP data events
```bash
arpwitch -n -f /var/lib/arpwitch/arpwitch.dat -U root \
 -H 'nmap -O -T4 -Pn -oN /var/lib/arpwitch/scans/{TS}_{hw}_{IP}.nmap {IP}'
```

- example #3 : query datafile for ARP event data about an ip-address
```bash
arpwitch -f /var/lib/arpwitch/arpwitch.dat -q 192.168.0.1
```

#### notes:
 - obtaining VLAN tags is not currently possible with scapy - https://github.com/secdev/scapy/issues/969
