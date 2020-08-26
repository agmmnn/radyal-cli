# -*- coding: utf-8 -*-
import json
import requests

from rich.console import Console
from rich.table import Table
from rich import box

from radyal.dict import DictBase


class TurengDict(DictBase):
    def __init__(self, word):
        url = "http://ws.tureng.com/TurengSearchServiceV4.svc/Search"
        payload = {"Term": word}
        headers = {"Content-Type": "application/json", "Origin": "tureng.com"}
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        j = json.loads(response.text, encoding="utf8")
        rslt = j["MobileResult"]["Results"]

        with open("tureng.json", "w", encoding="utf8") as f:
            json.dump(j, f, indent=4)

        if rslt != None:
            global dic
            dic = {}
            for i in rslt:
                catg = i["CategoryEN"][:-9]
                if catg not in dic:
                    dic[catg] = [i["Term"]]
                    # dic[catg] = [(i["Term"], i["TypeEN"])]
                else:
                    dic[catg].append(i["Term"])
            self.rich()
        else:
            print("Not found. Try these:")
            print(", ".join(j["MobileResult"]["Suggestions"]))

    @staticmethod
    def plain():
        console = Console(record=True)
        for i in dic:
            console.print(
                "[steel_blue]" + i + ":[/steel_blue]\n  " + ", ".join(dic[i]),
                highlight=False,
            )
        print()
        # import pyperclip
        # pyperclip.copy(console.export_text())

    @staticmethod
    def rich():
        table = Table(
            show_header=False,
            box=box.SQUARE,
            show_lines=False,
            row_styles=("cyan2", ""),
        )
        table.add_column(justify="right")
        table.add_column()
        for i in dic:
            table.add_row(i, ", ".join(dic[i]))
        Console().print(table)

    def show(self):
        pass
