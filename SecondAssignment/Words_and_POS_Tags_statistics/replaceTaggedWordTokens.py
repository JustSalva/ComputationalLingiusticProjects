import sys

from Utilities.utility import *


def checkTag(token):
    word, tag = token.split("/", 1)
    if not isInTagSet(tag):
        word, tag = handleMultipleSlashes(token)
    if tag == "CD":
        word = "<NUMBER>"
    elif tag == "NNP":
        word = "<PROPER_NOUN>"
    elif tag == "NNPS":
        word = "<PROPER_NOUN_PLURAL>"
    else:
        return token

    return word + "/" + tag


for line in sys.stdin:
    list = []
    for token in line.split():
        list.append( checkTag(token))
    toPrint = ""
    for i in range(0, len(list)-1):
        toPrint = toPrint + list[i]+" "
    toPrint = toPrint + list[len(list)-1]
    print(toPrint)