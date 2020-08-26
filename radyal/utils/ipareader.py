# -*- coding: utf-8 -*-
from requests import post
import json
import base64
from playsound import playsound

# http://ipa-reader.xyz/
voicediclis = [
    "Ivy",
    "Joanna",
    "Joey",
    "Justin",
    "Kendra",
    "Kimberly",
    "Salli",
    "Nicole",
    "Russell",
    "Emma",
    "Brian",
    "Amy",
    "Raveena",
    "Geraint",
    "Ricardo",
    "Vitoria",
    "Lotte",
    "Ruben",
    "Mathieu",
    "Celine",
    "Chantal",
    "Marlene",
    "Dora",
    "Karl",
    "Carla",
    "Giorgio",
    "Mizuki",
    "Liv",
    "Maja",
    "Jan",
    "Ewa",
    "Cristiano",
    "Ines",
    "Carmen",
    "Maxim",
    "Tatyana",
    "Enrique",
    "Penelope",
    "Conchita",
    "Astrid",
    "Filiz",
    "Gwyneth",
]

voicedic = {
    "English - American": [
        "Ivy",
        "Joanna",
        "Joey",
        "Justin",
        "Kendra",
        "Kimberly",
        "Salli",
    ],
    "English - Australian": ["Nicole", "Russell"],
    "English - British": ["Emma", "Brian", "Amy"],
    "English - Indian": ["Raveena"],
    "English - Welsh": ["Geraint"],
    "Brazilian Portuguese": ["Ricardo", "Vitoria"],
    "Dutch": ["Lotte", "Ruben"],
    "French": ["Mathieu", "Celine"],
    "Canadian French": ["Chantal"],
    "German": ["Marlene"],
    "Icelandic": ["Dora", "Karl"],
    "Italian": ["Carla", "Giorgio"],
    "Japanese": ["Mizuki"],
    "Norwegian": ["Liv"],
    "Polish": ["Maja", "Jan", "Ewa"],
    "Portuquese": ["Cristiano", "Ines"],
    "Romanian": ["Carmen"],
    "Russian": ["Maxim", "Tatyana"],
    "US Spanish": ["Miguel", "Penelope"],
    "Castilian Spanish": ["Conchita"],
    "Swedish": ["Astrid"],
    "Turkish": ["Filiz"],
    "Welsh": ["Gwyneth"],
}


class IpadReaderCls:
    def __init__(self, text, voice):
        self.text = text
        self.voice = voice

    def run(self):
        url = "https://iawll6of90.execute-api.us-east-1.amazonaws.com/production"
        payload = {"text": self.text, "voice": self.voice}
        headers = {
            "authority": "iawll6of90.execute-api.us-east-1.amazonaws.com",
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.34 Safari/537.36",
            "content-type": "application/json",
            "origin": "http://ipa-reader.xyz",
        }

        r = post(url, headers=headers, data=json.dumps(payload))
        if "errorMessage" in r.text:
            print("error.")
        else:
            decode = base64.b64decode(json.loads(r.content))
            with open("temp.wav", "wb") as wavfile:
                wavfile.write(decode)

    @staticmethod
    def list():
        for i in voicedic:
            print(i + ":")
            items = []
            for j in voicedic[i]:
                items.append(j)
            print(" " + ", ".join(items))


# IpadReaderCls.list()
tatyana = IpadReaderCls("mɪˈsandrɪst", "Joanna")
tatyana.run()
