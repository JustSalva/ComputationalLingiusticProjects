import sys

possibleTags = [line.rstrip('\n') for line in open('dataSets/Penn_TreeBank_tagSet_TAGS')]


def isInTagSet(tag):
    return tag in possibleTags


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


def handleMultipleSlashes(token):
    #print("multiple token: " + token)
    i = 0
    found = False
    while not found:
        i += 1
        split = token.split("/", i)
        temp_word = "/".join(split[:i])
        temp_tag = split[i]
        if isInTagSet(temp_tag):
            found = True
    return temp_word, temp_tag


for line in sys.stdin:
    list = []
    for token in line.split():
        list.append( checkTag(token))
    toPrint = ""
    for i in range(0, len(list)-1):
        toPrint = toPrint + list[i]+" "
    toPrint = toPrint + list[len(list)-1]
    print(toPrint)