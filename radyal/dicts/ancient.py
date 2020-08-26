# dict template

import requests

# import urllib.request
from bs4 import BeautifulSoup

from rich.console import Console
from rich.table import Table
from rich import box

from radyal.dict import DictBase

# https://www.ancient.eu/Apis/
# https://www.ancient.eu/Second_Dynasty_of_Egypt/
# random
# https://www.ancient.eu/ajax/ajax_random_article.php?types=1,2,6,9


class SomeDict(DictBase):
    def __init__(self, word):
        self.word = word.replace(" ", "_")
        url = "https://www.ancient.eu/" + self.word
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "lxml")
            article = soup.find("article")
            if article is not None:
                title = soup.find("h1").text
                table = Table(
                    title=title + " - Ancient History Encyclopedia", box=box.SQUARE
                )
                table.add_column(title)
                table.add_row(soup.p.text)
                Console().print(table)
            else:
                lis = []
                for i in soup.find_all("div", class_="ci_header type__1"):
                    lis.append(i.h3.text)
                print("Disambiguation: " + ", ".join(lis))
        elif r.status_code == 404:
            url = "https://www.ancient.eu/search/?q=" + self.word
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "lxml")
            # lis = []
            # for i in soup.find_all("div", class_="ci_header type__1"):
            #     lis.append(i.h3.text)
            try:
                print(
                    "Search results: "
                    + (
                        ", ".join(
                            str(i.h3.text)
                            for i in soup.find_all("div", class_="ci_header type__1")
                        )
                    )
                    + "\n\n"
                    "Related tags: "
                    + (
                        ", ".join(
                            str(i.text.strip())
                            for i in soup.find("div", id="tags").find_all("label")
                        )
                    )
                )
            except Exception:
                print("not found.")

    def show(self):
        pass

    def render_plain(self):
        pass

    def render_list(self):
        pass

    def get_data(self):
        pass
