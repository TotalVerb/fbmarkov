#!/usr/bin/python3

import collections
import json
import random
import re

def make_chain():
    return collections.defaultdict(lambda: collections.defaultdict(int))

def weighted_choice(dct):
    total = 0
    for key in dct:
        total += dct[key]
    rand = random.randrange(0, total)
    now = 0
    for key in dct:
        now += dct[key]
        if rand < now:
            return key

def accumulate(chain, lst, nxt):
    chain[lst][nxt] += 1

def update(chain, sentence):
    words = sentence.split()
    lst = '[start]'
    for word in words:
        accumulate(chain, lst, word)
        lst = word
    accumulate(chain, lst, '[end]')

def make(chain):
    now = '[start]'
    while True:
        now = weighted_choice(chain[now])
        if now == '[end]':
            return
        yield now

SUBS = {
    "like emoticon": "👍",
    "smile emoticon": "😃",
    "wink emoticon": "😉",
    "frown emoticon": "☹",
    "tongue emoticon": "👅"
}

def process(line):
    """Make quick substitutions so output looks nicer."""
    for sub, to in SUBS.items():
        line = re.sub(sub, to, line)
    return line

with open('data') as file:
    lines = file.read().split('\n')

chain = {}

# Really sketchy heuristic to parse pasted FB data

# First we need to remove the basketball lines.
# They look like:
# (date)
# x scored x pointx playing basketball
BASKETBALL_REGEX = r".+? scored [0-9]+ points? in basketball."
lines = [lines[i]
         for i in range(len(lines) - 1)
         if not re.match(BASKETBALL_REGEX, lines[i+1])]

for i in range(len(lines) - 4):
    if lines[i] == lines[i+2] \
       and lines[i] and lines[i][0].isupper() \
       and lines[i+1] and '0' <= lines[i+1][0] <= '9' \
       and lines[i+3].strip() == "" \
       and (i+6 >= len(lines) or lines[i+4] != lines[i+6]):
        person = lines[i]
        if person not in chain:
            chain[person] = make_chain()
            chn = chain[person]
        else:
            chn = chain[person]
        words = process(lines[i+4])
        update(chn, words)

# Simple post processing step
# Get rid of everyone with less than 50 messages
for name in list(chain.keys()):
    if len(chain[name]) < 100:
        del chain[name]

#for i in range(5):
#    print(" ".join(make(chain)))

with open('out-bb.txt', 'w') as file:
    json.dump(chain, file, indent=2)
