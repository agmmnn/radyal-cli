# -*- coding: utf-8 -*-
#
# site: https://www.luggat.com
# description: turkish-ottoman turkish translation.
#
import requests
from bs4 import BeautifulSoup

from radyal.dict import DictBase


class LuggatDict(DictBase):

    def __init__(self, search):
        # input
        # search = input(
        #     "Varsayılan, Osmanlıca arama (ri'mam). Türkçe arama için kelimenin sonuna 2 ekleyin. (sevmek2)"+"\nAranacak Sözcük: ")
        # print()
        # request
        url = "https://www.luggat.com/index.php"
        s_type = ('OSMANLICA ARA', 'TÜRKÇE ARA')
        data = {'Bul': s_type[1] if search[-1:] == "2" else s_type[0],
                'search': search[:-1] if search[-1:] == "2" else search}
        headers = {'Origin': 'https://www.luggat.com'}
        r = requests.post(url, headers=headers, data=data)
        # soup
        soup = BeautifulSoup(r.content, "lxml")
        info = soup.find("div", attrs={"class": "listingIntro"}).text
        result = soup.find(
            "div", attrs={"class": "col-md-6 col-sm-6 col-xs-12"})

        resultsoup = BeautifulSoup(str(result), "lxml")
        items = resultsoup.find_all(["li", "h2"])
        if len(items) == 0:
            print("Sonuç Bulunamadı! Ters Yönde Aramayı deneyin.")
        else:
            print(info)
            itemcount = 0
            for item in items:
                if item.name == "h2":
                    # itemcount+=1
                    # if itemcount==2:
                    #     break
                    print(item.text)
                if item.name == "li":
                    print(">"+item.text)

    def show(self):
        pass

