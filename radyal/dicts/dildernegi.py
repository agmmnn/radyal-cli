import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

from rich.console import Console
from rich.table import Table
from rich import box

from radyal.dict import DictBase


class SomeDict(DictBase):
    def __init__(self, word):
        url = "http://www.dildernegi.org.tr/TR,274/turkce-sozluk-ara-bul.html"
        word = quote(word)

        payload = f"ctl00%24ScriptManager1=ctl00%24ScriptManager1%7Cctl00%24ContentPlaceHolder1%24hfSozluk&ctl00_wucmenu1_rdMenu_ClientState=&ctl00%24akArama%24AramaCmb=site%20i%C3%A7i%20arama&akArama%24AramaCmb_ClientState=&ctl00%24ContentPlaceHolder1%24txtSozlukText={word}&ctl00%24ContentPlaceHolder1%24rbAramaTip=2&ctl00%24ContentPlaceHolder1%24hfSozluk=Ara%3A{word}&__VIEWSTATE=%2FwEPDwUKLTc1OTM5MTU0NQ9kFgJmD2QWAgIDDxYCHgZhY3Rpb24FIi9UUiwyNzQvdHVya2NlLXNvemx1ay1hcmEtYnVsLmh0bWwWBAIHD2QWAmYPFCsAAg8WBh4EVGV4dGUeF0VuYWJsZUFqYXhTa2luUmVuZGVyaW5naB4SUmVzb2x2ZWRSZW5kZXJNb2RlCylyVGVsZXJpay5XZWIuVUkuUmVuZGVyTW9kZSwgVGVsZXJpay5XZWIuVUksIFZlcnNpb249MjAxNC4yLjYxOC40NSwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj0xMjFmYWU3ODE2NWJhM2Q0AWRkFgRmDw8WBB4IQ3NzQ2xhc3MFCXJjYkhlYWRlch4EXyFTQgICZGQCAQ8PFgQfBAUJcmNiRm9vdGVyHwUCAmRkAgkPZBYCAgQPZBYCZg9kFgYCCQ8UKwACZGRkAgsPFCsAAg8WBh4LXyFEYXRhQm91bmRnHgtfIUl0ZW1Db3VudAIBHgdWaXNpYmxlZ2RkFgJmD2QWAgIBD2QWBGYPFQINxZ9pbWFsLCAtbGkgIA5hLiBBci4gZXNrLiAgIGQCAQ8UKwACDxYEHwZnHwcCAWRkFgJmD2QWAgIBD2QWAmYPFQQADyZuYnNwOzxlbT48L2VtPgZLdXpleS4AZAIRDxYCHgVWYWx1ZWVkGAUFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYCBRVjdGwwMCR3dWNtZW51MSRyZE1lbnUFFmN0bDAwJGFrQXJhbWEkQXJhbWFDbWIFM2N0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkbHZTb3pjdWtEZXRheSRjdHJsMCRsdkFsdA8UKwAOZGRkZGRkZBQrAAFkAgFkZGRmAv%2F%2F%2F%2F8PZAUWY3RsMDAkYWtBcmFtYSRBcmFtYUNtYg8UKwACZWVkBSdjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJGx2U296Y3VrRGV0YXkPFCsADmRkZGRkZGQUKwABZAIBZGRkZgL%2F%2F%2F%2F%2FD2QFJGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkbFZzb251Y2xhcg88KwAOAwMCAwxmDQL%2F%2F%2F%2F%2FD2QD7f%2BhRJ1CjgLBfO8g6NU0qp7OCWky%2BXTfRl%2Bqni1avQ%3D%3D&__VIEWSTATEGENERATOR=46C20B46&__EVENTTARGET=ctl00%24ContentPlaceHolder1%24hfSozluk&__EVENTARGUMENT=&__EVENTVALIDATION=%2FwEdAAcNJNwVNiiXTVZPEux%2F9y7Gm1tJ99gdb3Vv2AOE%2FlGM0EQIHuFzCQJyCNKY7udvsbzyuwsCNkZ%2BGz1ZuhflD0ARH8KhsrH4%2FaAmHKuyBmQYpEOHofcJTA%2BewBjmo84IIagUZmm5s8NsINPMyLKdpEA0%2FGkjGkCzBOxBF1LLf0KAIRel9aNkpW3%2FbcVmNo%2FHJeg%3D&__ASYNCPOST=true&"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.45 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "Origin": "http://www.dildernegi.org.tr",
            "Referer": "http://www.dildernegi.org.tr/TR,274/turkce-sozluk-ara-bul.html",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": "ASP.NET_SessionId=mdn03ouqu22bhouwmktfijwz; ASP.NET_SessionId=jafmxlgpn32c0tofd1yb5d4a",
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        soup = BeautifulSoup(response.content, "lxml")
        table = soup.find("table", class_="sozcukDetay")
        aa = [
            i.text.strip()
            .replace("\t", "")
            .replace("\r", "")
            .replace("\n", "")
            .replace("\xa0", " ")
            for i in soup.findAll("td", class_="anlam")
        ]
        table = Table(box=box.SQUARE)
        for a in aa:
            print(a)
        #     table.add_row(a)

        # Console.print(table)

    def show(self):
        pass

    def render_plain(self):
        pass

    def render_list(self):
        pass

    def get_data(self):
        pass
