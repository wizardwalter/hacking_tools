#!/usr/bin/env python

import subprocess

interface = input("interface >") # use raw_input for python2^
new_mac = input("New Mac Address >")

print("[+] Changing Mac Address for "+ interface + " to " + new_mac)

subprocess.call("ifconfig " + interface + " down", shell=True)
subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
subprocess.call("ifconfig " + interface + " up ", shell=True)