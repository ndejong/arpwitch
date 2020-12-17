
import argparse

from arpwitch import __title__ as NAME
from arpwitch import __version__ as VERSION
from arpwitch import __logger_default_level__ as LOGGER_DEFAULT_LEVEL
from arpwitch import __save_data_interval__default__ as SAVE_DATA_INTERVAL_DEFAULT
from arpwitch import __nmap__exec__ as NMAP_EXEC
from arpwitch.utils.utils import out

from arpwitch.exceptions.ArpWitchException import ArpWitchException


def arpwitch():
    from arpwitch.ArpWitch import ArpWitch

    parser = argparse.ArgumentParser(
        epilog='{} v{}'.format(NAME, VERSION),
        add_help=True,
        description="""
            A modern arpwatch replacement with JSON formatted outputs and easy options to execute commands when network 
            changes are observed.
        """,
    )

    # parser_group0
    # ===
    parser_group0 = parser.add_argument_group(title='datafile arguments')
    parser_group0.add_argument(
        '-f', '--datafile', required=False, type=str, metavar='<datafile>',
        help='The arpwitch datafile where ARP event data is stored as a JSON formatted file (REQUIRED).  The datafile '
             'is also easy to manually query and inspect with external tools such as `jq`'
    )
    parser_group0.add_argument(
        '-i', '--interval', required=False, default=SAVE_DATA_INTERVAL_DEFAULT, type=int, metavar='<seconds>',
        help='Interval seconds between writing to the datafile (DEFAULT: {})'.format(SAVE_DATA_INTERVAL_DEFAULT)
    )

    # parser_group1 - request
    # ===
    parser_group1 = parser.add_mutually_exclusive_group()
    parser_group1.add_argument(
        '-req', '--new-request', required=False, default=False, action='store_true',
        help='Select ARP request packet events that include new ip/hw addresses not yet observed (DEFAULT).'
    )

    parser_group1.add_argument(
        '-noreq', '--no-request', required=False, default=False, action='store_true',
        help='Ignore all ARP request packet events.'
    )

    parser_group1.add_argument(
        '-allreq', '--all-request', required=False, default=False, action='store_true',
        help='Select all ARP request packet events regardless if addresses have been previously observed.'
    )

    # parser_group2 - reply
    # ===
    parser_group2 = parser.add_mutually_exclusive_group()
    parser_group2.add_argument(
        '-rep', '--new-reply', required=False, default=False, action='store_true',
        help='Select only reply packet events that include new ip/hw addresses not yet observed (DEFAULT).'
    )

    parser_group2.add_argument(
        '-norep', '--no-reply', required=False, default=False, action='store_true',
        help='Ignore all ARP reply packet events.'
    )

    parser_group2.add_argument(
        '-allrep', '--all-reply', required=False, default=False, action='store_true',
        help='Select all ARP reply packet events regardless if the addresses have been previously observed.'
    )

    # parser_group3
    # ===
    parser_group3 = parser.add_argument_group(
        title='ARP event command execution arguments',
        description='The following exec command substitutions are available: '
                    '{IP}=ipv4-address, '
                    '{HW}=hardware-address, '
                    '{TS}=timestamp-utc, '
                    '{ts}=timestamp-utc-short'
    )
    parser_group3.add_argument(
        '-e', '--exec', required=False, type=str, metavar='<command>',
        help='Command line to exec on selected ARP events.  Commands are run async '
    )
    parser_group3.add_argument(
        '-n', '--nmap', required=False, default=False, action='store_true',
        help='A hard coded convenience --exec that causes nmap to be run against the IPv4 target with nmap-XML formatted '
             'output written to the current-working-directory.  This option cannot be used in conjunction with --exec.'
    )
    parser_group3.add_argument(
        '-u', '--user', required=False, type=str, metavar='<user>',
        help='User to exec commands with, if not set this will be the same user context as arpwitch.'
    )

    # parser_group3
    # ===
    parser_group4 = parser.add_argument_group(
        title='run-mode arguments',
        description='Switches that invoke run-modes other than ARP capture.'
    )
    parser_group4.add_argument(
        '-q', '--query', required=False, type=str, metavar='<address>',
        help='Query the <datafile> for an IPv4 or HW address and return results in JSON formatted output and exit.'
    )
    parser_group4.add_argument(
        '-v', '--version', required=False, default=False, action='store_true',
        help='Return the arpwitch version and exit.'
    )
    parser_group4.add_argument(
        '-w', '--witch', required=False, default=False, action='store_true',
        help='Supply one witch to <stdout> and exit.'
    )
    parser_group4.add_argument(
        '-d', '--debug', required=False, default=False, action='store_true',
        help='Debug messages to stdout.'
    )

    args = parser.parse_args()

    if args.nmap:
        exe = NMAP_EXEC
    else:
        exe = getattr(args, 'exec')

    if args.no_request:
        request_select = 'nil'
    elif args.all_request:
        request_select = 'all'
    else:
        request_select = 'new'

    if args.no_reply:
        reply_select = 'nil'
    elif args.all_reply:
        reply_select = 'all'
    else:
        reply_select = 'new'

    if args.debug:
        logger_level = 'debug'
    else:
        logger_level = LOGGER_DEFAULT_LEVEL

    try:

        arpwitch = ArpWitch(logger_level=logger_level)
        if args.version:
            out(arpwitch.do_version())
        elif args.witch:
            out(arpwitch.do_witch())
        elif args.query and args.datafile:
            out(arpwitch.do_query(datafile=args.datafile, query=args.query))
        elif args.datafile:
            try:
                arpwitch.do_sniffer(
                    datafile=args.datafile,
                    save_interval=args.interval,
                    request_select=request_select,
                    reply_select=reply_select,
                    exe=exe,
                    exec_user=args.user,
                )
            except KeyboardInterrupt:
                pass
        else:
            parser.print_help()

    except ArpWitchException as e:
        print('')
        print('{} v{}'.format(NAME, VERSION))
        print('ERROR: ', end='')
        for err in iter(e.args):
            print(err)
        print('')
        exit(9)

