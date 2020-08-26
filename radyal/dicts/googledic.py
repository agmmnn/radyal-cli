from urllib.parse import quote
from bs4 import BeautifulSoup
import requests

from rich.console import Console
from rich.table import Table
from rich import box
from time import sleep

from radyal.dict import DictBase


class GoogleDict(DictBase):
    def __init__(self, word):
        self.word = word
        sleep(1)
        # https://www.google.com/search?q=define+flow&oq=define+flow
        # show_header=False, box=box.MINIMAL_HEAVY_HEAD, show_edge =False,
        table = Table(title="Google Dictionary", box=box.SQUARE)
        table.add_column("", justify="right", style="cyan", width=10)
        aa = "[cyan]/fləʊ[/cyan]"
        table.add_column("Flow " + aa)

        table.add_row(
            "verb",
            "1. (of a liquid, gas, or electricity) move steadily and continuously in a current or stream.",
        )
        table.add_row("", '[grey54]"from here the river flows north"')
        table.add_row(
            "", "similar: [grey54]run, move, go along, course, pass, proceed, glide"
        )
        table.add_row(
            "",
            "2. go from one place to another in a steady stream, typically in large numbers.",
        )
        table.add_row("", '[grey54]"people flowed into the huge courtyard"')
        table.add_row()
        table.add_row(
            "noun",
            "1. the action or fact of moving along in a steady, continuous stream.",
        )
        table.add_row("", '[grey54]"the flow of water into the pond"')
        table.add_row("", "2. a steady, continuous stream or supply of something.")
        table.add_row("", '[grey54]"a constant flow of people"')
        table.add_row("", "similar: [grey54]run, move, course")

        console = Console()
        console.print(table)

    def show(self):
        word = self.word
        # word = input("Kelime giriniz: ")
        url = "https://www.google.com/search?hl=en&safe=off&q=define:" + quote(
            self.word
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
        }
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "lxml")
        div = soup.find("div", {"jsname": "cJAsRb"})
        print(div.text)
