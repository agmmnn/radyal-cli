# -*- coding: utf-8 -*-
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests

from rich.console import Console
from rich.table import Table
from rich import box

from radyal.dict import DictBase


class NisanyanDict(DictBase):
    def __init__(self, word):
        # word = input("Kelime giriniz: ")
        self.word = word
        url = (
            "https://www.nisanyansozluk.com/?k=" + quote(self.word) + "&view=annotated"
        )
        # s = requests.Session()
        # sr = s.get(url)
        # headers = {'User-Agent': 'Mozilla',
        #            'Cookie': 'PHPSESSID=' + sr.cookies['PHPSESSID']+"; stevarih="+sr.cookies['stevarih']}
        # print(headers)
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.Timeout:
            pass
            # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            pass
        except requests.exceptions.HTTPError as err:
            # 404
            raise SystemExit(err)
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise SystemExit(f"cannot reach nisanyansozluk.com\n{e}")

        soup = BeautifulSoup(r.content, "html5lib")
        div = soup.find("tr", {"class": "yaz hghlght"})

        if div != None:
            for br in div.find_all("br"):
                br.replace_with("\n")
            for s in div.find_all(
                "span", {"style": "display:block;padding-left:25px;font-style:italic;"}
            ):
                s.replace_with("    >" + s.text + "\n")
            self.topic = div.a.text.strip()
            resultsoup = BeautifulSoup(str(div), "lxml")
            results = resultsoup.find_all("div", {"class": "eskoken"})
            # print(word+":")
            # print(len(results))
            lst = []
            for i in results:
                if i.find("div", class_="blmbasi") is not None:
                    lst.append(
                        [
                            i.find("div", class_="blmbasi").text.strip(),
                            " "
                            + i.p.get_text()
                            .replace("[ ", "[")
                            .replace("[", "[[")
                            .replace("]", "]]")
                            .strip(),
                        ]
                    )
                else:
                    lst.append(
                        ["", i.p.text.replace("[", "[[").replace("]", "]]").strip(),]
                    )
                # print("  " + i.text)
            self.finallist = lst
            self.rich()
        else:
            print("Sonuç Bulunamadı! Yakın Kelimeler:")
            aa = BeautifulSoup(str(soup.find("tbody")), "lxml").find_all("a")
            wordlist = []
            for i in aa:
                wordlist.append(i.text)
            wordlist.insert(5, "<" + word + ">")
            print(", ".join(wordlist))
            print()

    def rich(self):
        table = Table(
            title=self.topic + " - Nişanyan Sözlük", show_header=False, box=box.SQUARE
        )
        table.add_column()
        for idx, i in enumerate(self.finallist):
            newline = "\n\n" if idx != len(self.finallist) - 1 else ""
            if i[0] != "":
                table.add_row("[grey74]" + i[0] + ":[/grey74]")
            table.add_row(i[1] + newline)
        Console().print(table)

    def show(self):
        pass

    def plain(self):
        for idx, i in enumerate(self.finallist):
            console = Console(highlight=False)
            newline = "\n\n" if idx != len(self.finallist) - 1 else ""
            if i[0] != "":
                console.print("[grey74]" + i[0] + ":[/grey74]")
            console.print(i[1] + newline)
        print()

    def datalist(self):
        print("datalist: [[topic, content], ...]\n")
        print(self.finallist)
