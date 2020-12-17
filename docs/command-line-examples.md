# arpwitch

## Command Line Examples

### Example 1
Use the built-in nmap `--exec` definition to nmap scan new hosts when they are first observed.  Additionally,
use `--debug` logging output and pipe the JSON outputs through `jq` for pretty formatting. 
```shell
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


### Example 2
Query the datafile to extract data about the address supplied.
```shell
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
