from urllib.parse import quote
from bs4 import BeautifulSoup
import requests

from radyal.dict import DictBase

from rich.console import Console
from rich.table import Table
from rich import box

# https://esanlamlisi.net/es-anlamli/dost/
# http://nlpapps.cs.deu.edu.tr/esveyakin/sonuc.aspx
# http://www.es-anlam.com
# https://www.esanlamli.com/
# https://es-anlamli-kelimeler.com/karakter-e%C5%9F-anlaml%C4%B1s%C4%B1
# http://dost.anlamlisi.org/
# http://www.es-anlam.com/zit-anlam/kelime/


class EsanlamDict(DictBase):
    def __init__(self, word, style="rich"):
        self.word = word
        self.style = style
        url = "http://nlpapps.cs.deu.edu.tr/esveyakin/Default.aspx"
        payload = {
            "Button1": "Ara",
            "__EVENTVALIDATION": "/wEWAwLT2dDqCALZs8iPCQKM54rGBownJMQZ6M4erJwdMf+TowvPb3SH",
            "__VIEWSTATE": "/wEPDwUJLTQ4NDk5Njg4ZGSpJCn6mH7X2KCzYizcV9oQKEo23A==",
            "__VIEWSTATEGENERATOR": "BD2DF568",
            "word": word,
        }
        r = requests.post(url, data=payload)
        soup = BeautifulSoup(r.content, "lxml")
        self.finallist = soup.find("span", id="Label2").text.strip().split(" / ")
        self.show()

    def show(self):
        if self.style == "rich":
            self.rich()
        elif self.style == "plain":
            print(", ".join(self.finallist))
            print()
            print(", ".join(self.ayrintili()))

    def rich(self):
        print("Eş Anlam: ")
        table = Table(show_header=False, show_lines=True, box=box.SQUARE)
        if self.finallist != []:
            table.add_row(", ".join(self.finallist))
        Console().print(table)

        table2 = Table(show_header=False, show_lines=True, box=box.SQUARE)
        aylist = self.ayrintili()
        zitlist = self.zitanlam()
        if aylist != []:
            table2.add_row(", ".join(aylist))
        if zitlist != []:
            table2.add_row("zıt: " + ", ".join(zitlist))
        Console().print(table2)

    def zitanlam(self):
        url = "http://www.es-anlam.com/zit-anlam/kelime/" + quote(self.word)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        result = soup.find("h2", id="esanlamlar")
        if result == None or "BULUNAMADI !" in str(result):
            lst = []
        else:
            lst = result.strong.text.lower().split(", ")  # ", "
        return lst

    def ayrintili(self):
        from urllib.parse import quote

        try:
            url = "https://esanlamlisi.net/es-anlamli/" + quote(self.word)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "lxml")
            lis = soup.find("div", class_="list-wrapper").ul.find_all("li")
            liss = []
            for i in lis:
                liss.append(i.text.strip())
            return liss
        except Exception:
            return []
