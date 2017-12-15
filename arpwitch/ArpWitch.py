
import os
import json
import time
import logging
import argparse
import datetime
import subprocess
from arpwitch import LoggerManager
from threading import Thread


logging.getLogger('scapy.runtime').setLevel(logging.ERROR)
from scapy.all import sniff, ARP


class ArpWitchException(Exception):
    pass


class ArpWitch:

    VERSION = '2017.2'
    SNIFF_BATCH_SIZE = 16
    SNIFF_BATCH_TIMEOUT = 2
    SAVE_DATA_INTERVAL_DEFAULT = 30

    Log = None

    meta = {}
    ip_data = {}
    hw_data = {}
    exec_subprocesses = []

    save_data_filename = None
    save_data_interval_seconds = None
    select_all_mapping_events = None
    select_new_mapping_events = None
    output_to_terminal_ip_events = None
    output_to_terminal_hw_events = None
    command_exec_ip_events = None
    command_exec_hw_events = None
    command_exec_run_as_user = None
    query_address = None
    do_version = None
    do_witch = None
    debug = None

    def __init__(self):
        self.arg_parse()
        self.Log = LoggerManager.LoggerManager().build_logger('arpwitch',
                                                              is_console_quiet=True,
                                                              is_console_debug=self.debug
                                                              )

    def arg_parse(self):
        ArgParse = argparse.ArgumentParser(
            prog='arpwitch',
            add_help=False,
            description='A modern arpwatch tool with JSON formatted oututs and easy options to exec commands when '
                        'network changes are observed.',
        )

        ArgParseGroup0 = ArgParse.add_argument_group(title='datafile arguments')
        ArgParseGroup0.add_argument(
            '-f',
            required=False,
            type=str,
            metavar='<datafile>',
            help='The arpwitch datafile - all arp event data is stored in this file in a simpe JSON format making it '
                 'easy to query and inspect with external tools such as jq - this argument is required.'
        )
        ArgParseGroup0.add_argument(
            '-s',
            required=False,
            default=self.SAVE_DATA_INTERVAL_DEFAULT,
            type=int,
            metavar='<seconds>',
            help='Seconds interval between datafile write to file - default is {} seconds.'.
                format(self.SAVE_DATA_INTERVAL_DEFAULT)
        )

        ArgParseGroup1 = ArgParse.add_argument_group(
            title='ARP mapping event selection arguments',
        )
        ArgParseGroup1.add_argument(
            '-a',
            required=False,
            default=False,
            action='store_true',
            help='Select all ARP mapping events packets regardless if they have been previously observed.'
        )
        ArgParseGroup1.add_argument(
            '-n',
            required=False,
            default=False,
            action='store_true',
            help='Select only new ARP mapping events that have not been previously observed.'
        )

        ArgParseGroup2 = ArgParse.add_argument_group(
            title='ARP mapping event terminal output arguments',
            description='event data is output to <stdout> as one event per line in a JSON format which facilitates '
                        'easy chaining to other tools, such as jq and others.'
        )
        ArgParseGroup2.add_argument(
            '-i',
            required=False,
            default=False,
            action='store_true',
            help='Output to terminal the event data for ip-address (IP) arp packet events.'
        )
        ArgParseGroup2.add_argument(
            '-h',
            required=False,
            default=False,
            action='store_true',
            help='Output to terminal the event data for network-hardware (HW) arp packet events.'
        )

        ArgParseGroup3 = ArgParse.add_argument_group(
            title='ARP mapping event command exec arguments',
            description='the following exec command data substitutions are available: '
                        '{IP}=ip-address, '
                        '{HW}=network-address, '
                        '{hw}=network-address-short, '
                        '{TS}=timestamp-utc'
        )
        ArgParseGroup3.add_argument(
            '-I',
            required=False,
            type=str,
            metavar='<command>',
            help='Command to exec on ip-address (IP) arp packet events.'
        )
        ArgParseGroup3.add_argument(
            '-H',
            required=False,
            type=str,
            metavar='<command>',
            help='Command to exec on network-hardware (HW) arp packet events.'
        )
        ArgParseGroup3.add_argument(
            '-U',
            required=False,
            type=str,
            metavar='<user>',
            help='User to exec commands under, if not set this will be the same user that arpwitch is running.'
        )

        ArgParseGroup4 = ArgParse.add_argument_group(title='optional arguments')
        ArgParseGroup4.add_argument(
            '-q',
            required=False,
            type=str,
            metavar='<address>',
            help='Query the <datafile> for an IP or HW address and return results in JSON formatted output and exit.'
        )
        ArgParseGroup4.add_argument(
            '-v',
            required=False,
            default=False,
            action='store_true',
            help='Return the arpwitch version and exit.'
        )
        ArgParseGroup4.add_argument(
            '-w',
            required=False,
            default=False,
            action='store_true',
            help='Supply one witch to the terminal and exit.'
        )
        ArgParseGroup4.add_argument(
            '-d',
            required=False,
            default=False,
            action='store_true',
            help='Enable debug log output to <stderr> in the terminal.'
        )

        args = ArgParse.parse_args()

        # datafile arguments:
        if args.f:
            self.save_data_filename = args.f
        else:
            if args.w is False and args.v is False:
                ArgParse.print_help()
                print('\n'
                      'Example #1 : output new ip-address ARP data events\n'
                      ' $ arpwitch -n -f /var/lib/arpwitch/arpwitch.dat -i'
                      '\n\n'
                      'Example #2 : invoke nmap on new network-hardware ARP data events\n'
                      ' $ arpwitch -n -f /var/lib/arpwitch/arpwitch.dat -U root -H \'nmap -O \\ \n'
                      '   -T4 -Pn -oN /var/lib/arpwitch/scans/{TS}_{hw}_{IP}.nmap {IP}\''
                      '\n\n'
                      'Example #3 : query datafile for ARP event data about an ip-address\n'
                      ' $ arpwitch -f /var/lib/arpwitch/arpwitch.dat -q 192.168.0.1'
                      '\n'
                      )
                exit(1)
        self.save_data_interval_seconds = args.s

        # ARP mapping event selection arguments:
        self.select_all_mapping_events = args.a
        self.select_new_mapping_events = args.n

        # ARP mapping event terminal output arguments:
        self.output_to_terminal_ip_events = args.i
        self.output_to_terminal_hw_events = args.h

        # ARP mapping event command exec arguments:
        self.command_exec_ip_events = args.I
        self.command_exec_hw_events = args.H
        self.command_exec_run_as_user = args.U

        # optional arguments:
        self.query_address = args.q
        self.do_version = args.v
        self.do_witch = args.w
        self.debug = args.d

    def main(self):

        if self.do_version is True:
            print('arpwitch {}'.format(self.VERSION))
            exit(0)

        if self.do_witch is True:
            print(self.witch())
            exit(0)

        self.data_file_load()

        if self.query_address is not None:
            print(json.dumps(self.do_query(self.query_address)), flush=True)
            exit(0)

        batch_has_new = False
        batch_interval_start = time.time()
        while True:
            subprocess_list_is_updated = False
            batch_timestamp = self.timestamp()
            try:
                batch_packets = self.sniff_batch_arp_packets(self.SNIFF_BATCH_SIZE, self.SNIFF_BATCH_TIMEOUT)
            except PermissionError:
                self.Log.error('arpwitch requires root privilages to sniff network interfaces!')
                exit(1)
            for packet in batch_packets:
                packet_data = self.store_arp_packet_event(packet, timestamp=batch_timestamp)
                if len(packet_data) > 0:

                    if self.select_all_mapping_events is True:
                        if self.output_to_terminal_hw_events is True:
                            print(json.dumps({'hw': packet_data['hw']}), flush=True)
                        if self.output_to_terminal_ip_events is True:
                            print(json.dumps({'ip': packet_data['ip']}), flush=True)
                        if self.command_exec_hw_events is not None:
                            subprocess_list_is_updated = True
                            self.async_command_exec(
                                command_line=self.exec_command_line_create('hw', packet_data),
                                as_user=self.command_exec_run_as_user
                            )
                        if self.command_exec_ip_events is not None:
                            subprocess_list_is_updated = True
                            self.async_command_exec(
                                command_line=self.exec_command_line_create('ip', packet_data),
                                as_user=self.command_exec_run_as_user
                            )
                    if self.select_new_mapping_events is True and packet_data['hw']['is_new'] is True:
                        if self.output_to_terminal_hw_events is True:
                            print(json.dumps({'hw': packet_data['hw']}), flush=True)
                        if self.command_exec_hw_events is not None:
                            subprocess_list_is_updated = True
                            self.async_command_exec(
                                command_line=self.exec_command_line_create('hw', packet_data),
                                as_user=self.command_exec_run_as_user
                            )
                    if self.select_new_mapping_events is True and packet_data['ip']['is_new'] is True:
                        if self.output_to_terminal_ip_events is True:
                            print(json.dumps({'ip': packet_data['ip']}), flush=True)
                        if self.command_exec_ip_events is not None:
                            subprocess_list_is_updated = True
                            self.async_command_exec(
                                command_line=self.exec_command_line_create('ip', packet_data),
                                as_user=self.command_exec_run_as_user
                            )

                    # flag batches with new data so data_file_write() can be invoked below
                    if packet_data['hw']['is_new'] is True or packet_data['ip']['is_new'] is True:
                        batch_has_new = True

            for i, sp in enumerate(self.exec_subprocesses):
                if sp.poll() is not None:
                    self.exec_subprocesses.pop(i)
                    subprocess_list_is_updated = True

            if subprocess_list_is_updated is True:
                # NB: race condition here where new processes may have already completed thus resulting in zero value
                self.Log.debug('ArpWitch.main() - currently {} active subprocesses'.format(len(self.exec_subprocesses)))

            # if self.debug is True:
            #     print('.', end='', flush=True, file=sys.stderr)

            if time.time() > batch_interval_start + self.save_data_interval_seconds:
                if batch_has_new is True:
                    self.data_file_write()
                    batch_has_new = False
                batch_interval_start = time.time()

    def store_arp_packet_event(self, packet, timestamp):
        packet_data = {}
        if packet['ip_src'] != '0.0.0.0':
            hw_address = packet['hw_src']
            ip_address = packet['ip_src']

            hw_address_is_new = False
            ip_address_is_new = False

            # ip_data
            if ip_address not in self.ip_data:
                ip_address_is_new = True
                self.ip_data[ip_address] = {}
            if hw_address not in self.ip_data[ip_address]:
                self.ip_data[ip_address][hw_address] = {
                    'count': 0,
                    'ts_first': timestamp,
                    'ts_last': None
                }
            self.ip_data[ip_address][hw_address]['count'] += 1
            self.ip_data[ip_address][hw_address]['ts_last'] = timestamp

            # hw_data
            if hw_address not in self.hw_data:
                hw_address_is_new = True
                self.hw_data[hw_address] = {}
            if ip_address not in self.hw_data[hw_address]:
                self.hw_data[hw_address][ip_address] = {
                    'count': 0,
                    'ts_first': timestamp,
                    'ts_last': None
                }
            self.hw_data[hw_address][ip_address]['count'] += 1
            self.hw_data[hw_address][ip_address]['ts_last'] = timestamp

            packet_data = {
                'ip': {ip_address: self.ip_data[ip_address], 'is_new': ip_address_is_new},
                'hw': {hw_address: self.hw_data[hw_address], 'is_new': hw_address_is_new},
            }
        return packet_data

    def exec_command_line_create(self, address_type, packet_data):
        self.Log.debug('ArpWitch.exec_command_on_new_address({}, {})'.format(address_type, '<packet_data>'))

        ip_address = None
        hw_address = None
        command_line = None

        for ip in packet_data['ip'].keys():
            if ip != 'is_new':
                ip_address = ip
        for hw in packet_data['hw'].keys():
            if hw != 'is_new':
                hw_address = hw

        if address_type == 'ip':
            command_line = self.command_exec_ip_events.format(
                IP=ip_address,
                HW=hw_address, hw=hw_address.replace(':',''),
                TS=self.timestamp())
        elif address_type == 'hw':
            command_line = self.command_exec_hw_events.format(
                IP=ip_address,
                HW=hw_address, hw=hw_address.replace(':',''),
                TS=self.timestamp())
        else:
            raise ArpWitchException('Unsupported address_type', address_type)

        return command_line

    def async_command_exec(self, command_line, as_user=None):
        self.Log.debug('ArpWitch.async_command_exec({}, {})'.format(command_line, as_user))
        thread = Thread(target=self.command_exec, args=(command_line, as_user))
        thread.start()

    def command_exec(self, command_line, as_user=None):
        self.Log.debug('ArpWitch.command_exec({}, {})'.format(command_line, as_user))
        if as_user is not None:
            command_line = 'sudo -u {} {}'.format(as_user, command_line)
        self.exec_subprocesses.append(subprocess.Popen(command_line,
                                                       shell=True,
                                                       stdout=subprocess.DEVNULL,
                                                       stderr=subprocess.STDOUT
                                                       ))

    def sniff_batch_arp_packets(self, batch_size, batch_timeout):
        packets = []
        sniffed_packets = sniff(filter='arp', count=batch_size, timeout=batch_timeout, store=1)
        for sniffed_packet in sniffed_packets:
            packet = {
                'op': None,
                'hw_src': None,
                'ip_src': None,
                'ip_dst': None
            }
            if sniffed_packet[ARP].op == 1:
                packet['op'] = 'ARP_REQ'
            elif sniffed_packet[ARP].op == 2:
                packet['op'] = 'ARP_REP'
            packet['hw_src'] = self.scrub_address('hw',sniffed_packet.sprintf('%ARP.hwsrc%'))
            packet['ip_src'] = self.scrub_address('ip',sniffed_packet.sprintf('%ARP.psrc%'))
            packet['ip_dst'] = self.scrub_address('ip',sniffed_packet.sprintf('%ARP.pdst%'))
            packets.append(packet)
        return packets

    def data_file_load(self):
        self.Log.debug('ArpWitch.data_file_load()')
        self.meta = {
            'arpwitch': self.VERSION,
            'starts': 0,
            'ts_first': self.timestamp(),
            'ts_last': None,
            'hw_count': None,
            'ip_count': None,
        }
        if os.path.isfile(self.save_data_filename):
            with open(self.save_data_filename, 'r') as f:
                data = json.load(f)
                self.meta = data['meta']
                self.meta['starts'] += 1
                self.ip_data = data['ip']
                self.hw_data = data['hw']
            self.Log.debug('ArpWitch.data_file_load() - loaded from {}'.format(self.save_data_filename))
        else:
            self.Log.warn('ArpWitch.data_file_load() - no existing data file found {}'.format(self.save_data_filename))
        for meta_field in self.meta:
            self.Log.info('{}: {}'.format(meta_field, self.meta[meta_field]))

    def data_file_write(self):
        self.Log.debug('ArpWitch.data_file_write()')
        self.meta['ts_last'] = self.timestamp()
        self.meta['hw_count'] = len(self.hw_data)
        self.meta['ip_count'] = len(self.ip_data)
        with open(self.save_data_filename, 'w') as f:
            json.dump({
                'meta': self.meta,
                'ip': self.ip_data,
                'hw': self.hw_data,
            }, f)
        self.Log.debug('ArpWitch.data_file_write() - written to {}'.format(self.save_data_filename))

    def do_query(self, address):
        address = address.replace('-',':').lower()
        if len(address.split(':')) == 6:
            if address in self.hw_data:
                return {'hw':{address: self.hw_data[address]}}
        else:
            if address in self.ip_data:
                return {'ip':{address: self.ip_data[address]}}
        return {}

    def timestamp(self):
        return datetime.datetime.utcnow().strftime("%Y%m%dZ%H%M%S")

    def scrub_address(self, address_type, address):
        if address_type == 'ip':
            return ''.join(x for x in address if x in ['.','0','1','2','3','4','5','6','7','8','9'])
        elif address_type == 'hw':
            return ''.join(x for x in address if x in [':','0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'])
        else:
            raise ArpWitchException('unsupported address_type', address_type)

    def witch(self):
        return \
            '                                                                               \n' \
            '                                                                               \n' \
            '                    %                                                          \n' \
            '                    @@            ,@@@@(@,                                     \n' \
            '                    @@@@.     @@@@@@@@@@@@@@                                   \n' \
            '                     @@@@@@@@@@@@@@@@@                                         \n' \
            '                     @@@@@@@@@@@@@@@                                           \n' \
            '                      @@@@@@@@@@@@                                             \n' \
            '                      @@@@@@@@@@@@                                             \n' \
            '                     .@@@@@@@@@@@@@@                                           \n' \
            '                      @@@@@@@@@@@@@@@@@*                                       \n' \
            '                       *  @@@@@@@@@@@@@                                        \n' \
            '                            @@@@@@@@@@@@@@@@@@@@@                              \n' \
            '                          @@@@@@@@@@@@@@@*                                     \n' \
            '                        @@@@@@@@@@@ %@@@%                                      \n' \
            '                      @@@@ @@@@@@@@@                                           \n' \
            '                    @@@@    @@@@@@@@@.                                         \n' \
            '                  @@@@/        .@@@@@@@*                                       \n' \
            '                 @@@              @@@@@@@#                                     \n' \
            '               @@& &@@@@@@@@@@@@@@@@@@@@@@@                                    \n' \
            '    @@@@@@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@                                    \n' \
            '         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                    \n' \
            '                   @@@@@@@@@@@@@@@@@@@@@@@          *@@@@@@@                   \n' \
            '                    @@@@@@@@  @@@@@@@@@@       .  #@@@@@@@@@@@                 \n' \
            '                     @@@@@@@  @        /@@@@@@@@@@@@@@@@@@@@@@@&               \n' \
            '                     .@@@(@@@               /@@@@@@@@@@@@@@@@@@@@              \n' \
            '                      &@@@ @@@                   @@@@@@@@@@@@@@@@@@            \n' \
            '                       @@@@  &@@@@@@             @@@@@@@@@@@@@@@@@@@@@@@@@@,   \n' \
            '                        @@@.    @@@@@             @@@@@@@@@@@@@@@@@@@@@@       \n' \
            '                         &@@      &@@@@             #@@# (@@@@@@@@@&           \n' \
            '                           @@@@@     @@@                                       \n' \
            '                            @@@@@                                              \n' \
            '                              @@@@                                             \n' \
            '                                @@@                                            \n' \
            '                                 %@                                            \n' \
            '                                                                               \n' \
