import requests

# import urllib.request
from bs4 import BeautifulSoup

from rich.console import Console
from rich.table import Table
from rich import box

from radyal.dict import DictBase


class EtymonlineDict(DictBase):
    def __init__(self, word):
        self.word = word
        url = "https://www.etymonline.com/word/" + word
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        term = soup.find_all(class_="word__name--TTbAA")
        defin = soup.find_all(class_="word__defination--2q7ZH")

        relate = soup.find(class_="related__container--22iKI")
        if relate is not None:
            self.relate = [
                i.text for i in relate.find_all("li") if not "See all related" in i.text
            ]
        else:
            self.relate = None

        dic = {}
        for i, j in zip(term, defin):
            dic[i.text] = ""
            content = j.find_all(["p", "blockquote"])
            for idx, k in enumerate(content):
                txt = k.text.replace("[", "[[").replace("]", "]]").strip()
                if k.name == "blockquote" and k.has_attr("class"):
                    dic[i.text] += "\n" + txt
                elif k.name == "blockquote" and not k.has_attr("class"):
                    dic[i.text] += "“" + txt + "”"
                elif k.text == "" and not idx == len(content) - 1:
                    dic[i.text] += "\n\n"
                else:
                    dic[i.text] += txt
                    if (
                        not idx == len(content) - 1
                        and content[idx + 1].name == "blockquote"
                        and content[idx + 1].has_attr("class")
                    ):
                        dic[i.text] += "\n"
        self.dic = dic
        if self.dic != {}:
            self.rich()

    def show(self):
        pass

    def rich(self):
        table = Table(
            title=f"{self.word} - Etymology Dictionary",
            show_header=False,
            show_lines=True,
            box=box.SQUARE,
        )
        for i in self.dic:
            table.add_row(
                "[spring_green3]" + i + "[/spring_green3]" + "\n" + self.dic[i]
            )
        if self.relate is not None:
            table.add_row(f"[grey50]Related to {self.word}: " + ", ".join(self.relate))
        Console().print(table)

    def plain(self):
        for i in self.dic:
            print("\n" + i + "\n" + self.dic[i])
        print()

    def render_list(self):
        pass

    def get_data(self):
        pass
