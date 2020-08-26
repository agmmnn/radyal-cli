from urllib import parse
import urllib.request
import requests
from bs4 import BeautifulSoup
import random

from rich.console import Console
from rich.table import Table
from rich import box

# https://rich.readthedocs.io/en/latest/

from radyal.dict import DictBase

# known issues
# * "ekşişeyler -100" yönlendirmeden sonra sayfa sayısını gir


class EksiDict(DictBase):
    def __init__(self, word="metinlerarasılık", page=1):
        if " -" in word:
            self.word = word.split(" -")[0]
            self.page = word.split(" -")[1]
            if self.page == "rand":
                self.page = random.randint(1, 30)  # wip
        else:
            self.word = word
            self.page = page

        if self.word == "gündem":
            self.gundem()
        elif self.word == "debe":
            self.debe()
        else:
            self.show()

    def page_not_found(self):
        print("sayfa bulunamadı.")
        quit()

    def debe(self):
        r = requests.get(
            "https://eksisozluk.com/debe", headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(r.content, "lxml")
        topic = soup.find("div", id="content").find_all("li")
        table = Table(
            title="dünün en beğenilen entry'leri",
            show_header=False,
            box=box.SQUARE,
            row_styles=("medium_spring_green", "cyan"),
        )
        table.add_column(justify="right")
        for l in topic:
            if not l.has_attr("id"):
                table.add_row(l.span.text + "→", "https://eksisozluk.com" + l.a["href"])
        Console().print(table)

    def gundem(self):
        r = requests.get(
            "https://eksisozluk.com/basliklar/gundem",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        soup = BeautifulSoup(r.content, "lxml")
        topic = soup.find("ul", class_="topic-list partial").find_all("li")
        table = Table(
            title="gündem",
            show_header=False,
            box=box.SIMPLE,
            row_styles=("medium_spring_green", "cyan"),
        )
        table.add_column(justify="right")
        table.add_column(justify="right", style="grey50")
        table.add_column(width=35 + 2, style="grey50")
        for li in topic:
            if not li.has_attr("id"):
                table.add_row(
                    li.a.find(text=True, recursive=False),
                    li.a.small.text,
                    "https://eksisozluk.com" + li.a["href"],
                )
        Console().print(table)

    def show(self):
        self.get_content_soup()
        soup = self.soup
        lis = self.get_data()

        table = Table(
            title="[#388e3c]" + soup.h1.span.text + " - ekşi sözlük",
            show_header=False,
            box=box.ROUNDED,
            show_lines=True,
        )
        table.add_column()

        for i in lis:
            # 🌢
            if i[4] == "0":
                favcount = ""  # [#b0bec5][[·]][/#b0bec5]
            else:
                favcount = "[#b0bec5][[" + i[4] + "]][/#b0bec5] "
            eksiseyler = "[#55cbe2][[ekşişeyler]][/#55cbe2] " if i[5] != "" else ""
            date = "[#a7a090]" + i[3] + "[/#a7a090]"
            author = "[#a7a090], " + i[2] + "[/#a7a090]"
            # entry \n favcount, eksiseyler, date, author
            table.add_row(i[1] + "\n\n" + favcount + eksiseyler + date + author)
            # if not idx == len(lis)-1 : table.add_row("") # empty row

        # add page count row
        pager = soup.find("div", {"class": "pager"})
        if pager != None:
            ptext = (
                "<< sayfa ("
                + pager["data-currentpage"]
                + "/"
                + pager["data-pagecount"]
                + ") >>"
            )
            table.add_row("[grey70]" + ptext)

        # if exist print disambiguations
        dis = soup.find("div", id="disambiguations")
        if dis != None:
            print(dis.next_element.strip())
            disli = dis.find_all("li")
            dislitx = [i.text for i in disli]
            for i in dislitx:
                Console().print("[italic]" + i)
            Console().print()
        # print table
        Console().print(table)

    def render_plain(self):
        self.get_content_soup()
        lis = self.get_data()
        for i in lis:
            Console().print("- " + i[1], highlight=False)
            # print(i[3] + ", " + i[2])

        pager = self.soup.find("div", {"class": "pager"})
        if pager != None:
            ptext = (
                "<< sayfa ("
                + pager["data-currentpage"]
                + "/"
                + pager["data-pagecount"]
                + ") >>"
            )
            Console().print("[grey70]" + ptext)

    def render_list(self):
        print("datalist: [(entryid, entry, author, date, favcount, eksiseyler), ...]\n")
        print(self.get_data())

    def get_content_soup(self):
        pg = "?p=" + str(self.page)
        # redirect
        redirecturl = "https://eksisozluk.com/?q=" + parse.quote(self.word)
        try:
            url = urllib.request.urlopen(redirecturl).geturl()
        except Exception:
            print(redirecturl)
            self.page_not_found()

        # clear referrer url parameters
        finalurl = url.split("?nr")[0]
        r = requests.get(finalurl + pg, headers={"User-Agent": "Mozilla/5.0"})

        # soup, escape square brackets
        self.soup = BeautifulSoup(
            str(r.text).replace("[", "[[").replace("]", "]]"), "lxml"
        ).find("div", id="content")

    def get_data(self):
        self.get_content_soup()
        soup = self.soup
        try:
            li = soup.find("ul", {"id": "entry-item-list"}).find_all("li")
        except Exception:
            self.page_not_found()

        # entry content interpreter
        # br tags
        for br in soup.find_all("br"):
            br.replace_with("\n")
        # bkz*
        for ab in soup.find_all("sup", {"class": "ab"}):
            # https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts
            # looks not good but it is fun
            intab = "qwertyuiopasdfghjklzxcvbnmğüşıöç1234567890()-'+=?!"
            outtab = "ᑫʷᵉʳᵗʸᵘⁱᵒᵖᵃˢᵈᶠᵍʰʲᵏˡᶻˣᶜᵛᵇⁿᵐᵍᵘᶳᶥᵒᶜ¹²³⁴⁵⁶⁷⁸⁹⁰⁽⁾⁻'⁺⁼ˀꜝ"
            trantab = str.maketrans(intab, outtab)
            tx = ab.a["data-query"]
            ab.replace_with("[#53a245]*⁽" + tx.translate(trantab) + "⁾[/#53a245]")
        # hede links
        for a in soup.find_all("a", {"class": "b"}):
            a.replace_with("[#53a245]" + a.text + "[/#53a245]")
        # web links
        for a in soup.find_all("a", {"class": "url"}):
            # prevent messy urls
            tx = (
                ""
                if a.text.strip().startswith("https://")
                or a.text.strip().startswith("http://")
                else a.text
            )
            # ↪
            text = "[#53a245]" + tx + "→" + "[/#53a245]"
            href = "(" + "[steel_blue3]" + a["href"] + "[/steel_blue3]" + ")"
            a.replace_with(text + href)

        list = []
        for i in li:  # entry sections
            isoup = BeautifulSoup(str(i), "lxml")
            entry = isoup.find("div", class_="content").text.strip()
            entryid = i["data-id"]
            entryau = i["data-author"]
            entryfav = i["data-favorite-count"]
            entrydate = isoup.find("a", class_="entry-date").text
            eksiseyler = i["data-seyler-slug"]
            list.append((entryid, entry, entryau, entrydate, entryfav, eksiseyler))
        return list
