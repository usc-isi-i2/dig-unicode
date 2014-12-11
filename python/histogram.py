import sys
import os

import simplejson as json
from collections import Counter

def isAscii(c):
    try:
        return ord(c) <= 127
    except:
        return False

for line in sys.stdin:
    try:
        (url, jrep) = line.split('\t')
        d = json.loads(jrep)

        body = d["hasBodyPart"]["text"]
        bodyChars = []
        bodyHisto = Counter()
        for c in body:
            if not isAscii(c):
                bodyHisto[c] += 1
                bodyChars.append(c)
        d["hasBodyPart"]["unicodeHistogram"] = bodyHisto
        d["hasBodyPart"]["unicodeText"] = " ".join(bodyChars)

        title = d["hasTitlePart"]["text"]
        titleChars = []
        titleHisto = Counter()
        for c in title:
            if not isAscii(c):
                titleHisto[c] += 1
                titleChars.append(c)
        d["hasTitlePart"]["unicodeHistogram"] = titleHisto
        d["hasTitlePart"]["unicodeText"] = " ".join(titleChars)

        json.dump(d, sys.stdout, indent=4, sort_keys=True)
    except ValueError as e:
        pass
