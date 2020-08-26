# -*- coding: utf-8 -*-
#
#   Tureng
#   desc: Multilangual Dictionary but especially focused on turkish-english translation.
#   url: https://tureng.com/
#   command: radyal tureng <word>
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

#######
import rich
from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text


from radyal.dict import DictBase

lang = {
    "tr": "turkish-english",
    "fr": "french-english",
    "es": "spanish-english",
    "de": "german-english",
    "syn": "english-synonym",
}


class TurengWebDict(DictBase):
    def __init__(self, word):
        self.word = word
        spl = word.split(" -")[-1]
        if (spl != []) and (spl in lang):
            lng = spl
            word = word.split(" -")[0]
        else:
            lng = "tr"
        url = "https://tureng.com/{}/{}/{}".format("en", lang[lng], quote(word))
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "lxml")
        title = soup.title.text
        if lng != "syn":
            table = soup.find_all("table", {"id": "englishResultsTable"})
            result = []
            for idx, i in enumerate(table):
                tr = i.find_all("tr")
                frm_to = (
                    i.tr.find("th", class_="c2").text
                    + "->"
                    + i.tr.find("th", class_="c3").text
                )
                result.append([[frm_to]])
                for j in tr:
                    t = j.find_all("td")
                    if len(t) > 3:
                        result[idx].append(
                            [t[1].text.strip(), t[2].text.strip(), t[3].text.strip()]
                        )
            self.showrich(result, title)
        else:
            tr = soup.find("table").findChildren("tr", recursive=False)
            result = []
            for idx, i in enumerate(tr):
                result.append([i.td.text.strip()])
                intr = i.td.find_next_sibling("td").find_all("tr")
                for j in intr:
                    aa = j.find_all("a")
                    alist = []
                    for k in aa:
                        alist.append(k.text.strip())
                    result[idx].append(alist)
            self.showrichsyn(result)

    def show(self):
        pass

    def plain(self, result):
        for i in result:
            for idx, j in enumerate(i):
                if idx == 0:
                    print()
                    print("::" + j[0] + "::")
                else:
                    print(">" + j[0] + ",\t" + j[1] + ",\t" + j[2])

    def showrich(self, result, title):
        for a, i in enumerate(result):
            for idx, j in enumerate(i):
                if idx == 0:
                    globals()[f"table{a}"] = Table(
                        title=title,
                        show_header=True,
                        box=box.SQUARE,
                        show_lines=False,
                        row_styles=("medium_spring_green", "cyan"),
                    )
                    globals()[f"table{a}"].add_column("", justify="right")
                    globals()[f"table{a}"].add_column(j[0].split("->")[0])
                    globals()[f"table{a}"].add_column(j[0].split("->")[1])
                else:
                    globals()[f"table{a}"].add_row(j[0], j[1], j[2])

                    # if catg!=j[0]:
                    #     globals()[f"table{a}"].add_row(j[0]+" >",j[1], j[2])
                    # else:
                    #     globals()[f"table{a}"].add_row(">",j[1], j[2])
                    # catg=j[0]
        # print
        # Console().print(Text(title, justify="center", style="bold cyan"))
        for s in range(len(result)):
            Console().print(globals()[f"table{s}"])

    def showrichsyn(self, result):
        self.result = result
        for idx, i in enumerate(result):
            for ij, j in enumerate(i):
                if ij == 0:
                    dic = {"v.": "verb:", "n.": "name:", "adj.": "adjective:"}
                    try:
                        typ = dic[j]
                    except Exception:
                        typ = j
                    globals()[f"table{idx}"] = Table(
                        title=typ, show_header=False, box=box.SQUARE, show_lines=False
                    )
                    globals()[f"table{idx}"].add_column()
                else:
                    globals()[f"table{idx}"].add_row(str(ij) + ". " + ", ".join(j))
        # print
        for s in range(len(result)):
            Console().print(globals()[f"table{s}"])


# if __name__ == "__main__":
#     # input
#     word=input("Kelime giriniz: ")
#     if word == "":
#         word="cute"
#     TurengWebDict(word)
