from pathlib import Path
from importlib import import_module
from inspect import getmembers
import inspect

import json
import os
import sys

from radyal.dict import DictBase

path = os.path.dirname(sys.argv[0])


def setdefault(defa="trans"):
    print(path)

    with open(path + "/dicc.json") as f:
        a = json.load(f)

    print(a.keys())
    a["default"] = defa
    print(a)
    with open(path + "/dicc.json", "w") as f:
        json.dump(a, f, indent=2)


def getdicjs():
    with open(path + "/dicc.json", encoding="utf8") as f:
        a = json.load(f)
    # for i in a:
    #     if i != "default":
    #         print(a[i]["dictkeys"])
    #         print(i)
    return a


def getsetjs():
    with open(path + "/settings.json", encoding="utf8") as f:
        a = json.load(f)
    return a


def dictloader(dictkey):
    from importlib import import_module
    from radyal import dicts

    # from pathlib import Path
    # print("\nkey:"+dictkey)
    a = getdicjs()
    for i in a:
        if i == "default":
            continue
        if dictkey in a[i]["dictkeys"]:
            # for f in Path(dicts.__file__).parent.glob("*.py"):
            # if not f.stem.startswith("_") and f.stem == a[i]:
            mdl = import_module("radyal.dicts.{}".format(i))
            for n, d in getmembers(mdl):
                if (
                    n.endswith("Dict")
                    and issubclass(d, DictBase)
                    and not (d is DictBase)
                ):
                    # print(f"{n}, {d}")
                    del import_module
                    return d
    # else:
    #     mdl = import_module("radyal.dicts.{}".format(a["default"]))
    #     for n, d in getmembers(mdl):
    #         if n.endswith("Dict"):
    #             print(f"{n}, {d}")
    #             del import_module
    #             print("default")
    #             return d


def dictdefault():
    from importlib import import_module

    defmdl = getsetjs()["defaults"]["dict"]
    mdl = import_module("radyal.dicts.{}".format(defmdl))
    for n, d in getmembers(mdl):
        if n.endswith("Dict"):
            del import_module
            return d
