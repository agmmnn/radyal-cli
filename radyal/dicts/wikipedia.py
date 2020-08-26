# api
# https://www.mediawiki.org/wiki/API:Get_the_contents_of_a_page
# ac
# https://en.wikipedia.org/w/api.php?action=opensearch&format=json&formatversion=2&search=google&namespace=0&limit=10

import requests
import json

# import urllib.request
# from bs4 import BeautifulSoup

from rich.console import Console
from rich.table import Table
from rich import box

from radyal.dict import DictBase


class WikiDict(DictBase):
    def __init__(self, word):
        params = {
            "action": "query",
            "prop": "extracts",
            "exlimit": "1",
            "explaintext": "1",
            "formatversion": "2",
            "titles": word,
            "format": "json",
            "exsentences": "5",
        }
        url = "https://en.wikipedia.org/w/api.php"
        s = requests.Session()
        r = s.get(url=url, params=params)
        data = json.loads(r.content)
        # print(r.url)
        print(data["query"]["pages"][0]["extract"])
        print()
        print(r.url)

    def show(self):
        pass
