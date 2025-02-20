#!/usr/bin/env python3

import requests

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "192.168.120.2/mutillidae/"
with open("./dir_names.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        # test_url = word + "." + target_url
        test_url = target_url + "/" + word
        response = request(test_url)
        if response:
            print("[+] Discovered subdomain --> " + test_url)