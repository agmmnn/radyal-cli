from urllib.parse import quote
from bs4 import BeautifulSoup
import requests

from rich.console import Console
from rich.table import Table
from rich import box


from radyal.dict import DictBase


class LugatimDict(DictBase):
    def __init__(self, inp):
        self.inp = inp
        self.rich()

    def run(self):
        # word = input("Kelime giriniz: ")
        word = self.inp
        # start session
        mainurl = "http://lugatim.com"
        s = requests.Session()
        sr = s.get(mainurl)
        # get session cookie
        sId = sr.cookies["JSESSIONID"]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.44 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Cookie": "JSESSIONID=" + sId,
        }
        url = "http://lugatim.com/s/" + quote(word)
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "lxml")
        div = soup.find("div", {"class": "search-results-div"})
        aa = div.find_all(["h3", "p"])
        results = []

        for item in aa:
            if item.name == "h3":  # title
                title = item.text.strip()
                results.append(title)
            if item.name == "p":  # definitions
                psoup = item.find_all(["span", "br"])
                idx = 0
                defin = [""]
                for i in psoup:
                    # combine all spans until br
                    if i.name == "span":
                        defin[idx] += i.text
                    # create new item
                    if i.name == "br":
                        defin[idx] = defin[idx].strip()
                        defin.append("")
                        idx += 1
                defin[-1] = defin[-1].strip()
                if defin != "":
                    results.append(defin)

        return results

    def datalist(self):
        print(self.run())

    def plain(self):
        results = self.run()
        for i in results:
            if isinstance(i, list):
                for j in i:
                    print(j)
            else:
                print(i)

    def rich(self):
        results = self.run()
        tabl = 0
        for i in results:
            if isinstance(i, list):  # resutls
                for j in i:
                    globals()[f"table{tabl-1}"].add_row(j)
            else:  # title
                title = "Kubbealtı Lugatı" if tabl == 0 else None
                globals()[f"table{tabl}"] = Table(title=title, box=box.SQUARE)
                globals()[f"table{tabl}"].add_column(i)
                tabl += 1
        for s in range(tabl):
            Console().print(globals()[f"table{s}"])
            del globals()[f"table{s}"]
            break  # 1

    def show(self):
        pass
