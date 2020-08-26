import requests

# import urllib.request
from bs4 import BeautifulSoup

from rich.console import Console
from rich.table import Table
from rich import box

from radyal.dict import DictBase

import re


class LexicoDict(DictBase):
    def __init__(self, word):
        url = "https://www.lexico.com/definition/" + word
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml",)
        for i in soup.find_all("ol", class_="subSenses"):
            i.decompose()
        for i in soup.find_all("div", class_="examples"):
            i.decompose()
        for i in soup.find_all("div", class_="synonyms"):
            i.decompose()
        body = soup.find("div", class_="entryWrapper").find_all(
            re.compile("div|section"), {"class": re.compile("entryHead|gramb")}
        )
        print(len(body))
        dic = {}
        ky = ""
        for i in body:
            if i.name == "section":
                for k in i.find_all("span", class_="ind"):
                    dic.update(ky:{k.text: []})
                    for j in i.find_all("div", class_="exg"):
                        dic[ky][k.text].append(j.text)
            else:
                dic[i.find("span", class_="hw").text] = ""
                ky = i.find("span", class_="hw").text
        print(dic)

    def show(self):
        pass

    def rich(self):
        pass

    def plain(self):
        pass

    def render_list(self):
        pass

    def get_data(self):
        pass
