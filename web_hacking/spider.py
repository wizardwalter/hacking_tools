#!/usr/bin/env python3

import requests, re

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "192.168.120.2/mutillidae/"
response = requests.get("http://" + target_url)
href_links = re.findall('(?:href=")(.*?)"',response.content.decode())
print(href_links)