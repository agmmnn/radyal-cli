# dict template

import requests

# import urllib.request
# from bs4 import BeautifulSoup

from rich.console import Console
from rich.table import Table
from rich import box

from radyal.dict import DictBase


class SomeDict(DictBase):
    def __init__(self, word):
        pass

    def show(self):
        pass

    def render_plain(self):
        pass

    def render_list(self):
        pass

    def get_data(self):
        pass
