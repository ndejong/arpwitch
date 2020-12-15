
import time

from arpwitch import __title__ as NAME
from arpwitch import __version__ as VERSION
from arpwitch import __save_data_interval__default__ as SAVE_DATA_INTERVAL_DEFAULT
from arpwitch.utils.utils import out
from arpwitch.utils.utils import timestamp
from arpwitch.utils import logger
from arpwitch.utils.witch import ArpWitchWitch
from arpwitch.utils.datafile import ArpWitchDataFile
from arpwitch.utils.sniffer import ArpWitchSniffer
from arpwitch.utils.exe import ArpWitchExec
from arpwitch.exceptions.ArpWitchException import ArpWitchException


class ArpWitch:

    def __init__(self, logger_level='warning'):
        logger.init(name=NAME, level=logger_level)
        logger.info('{} v{}'.format(NAME, VERSION))

    def do_version(self):
        logger.debug('do_version()')
        return {'version': VERSION}

    def do_witch(self):
        logger.debug('do_witch()')
        return ArpWitchWitch().witch()

    def do_query(self, datafile, query):
        logger.debug('do_query()')

        data = ArpWitchDataFile().read(filename=datafile)
        address = query.replace('-', ':').lower()

        if len(address.split(':')) == 6:
            if address in data['hw']:
                return {'hw': {address: data['hw'][address]}}
        else:
            if address in data['ip'].keys():
                return {'ip': {address: data['ip'][address]}}
        return {}

    def do_sniffer(self, datafile, save_interval=SAVE_DATA_INTERVAL_DEFAULT, request_select='new', reply_select='new', exe=None, exec_user=None):
        logger.debug('do_sniffer(datafile={}, save_interval={}, request_select={}, reply_select={}, exec={}, exec_user={})'.format(datafile, save_interval, request_select, reply_select, exe, exec_user))

        session = ArpWitchDataFile.read(filename=datafile)
        session['meta']['starts'] += 1
        session_save_time = time.time()
        session_data_count = session['meta']['hw_count'] + session['meta']['ip_count']

        while True:

            batch_packets = []

            try:
                batch_packets = ArpWitchSniffer().sniff_arp_packet_batch()
            except PermissionError:
                logger.critical('{} requires root privileges to sniff network interfaces!'.format(NAME))
                exit(1)

            arpwitchexec = ArpWitchExec()

            for packet in batch_packets:
                packet_data, session = ArpWitchSniffer().expand_packet_session_data(packet, session)

                trigger = None
                if packet_data['op'] == 'request':
                    if request_select == 'all':
                        trigger = 'all_request'
                    elif request_select == 'new' and packet_data['ip']['new'] is True:
                        trigger = 'new_ip_request'
                    elif request_select == 'new' and packet_data['hw']['new'] is True:
                        trigger = 'new_hw_request'
                    else:
                        pass
                elif packet_data['op'] == 'reply':
                    if reply_select == 'all':
                        trigger = 'all_reply'
                    elif reply_select == 'new' and packet_data['ip']['new'] is True:
                        trigger = 'new_ip_reply'
                    elif reply_select == 'new' and packet_data['hw']['new'] is True:
                        trigger = 'new_hw_reply'
                    else:
                        pass
                else:
                    raise ArpWitchException('Unexpected packet_data[op]', packet_data['op'])

                if trigger is not None:
                    out({**packet_data, **{'trigger': trigger}}, indent=0, flush=True)
                    arpwitchexec.async_command_exec_thread(exe, packet_data, as_user=exec_user)

            if len(arpwitchexec.subprocess_list) > 0:
                arpwitchexec.async_command_exec_threads_wait()

            del arpwitchexec

            session['meta']['ts_last'] = timestamp()
            session['meta']['hw_count'] = len(session['hw'])
            session['meta']['ip_count'] = len(session['ip'])

            if time.time() > session_save_time + save_interval and (session_data_count != session['meta']['hw_count'] + session['meta']['ip_count']):
                ArpWitchDataFile.write(filename=datafile, data=session)
                session_save_time = time.time()
                session_data_count = session['meta']['hw_count'] + session['meta']['ip_count']
