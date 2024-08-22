from dateutil.parser import parse
from datetime import datetime
from parsel import Selector
import time
import traceback
import requests
import re
import os
import pyodbc
import logging
import sqlite3
# from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import json


cookies = {
    '_fbp': 'fb.1.1724316765821.114181979122225621',
    '_gid': 'GA1.2.260848629.1724316769',
    'renderid': 'rend02',
    'WMONID': 'GkQlvE5bk8u',
    'cookie-agree': 'true',
    'JSESSIONID': 'node0nti9ptree58e1h13a81muw4zz9462198.node0',
    'M2_BYPASS_TOKEN': '6596322522499459941',
    '_gcl_au': '1.1.530493266.1724321164',
    '_ga_9PSV9LG5D2': 'GS1.1.1724321165.1.1.1724321428.57.0.0',
    '_ga': 'GA1.2.2139678927.1724321165',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    # 'content-length': '0',
    # 'cookie': '_fbp=fb.1.1724316765821.114181979122225621; _gid=GA1.2.260848629.1724316769; renderid=rend02; WMONID=GkQlvE5bk8u; cookie-agree=true; JSESSIONID=node0nti9ptree58e1h13a81muw4zz9462198.node0; M2_BYPASS_TOKEN=6596322522499459941; _gcl_au=1.1.530493266.1724321164; _ga_9PSV9LG5D2=GS1.1.1724321165.1.1.1724321428.57.0.0; _ga=GA1.2.2139678927.1724321165',
    'csrf-token': 'undefined',
    'origin': 'https://www.kia.com',
    'priority': 'u=1, i',
    'referer': 'https://www.kia.com/in/buy/find-a-dealer.html',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'x-kl-ajax-request': 'Ajax_Request',
    'x-requested-with': 'XMLHttpRequest',
}

response = requests.post('https://www.kia.com/api/kia2_in/findAdealer.getStateCity.do', cookies=cookies, headers=headers)
Main = json.loads(response.text)
# print(Main)


gujarat_key = None
ahmedabad_key = None

for state in Main['data']['stateAndCity']:
    if state['val1']['value'] == 'Gujarat':
        gujarat_key = state['val1']['key']
        for city in state['val2']:
            if city['value'] == 'Ahmedabad':
                ahmedabad_key = city['key']
                break

# print(f"Gujarat Key: {gujarat_key}")
# print(f"Ahmedabad Key: {ahmedabad_key}")

url = f'https://www.kia.com/in/buy/find-a-dealer/result.html?state={gujarat_key}&city={ahmedabad_key}'


# cookies = {
#     '_fbp': 'fb.1.1724316765821.114181979122225621',
#     '_gid': 'GA1.2.260848629.1724316769',
#     'renderid': 'rend02',
#     'WMONID': 'GkQlvE5bk8u',
#     'JSESSIONID': 'node015x59byuj1dem9qh571zuds789449156.node0',
#     'M2_BYPASS_TOKEN': '6596322522499459941',
#     '_gcl_au': '1.1.1085398407.1724316765.1569749963.1724316770.1724316782',
#     'cookie-agree': 'true',
#     '_ga': 'GA1.2.1788569748.1724316769',
#     '_ga_9PSV9LG5D2': 'GS1.1.1724316768.1.1.1724318039.60.0.0',
# }

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': '_fbp=fb.1.1724316765821.114181979122225621; _gid=GA1.2.260848629.1724316769; renderid=rend02; WMONID=GkQlvE5bk8u; JSESSIONID=node015x59byuj1dem9qh571zuds789449156.node0; M2_BYPASS_TOKEN=6596322522499459941; _gcl_au=1.1.1085398407.1724316765.1569749963.1724316770.1724316782; cookie-agree=true; _ga=GA1.2.1788569748.1724316769; _ga_9PSV9LG5D2=GS1.1.1724316768.1.1.1724318039.60.0.0',
    'csrf-token': 'undefined',
    'origin': 'https://www.kia.com',
    'priority': 'u=1, i',
    'referer': url,
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'x-kl-ajax-request': 'Ajax_Request',
    'x-requested-with': 'XMLHttpRequest',
}

data = {
    'state': {gujarat_key},
    'city': {ahmedabad_key},
    'dealerType': 'A',
}

response = requests.post(
    'https://www.kia.com/api/kia2_in/findAdealer.getDealerList.do',
    cookies=cookies,
    headers=headers,
    data=data,
)

Main = json.loads(response.text)
# print(Main)
result = []
for dealer in Main['data']:
    Dealer_Name=dealer.get('dealerName')
    store_url =  dealer.get('website')
    Email= dealer.get('email')
    Phone= dealer.get('phone1')

    address1 = dealer.get('address1')

    address2 = dealer.get('address2')
    add = address1 + ", " + address2


    google_link = f'https://www.google.com/maps/search/' + dealer.get('lat') + "," + dealer.get('lng') + "," + dealer.get('dealerName') + "," + dealer.get('address2')

    all_data = {
        "name":Dealer_Name,
        "address":add,
        "number":Phone,
        "email":Email,
        "stroe_url":store_url,
        "direction_url":google_link
    }


    result.append(all_data)

print(result)
with open('finall.json', 'a') as json_file:
    json.dump(result, json_file, indent=6)