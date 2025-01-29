#!/usr/bin/env python3

# iptables -I FORWARD -j NFQUEUE --queue-num 0 <- **run command to create queue which we will bind to**
# If testing locally, -I INPUT, OUTPUT in two separate commands
# iptables --flush <- **Run this when you are done, or it will continue using the queue,and you don't want that**

import netfilterqueue
import scapy.all as scapy
import re

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    packet.set_payload(bytes(packet))
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet.haslayer(scapy.TCP):
            if scapy_packet[scapy.TCP].dport == 80:
                print("[+] HTTP packet being sent...")
                modified_load = re.sub("Accept-Encoding:.*?\\r\\n", "",scapy_packet[scapy.Raw].load)
                new_packet = set_load(scapy_packet,  modified_load)
                packet.set_payload(bytes(new_packet))
            elif scapy_packet[scapy.TCP].sport == 80:
                print("[+] HTTP packet being received...")
                print(scapy_packet.show())

    packet.accept()

queue= netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()