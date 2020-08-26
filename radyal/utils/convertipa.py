# IPA phonetic transcription

# available languages:
# https://tophonetics.com/
#   english(american), english(british)
# http://www.ipaturkish.com/
#   turkish

import requests
from urllib.parse import quote
from bs4 import BeautifulSoup


class IpaConvertCls:
    def __init__(self, text="hi, how are you", lng="am"):
        self.text = text
        self.lng = lng
        
        dic = {
            self.tophonetics: ["am", "br"],
            self.ipaturkish: ["tr"]}

        for i in dic:
            for j in dic[i]:
                if j == self.lng:
                    i()

    def tophonetics(self):
        url = "https://tophonetics.com/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        payload = {'submit': 'Show transcription',
                   'text_to_transcribe': self.text,
                   'output_dialect': self.lng,
                   'output_style': 'only_tr'}

        response = requests.request("POST", url, data=payload, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")
        print(soup.find("div", id="transcr_output").text)

    def ipaturkish(self):
        url = f"http://www.ipaturkish.com/translate?sentence={quote(self.text)}"
        response = requests.request("GET", url)
        soup = BeautifulSoup(response.content, "lxml")
        print(soup.find("textarea", id="translated").text)


inp = input("Enter text: ")
lng = input("convert to: ")
cnv = IpaConvertCls(inp)
