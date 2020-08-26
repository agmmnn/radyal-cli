import json
from urllib.request import urlopen
from urllib.parse import quote

from rich.console import Console
from rich.table import Table
from rich import box

from radyal.dict import DictBase

UD_DEFID_URL = "https://api.urbandictionary.com/v0/define?defid="
UD_DEFINE_URL = "https://api.urbandictionary.com/v0/define?term="
UD_RANDOM_URL = "https://api.urbandictionary.com/v0/random"

# https://github.com/bocong/urbandictionary-py/blob/master/urbandictionary.py


class UrbanDict(DictBase):
    def __init__(self, word="numpty"):
        self.word = word
        self.run()

    def run(self):
        with urlopen(UD_DEFINE_URL + quote(self.word)) as u:
            jsdata = json.loads(u.read().decode("utf-8"))
        table = Table(
            title="Urban Dictionary: " + jsdata["list"][0]["word"],
            show_header=False,
            show_lines=True,
            box=box.SQUARE,
        )
        table.add_column()
        for idx, i in enumerate(jsdata["list"]):
            defi = i["definition"].replace("[", "").replace("]", "")
            example = (
                "\n\n"
                + "[cyan]example:[/cyan] "
                + i["example"].replace("[", "").replace("]", "")
            )
            # author = "[cyan]author:[/cyan] "+i["author"]
            table.add_row(defi + example)
            if idx == None:
                break
        self.rich = table
        Console().print(table)

    def show(self):
        pass
