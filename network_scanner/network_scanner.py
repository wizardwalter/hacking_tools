#!/usr/bin/env python

import scapy.all as scapy
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target",
                        help="Please provide an IP CIDR range or IP you would like to scan.")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify a target. Use --help for more information.")
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=3, verbose=True)[0]  # Increased timeout for reliability

    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}  # Fixed IP assignment
        client_list.append(client_dict)

    return client_list


def print_result(result_list):
    print("IP\t\t\tMAC Address\n-------------------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])


result_options = get_arguments()
scan_result = scan(result_options.target)
print_result(scan_result)