from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
import json

from rich.console import Console
from rich import print as pprint

# https://community.fandom.com/api/v1

from radyal.dict import DictBase


class FandomDict(DictBase):
    def __init__(self, word):
        # url inter
        self.topic = word.split()[0]
        self.word = quote(" ".join(word.split()[1:]).replace(" ", "_"))

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Sec-Fetch-Mode": "navigate",
        }

        # https://dune.fandom.com/api.php?action=parse&page=god&format=json

        # https://dune.fandom.com/api.php?action=query&titles=divided%20god&format=json
        idurl = f"https://{self.topic}.fandom.com/api.php?action=query&titles={self.word}&format=json"
        r = requests.get(idurl, headers=headers)
        cdata = json.loads(r.content)
        try:
            contentid = next(iter(cdata["query"]["pages"].items()))[0]
        except Exception:
            print("error")
        print(contentid)

        if contentid == "-1":
            print("not found")
            quit()

        # https://dune.fandom.com/api/v1/Articles/AsSimpleJson?id=2916
        # https://pokemon.fandom.com/api/v1/Articles/AsSimpleJson?id=206
        url = f"https://{self.topic}.fandom.com/api/v1/Articles/AsSimpleJson?id={contentid}"
        r = requests.get(url, headers=headers)
        jsdata = json.loads(r.content)
        print(url)
        try:
            print(jsdata["sections"][0]["title"])
            for i in jsdata["sections"][0]["content"]:
                if i["type"] == "paragraph":
                    print(i["text"])
                elif i["type"] == "list":
                    raise ValueError()
        except Exception:
            try:
                redr = jsdata["sections"][0]["content"][0]["elements"][0]["text"].split(
                    "REDIRECT "
                )
                print("Redirecting to " + redr[1])
                FandomDict(self.topic, redr[1])
            except Exception:
                print("error")

        # related
        # https://dune.fandom.com/api/v1/RelatedPages/List?ids=2916&limit=3
        # search
        # https://dune.fandom.com/api/v1/Search/List?query=god&limit=25&minArticleQuality=10&batch=1&namespaces=0%2C14
        # search suggest
        # https://dune.fandom.com/api/v1/SearchSuggestions/List?query=god
        # https://community.fandom.com/api/v1/SearchSuggestions/List?query=god

        # soup = BeautifulSoup(r.content, "lxml")
        # content = soup.find(
        #     "div", id="mw-content-text").find("p", recursive=False)

        # for b in content.find_all("b"):
        #     b.replace_with("[bold]"+b.text+"[/bold]")
        # for a in content.find_all("a"):
        #     a.replace_with("[spring_green1]"+a.text+"[/spring_green1]")

        # txt = content.text.strip()
        # Console().print(txt,highlight=False)

    def show(self):
        pass


# if __name__ == "__main__":
#     go = input("Enter <topic> <term>: ").strip().split()
#     if go != [""]:  # and len(go)>1
#         FandomDict(go[0], " ".join(go[1:]))
#     else:
#         FandomDict()
