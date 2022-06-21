from bs4 import BeautifulSoup
import os
import aiohttp
import requests
import asyncio
import re
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time



scraps = [
    {"name": "mojaveofbarstove-dot-com",
     "url": "https://www.mojaveofbarstow.com/used-inventory/index.htm?start=",
     "paging": [0, 18],
        "card": {
            "container": "vehicle-card-details-container",
            "headers": [
                {"header": "Title", "tag": ""},
                {"header": "Model", "tag": ""},
                {"header": "Year", "tag": ""},
                {"header": "Engine Specification", "tag": ""},
                {"header": "Wheel Specification", "tag": ""},
                {"header": "Price", "tag": ""},
                {"header": "Stock #", "tag": ""},
                {"header": "interior color", "tag": ""},
                {"header": "exterior color", "tag": ""},
                {"header": "miles", "tag": ""},

            ]
        },
     },
]


class Dict2Obj:
    def __init__(self, json_data):
        self.convert(json_data)

    def convert(self, json_data):
        if not isinstance(json_data, dict):
            return
        for key in json_data:
            if not isinstance(json_data[key], dict):
                self.__dict__.update({key: json_data[key]})
            else:
                self.__dict__.update({ key: Dict2Obj(json_data[key])})




async def main():
    async with aiohttp.ClientSession() as session:
        # async with session.post(url=trackurl, data=r )as logresp:
        #     print(f'cookies-> {logresp.cookies}')
        # session.cookies.set(site_cookie)
        doc_coll = 0
        
        for i in scraps:
            so = Dict2Obj(i)
            print(f"Scapping from {so.name} ...")
            for pg in so.paging: 
                url = so.url + str(pg)
                print(f"Page {str(pg)}.")
                print(f"url {url}")
                if not os.path.exists(so.name):
                    os.makedirs(so.name)
                async with session.get(url=url, headers={'User-agent': 'Mozilla/9.0'}) as resp:
                    print(f"response-status: {resp.status}")
                    ress = await resp.content.read()
                    # print(type(ress))
                    if resp.status == 200:
                        soup = BeautifulSoup(ress, "html.parser")
                        print(soup.prettify())
                        all_cards = soup.find_all('div', class_="vehicle-card-details-container")
                        print(all_cards)
                        # for cd in all_cards:
                        #     # img_url = img.get('ng-src')
                        #     print(cd)
                        #     break
                        #     style = img['style']
                        #     url = re.findall('url\((.*?)\)', style)
                        #     for ur in url:
                        #         ur = ur[:-7] + 'M' + ur[-6:]
                        #         if ur[-4:] == '.jpg':
                        #             urls.append(ur)
                        # # await asyncio.sleep(1)
                        # for u in urls:
                        #     caste = u.split("/")[-6]
                        #     filename = f'{i.name}/{caste}-{str(uuid.uuid4().hex[:12])}.jpg'
                        #     with open(filename, 'wb') as fd:
                        #         async with session.get(url=u, headers={'User-agent': 'Mozilla/9.0'}) as res:
                        #             if res.status == 200:
                        #                 im_coll += 1
                        #                 chunk = await res.content.read()
                        #                 fd.write(chunk)
                        # print(f"files-collected-> {im_coll} jpgs \n")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
