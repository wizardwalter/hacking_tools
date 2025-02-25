#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "http://10.0.0.165/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url)
parsed_html = BeautifulSoup(response.content)
forms_list = parsed_html.findAll("form")
print(forms_list)