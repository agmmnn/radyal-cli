from urllib import parse
import urllib.request
import requests
from bs4 import BeautifulSoup

import rich
from rich import box
from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich.panel import Panel

from radyal.dict import DictBase

# https://github.com/UlionTse/translators


class GoogleTransDict(DictBase):
    def __init__(self, inp):
        import translators as trns

        print(trns.google(inp, to_language="tr"))

    def show(self):
        pass
