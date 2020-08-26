# -*- coding: utf-8 -*-
import os
import sys
import argparse

from . import __info__ as radyal_info
from . import dicts
from radyal.loader import dictloader, dictdefault

from rich.console import Console
from rich.text import Text

import pyperclip

# parse arguments
argparser = argparse.ArgumentParser(prog="radyal-cli")
argparser.add_argument(
    "dict",
    type=str,
    nargs="*",
    help="""dictionary and/or input text. 
                       (just dict: enter iteractive mode,
                       dict+input: return output)""",
)
argparser.add_argument(
    "-v", "--version", action="version", version="%(prog)s " + radyal_info.__version__
)
argparser.add_argument("-l", "--list", action="store_true", default=False)

argparser.add_argument(
    "-cl",
    "--clean",
    action="store_true",
    default=False,
    help="start interactive mode clean.",
)

argparser.add_argument(
    "-co", "--copyoutput", action="store_true", help="copy output to clipboard."
)

# input group --paste --ocr
inparg = argparser.add_mutually_exclusive_group()
inparg.add_argument(
    "-p",
    "--paste",
    action="store_true",
    default=False,
    help="take input text from clipboard.",
)
inparg.add_argument("--ocr", action="store_true")

# style group
stylearg = argparser.add_mutually_exclusive_group()
stylearg.add_argument(
    "-s",
    "--style",
    action="store",
    metavar="",
    help="output style. (plain, rich, list)",
)
stylearg.add_argument(
    "--default", action="store", metavar="", help="set default dictionary."
)

argparser.add_argument("--ipaconvert", action="store", metavar="")
argparser.add_argument("--ipareader", action="store", metavar="")
args = argparser.parse_args()


def watchcb():
    # import subprocess
    # subprocess.call("hi", shell=True)
    global cb
    print("clipboard watching...")
    while 1:
        print(pyperclip.waitForNewPaste())
        if cb == False:
            break


def interactive():
    # ⨁ radyal-cli
    if args.clean == True:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    showlogo()
    print()
    # emojilist = [":books:", ":mag:", ":sparkles:",
    #              ":comet:", ":stars:", ":milky_way:"]

    def inpp(subtxt=" "):
        inp = (
            Console()
            .input(
                f"[on grey23][sea_green3]↪ Enter:[/sea_green3]{subtxt}"
                + "[/on grey23][grey23][/grey23] "
            )
            .strip()
            .split()
        )
        return inp

    while True:
        inp = inpp()
        if inp == []:
            continue
        if inp == ["exit"] or inp == ["quit"]:
            break
        elif inp == ["help"]:
            argparser.print_help()
        elif inp == ["cbw"]:
            import threading

            global cb
            cb = True
            threading.Thread(target=watchcb).start()
        elif inp[0] == "list":
            listkey("".join(inp[1:]))
        elif inp == ["clear"]:
            clear()
        else:
            cls = dictloader(inp[0])
            if len(inp) > 1 and cls is not None:
                cls(" ".join(inp[1:]))
            elif len(inp) > 1 and cls is None:
                cls = dictdefault()
                cls(" ".join(inp))
            elif len(inp) == 1 and cls is not None:
                # entr = "(" + inp[0] + ") " + entr
                # entr = entr + " <" + inp[0] + "> "
                Console().print(
                    f"[grey50]✓ Entered interactive {inp[0]}. Type '..' to go back."
                )
                subtxt = inp[0]
                while True:
                    inp = inpp(f" {subtxt} ")
                    if inp == [""]:
                        continue
                    if inp == ["exit"]:
                        quit()
                    if inp == [".."]:
                        Console().print(f"[grey50]..")
                        break
                    cls(" ".join(inp))
            else:
                cls = dictdefault()
                cls(" ".join(inp))
                print()


def clear():
    # win/linux
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def showlogo():
    logo = """
                  |                | 
  __|   _` |   _` |  |   |   _` |  | 
 |     (   |  (   |  |   |  (   |  | 
_|    \\__._| \\__._| \\__. | \\__._| _| 
          ____/            
    """
    row = len(logo.split("\n")) - 2
    a = int(255 / row)
    spl = logo.splitlines()
    logotext = Text()
    for i in range(row):
        r, g, b = 40, 255 - (i * a), 120
        logotext.append(spl[i + 1] + "\n", style=f"rgb({r},{g},{b})")

    width = os.get_terminal_size()[0] - 2
    console = Console(width=width)
    console.print(logotext, justify="center")
    console.print(
        # "[#2E3133]multiple online dictionaries on command-line.[#/2E3133]",
        "[i grey19]A command-line dictionary, translator, thesaurus from online sources.[/i grey19]",
        justify="center",
    )
    # dictlist
    # Console(width=width).print(
    #     "[grey19]available dicts:[/grey19] [grey23]" + ", ".join(dictlist()),
    #     justify="center",
    # )


def listkey(lngfilter=""):
    from rich import box
    from rich.table import Table
    import json

    with open(os.path.dirname(sys.argv[0]) + "/dicc.json", encoding="utf8") as f:
        lis = json.load(f)
        lis = dict(sorted(lis.items()))
    table = Table(
        title="List of Dictionaries",
        box=box.SQUARE,
        row_styles=("medium_spring_green", "cyan"),
        width=None,
    )
    table.add_column("Dictionary")
    table.add_column("Dict Keys")
    table.add_column("URL(s)")
    table.add_column("Description")
    table.add_column("Langs")
    table.add_column("+Commands")
    for i in lis:
        if (
            lngfilter in lis[i]["supported langs"]
            or "many" in lis[i]["supported langs"]
        ):  # lang filter
            table.add_row(
                i,
                str(", ".join(lis[i]["dictkeys"])),
                lis[i]["url"],
                lis[i]["description"],
                lis[i]["supported langs"],
                lis[i]["+commands"],
            )

    Console().print(table)


def showdictlist():
    print(", ".join(dictlist()))
    quit()


def dictlist():
    lis = []
    for file in os.listdir(dicts.__path__[0]):
        if not file.startswith("_") and file.endswith(".py"):
            lis.append(file[:-3])
    return lis


def main():
    if args.list:
        listkey()
        quit()

    def style():
        if args.style != None:
            print("style:", args.style)
            return args.style
        else:
            return "default"

    def outputcopy():
        co = args.copyoutput
        print("copy:", co)

    if len(args.dict) >= 2:
        # radyal <dict> <text>
        cls = dictloader(args.dict[0])
        if cls is None:
            cls = dictdefault()
            cls(" ".join(args.dict))
        else:
            cls(" ".join(args.dict[1:]))
    elif (len(args.dict) == 1) and (args.paste):
        # radyal <dict> -p
        if pyperclip.paste() != "":
            print("dict:", args.dict[0])
            print("text:", pyperclip.paste())
        else:
            print("No text copied on clipboard.")
            print("Clipboard watching...")
            wp = pyperclip.waitForPaste()
            print("Found.")
            print("text:", wp)
        outputcopy()
        style()
    elif len(args.dict) == 1 and args.paste == False:
        # radyal <inp>
        # cls = dictloader(args.dict[0])
        # if cls is None:
        #     cls = dictdefault()
        #     cls("".join(args.dict[0]))
        # else:
        #     print("run iteractive dict", args.dict[0])
        cls = dictdefault()
        cls("".join(args.dict[0]))
    else:
        # radyal
        interactive()
