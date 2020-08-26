from bs4 import BeautifulSoup
import requests

from radyal.dict import DictBase


class RandDict(DictBase):
    def __init__(self, word):
        word = word.replace(" ", "-")
        url = "https://www.bestrandoms.com/random-" + word

        r = requests.get(url)
        lst = []
        if r.status_code == 404:
            print("error")
            quit()
        else:
            soup = BeautifulSoup(r.text, "lxml").find("ul", class_="list-unstyled")
            for p in soup.find_all("p", class_="font-18"):
                lst.append(p.text)
        print(lst)

    def show(self):
        pass
