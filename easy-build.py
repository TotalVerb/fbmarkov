#!/usr/bin/python3

import re

with open("build/quotes.html", "r") as f, \
     open("build/out-bb.txt", "r") as g:
    code = f.read()
    result = g.read()

with open("build/quotes.html", "w") as f:
    f.write(re.sub(r"{ /\* data here \*/ }", result, code))
