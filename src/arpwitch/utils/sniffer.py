
import logging
import os
import csv

from .utils import timestamp
from arpwitch.exceptions import ArpWitchException
from arpwitch import __sniff_batch_size__ as SNIFF_BATCH_SIZE
from arpwitch import __sniff_batch_timeout__ as SNIFF_BATCH_TIMEOUT

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import sniff, ARP


class ArpWitchSniffer:
    def sniff_arp_packet_batch(self):

        packets = []
        sniffed_packets = sniff(filter="arp", count=SNIFF_BATCH_SIZE, timeout=SNIFF_BATCH_TIMEOUT, store=1)
        for sniffed_packet in sniffed_packets:
            packet = {"op": None, "src": {}, "dst": {}}

            if sniffed_packet[ARP].op == 1:
                packet["op"] = "request"
            elif sniffed_packet[ARP].op == 2:
                packet["op"] = "reply"

            packet["src"] = {
                "hw": self.scrub_address("hw", sniffed_packet.sprintf("%ARP.hwsrc%")),
                "ip": self.scrub_address("ip", sniffed_packet.sprintf("%ARP.psrc%")),
            }
            packet["dst"] = {
                "hw": self.scrub_address("hw", sniffed_packet.sprintf("%ARP.hwdst%")),
                "ip": self.scrub_address("ip", sniffed_packet.sprintf("%ARP.pdst%")),
            }
            packets.append(packet)

        return packets

    def scrub_address(self, address_type, address):
        if address_type == "ip":
            return "".join(x for x in address if x in [".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
        elif address_type == "hw":
            return "".join(
                x
                for x in address
                if x in [":", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
            )
        else:
            raise ArpWitchException("unsupported address_type", address_type)

    def expand_packet_session_data(self, packet, session):
        oui_path = "/usr/share/ieee-data/oui.csv"

        hw_address_is_new = False
        ip_address_is_new = False

        hw_address = packet["src"]["hw"]
        ip_address = packet["src"]["ip"]

        # lookup hw_vendor name
        hw_vendor = ''.join(hw_address.split(":")[:3]).upper()

        if os.path.exists(oui_path):
            # check if the CSV file from ieee-data exists
            with open(oui_path, "r") as oui_file:
                reader = csv.DictReader(oui_file)
                for row in reader:
                    if row["Assignment"] == hw_vendor:
                        hw_vendor = row["Organization Name"]
                        break
                else:
                    hw_vendor = None  # if vendor is not found in the CSV
        else:
            from ouilookup import OuiLookup
            hw_vendor = list(OuiLookup().query(hw_address)[0].values())[0]

        # update session['ip'] data
        if ip_address not in session["ip"].keys():
            ip_address_is_new = True
            session["ip"][ip_address] = {}
        if hw_address not in session["ip"][ip_address].keys():
            session["ip"][ip_address][hw_address] = {"count": 0, "ts_first": timestamp(), "ts_last": None}
        session["ip"][ip_address][hw_address]["count"] += 1
        session["ip"][ip_address][hw_address]["ts_last"] = timestamp()
        session["ip"][ip_address][hw_address]["hw_vendor"] = hw_vendor

        # update session['hw'] data
        if hw_address not in session["hw"].keys():
            hw_address_is_new = True
            session["hw"][hw_address] = {}
        if ip_address not in session["hw"][hw_address].keys():
            session["hw"][hw_address][ip_address] = {"count": 0, "ts_first": timestamp(), "ts_last": None}
        session["hw"][hw_address][ip_address]["count"] += 1
        session["hw"][hw_address][ip_address]["ts_last"] = timestamp()
        session["hw"][hw_address][ip_address]["hw_vendor"] = hw_vendor

        packet_data = {
            "op": packet["op"],
            "ip": {"addr": ip_address, "new": ip_address_is_new},
            "hw": {"addr": hw_address, "new": hw_address_is_new},
        }

        return packet_data, session
