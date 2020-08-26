from PIL import Image
import pytesseract
import pyperclip

# If you don't have tesseract, download and install from:
# https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

lang = input("language: ")
imgpath = './_other/ocrtr1.png'
# radyal translate @fren --ocr <imagepath> --ocrlng fra
try:
    result = pytesseract.image_to_string(Image.open(
        imgpath), lang=None if lang == "" else lang, timeout=20)
    print(result)
    print("[empty: exit, copy: copy to clipboard]")
    inp = input("choose dictionary: ")
    if inp == "copy":
        pyperclip.copy(result)
except FileNotFoundError:
    print("Tesseract installation or Image file path is not valid.")
except RuntimeError:
    print("Tesseract processing is terminated.")

