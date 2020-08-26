import requests
import requests_random_user_agent

# import urllib.request
from bs4 import BeautifulSoup

from rich.console import Console
from rich.table import Table
from rich import box

from radyal.dict import DictBase

import json
import re


class DictionaryDict(DictBase):
    def __init__(self, word):
        url = "https://www.dictionary.com/browse/" + word
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        js = str(soup.find_all("script")[20])[31:-10].replace(
            ":undefined", ':"undefined"'
        )
        try:
            jsdata = json.loads(js)
        except ValueError:
            print("try again.")
            print(js)
            jsdata = json.loads(js)

        try:
            self.term = jsdata["searchData"]["searchTerm"]
        except:
            pass

    def show(self):
        pass
