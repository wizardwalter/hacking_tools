#!/usr/bin/env python

import subprocess
import optparse
import re

def getArguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC Address.")
    parser.add_option("-m", "--mac", dest="new_mac", help="The MAC address value you would like to change to.")
    (options, arguments)= parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface. Use --help for more information.")
    elif not options.new_mac:
        parser.error("[-] Please specify a Mac Address. Use --help for more information.")
    return options


def changeMac(interface,new_mac):
    print("[+] Changing Mac_Address for " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read Mac Address.")




# interface = raw_input("interface >") # use raw_input for python2^
# new_mac = raw_input("New Mac Address >")
options = getArguments()
current_mac = get_current_mac(options.interface)
print("Current Mac Address" + str(current_mac))
changeMac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC Address was successfully changed to " + current_mac)
else:
    print("[-] MAC Address was not changed, please try again or run --help.")