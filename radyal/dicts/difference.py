import requests

# import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote
from rich.console import Console
from rich.table import Table
from rich import box

from radyal.dict import DictBase


class DifferenceDict(DictBase):
    def __init__(self, word):
        self.word = word.split(",")
        if len(self.word) == 2:
            url = (
                "https://diffsense.com/diff/"
                + quote(self.word[0].strip())
                + "/"
                + quote(self.word[1].strip())
            )
            r = requests.get(url)
            if r.status_code != 404:
                soup = BeautifulSoup(
                    r.text.replace("<strong>", "[cyan]").replace(
                        "</strong>", "[/cyan]"
                    ),
                    "lxml",
                )
                aa = soup.main.find("div", class_="container")

                title = aa.h1.text.strip()
                p = aa.find_all("p", style="margin: 1em 0.5em 0 0.5em;")

                table = Table(title=title, show_header=False, box=box.SQUARE)
                for i in p:
                    table.add_row("- " + i.text.strip())
                Console().print(table)
            else:
                Console().print("[grey50]not found.")
        else:
            Console().print(
                "[grey50]need '2' words, you given '"
                + str(len(self.word))
                + "'. exm: diff word1,word2"
            )

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
