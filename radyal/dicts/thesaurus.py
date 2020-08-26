# dict template
import requests
import requests_random_user_agent

# import urllib.request
from bs4 import BeautifulSoup

from rich.console import Console
from rich.table import Table
from rich import box

import json

from radyal.dict import DictBase


class ThesaurusDict(DictBase):
    def __init__(self, word):
        url = "https://www.thesaurus.com/browse/" + word
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        js = ""
        for i in soup.find_all("script"):
            if "window.INITIAL_STATE" in str(i):
                js = str(i)[31:-10].replace(":undefined", ':"undefined"')

        try:
            jsdata = json.loads(js)
        except ValueError:
            print("try again...")
            return

        try:
            self.term = jsdata["searchData"]["searchTerm"]
            tabs = jsdata["searchData"]["tunaApiData"]["posTabs"]
            dic = {}
            for i in tabs:
                synlis = [(i["term"], i["similarity"]) for i in i["synonyms"]]
                antlis = [(i["term"], i["similarity"]) for i in i["antonyms"]]
                dic[i["definition"]] = {
                    "pos": i["pos"],
                    "synonyms": synlis,
                    "antonyms": antlis,
                }
            self.dic = dic
            # for i in dic:
            #     print(dic[i])
            self.rich()
        except Exception:
            didy = soup.select_one('h2:contains("Did you mean")')
            print(didy.text + ".")
            print(
                "\nMore suggestions:\n"
                + ", ".join([i.text for i in didy.parent.parent.find_all("li")])
                + "."
            )

    def rich(self):
        Console().print(self.term + " - Thesaurus", justify="center")
        for i in self.dic:
            similcolors = {
                "100": ["[rgb(252,232,197)]", "[/rgb(252,232,197)]"],
                "50": ["[rgb(220,221,187)]", "[/rgb(220,221,187)]"],
                "10": ["[rgb(191,182,155)]", "[/rgb(191,182,155)]"],
                "-100": ["", ""],
                "-50": ["", ""],
                "-10": ["", ""],
            }
            table = Table(box=box.SQUARE)
            # ! TODO: must be sorted by tuple[1]
            table.add_column(
                "[cyan]" + i + "[/cyan]" + "[grey50]" + " (" + self.dic[i]["pos"] + ")"
            )
            table.add_row(
                "[cyan3]synonyms:[/cyan3] "
                + "[grey50],[/grey50] ".join(
                    [
                        similcolors[tups[1]][0]
                        + "".join(tups[0])
                        + similcolors[tups[1]][1]
                        for tups in self.dic[i]["synonyms"]
                    ]
                )
            )
            if self.dic[i]["antonyms"] != []:
                table.add_row()
                table.add_row(
                    "[cyan3]antonyms: "
                    + "[grey50],[/grey50] ".join(
                        [
                            similcolors[tups[1]][0]
                            + "".join(tups[0])
                            + similcolors[tups[1]][1]
                            for tups in self.dic[i]["antonyms"]
                        ]
                    )
                )
            Console().print(table)

    def show(self):
        pass

    def render_plain(self):
        pass

    def render_list(self):
        pass

    def get_data(self):
        pass
