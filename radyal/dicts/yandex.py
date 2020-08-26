from yandex_translate import YandexTranslate

from radyal.dict import DictBase


class YandexDict(DictBase):
    def __init__(self, word):
        translate = YandexTranslate(
            "trnsl.1.1.20200427T091614Z.9a305423c24aa8fd.9c4ba4ec17f852e7eea7f04f596b7af0c872f5c7"
        )
        # print('Languages:', translate.langs)
        # print('Translate directions:', translate.directions)
        # det = translate.detect(word)  # Привет, мир!
        print(translate.translate(word, "tr")["text"][0])  # or just 'en'

    def show(self):
        pass
