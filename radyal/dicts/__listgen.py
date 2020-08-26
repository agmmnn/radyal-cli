# *dev script, not part of radyal* it generates a json file
# that lists the names of the py files(with dictkeys) in the current folder

import os
import json

files = [f for f in os.listdir(".") if os.path.isfile(f)]

aa = {}
for f in files:
    if not f.startswith("_") and not f.endswith("json"):
        key = f.split(".")[0]
        aa[key] = {"dictkeys": [key]}

with open("__list.json", "w") as f:
    json.dump(aa, f, indent=2, sort_keys=True)
