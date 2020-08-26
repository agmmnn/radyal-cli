import requests

# import urllib.request
from bs4 import BeautifulSoup

from rich.console import Console
from rich.table import Table
from rich import box

from radyal.dict import DictBase


class DifferenceDict(DictBase):
    def __init__(self, word):
        word = word.split()
        url = "https://diffsense.com/diff/" + word[0] + "/" + word[1]
        r = requests.get(url)
        soup = BeautifulSoup(
            r.text.replace("<strong>", "[cyan]").replace("</strong>", "[/cyan]"),
            "lxml",
        )
        aa = soup.main.find("div", class_="container")

        title = aa.h1.text.strip()
        p = aa.find_all("p", style="margin: 1em 0.5em 0 0.5em;")

        table = Table(title=title, show_header=False)
        for i in p:
            table.add_row(i.text.strip())
        Console().print(table)

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
