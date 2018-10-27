import sys

possibleTags = [line.rstrip('\n') for line in open('./../dataSets/Penn_TreeBank_tagSet_TAGS')]
dictionary = dict()
wordFrequencies = dict()


def isInTagSet(tag):
    return tag in possibleTags


def addToDictionary(token):
    try:
        word, tag = token.split("/", 1)
        if not isInTagSet(tag):
            word, tag = handleMultipleSlashes(token)
        if tag in dictionary:
            if word in wordFrequencies:
                wordFrequencies[word] += 1

                if wordFrequencies[word] == 4:
                    temp_list = dictionary[tag]
                    temp_list.append(word)
                    dictionary[tag] = temp_list
            else:
                wordFrequencies[word] = 1
        else:
            temp_list = []
            dictionary[tag] = temp_list
            if word in wordFrequencies:
                wordFrequencies[word] += 1
                if wordFrequencies[word] == 4:
                    temp_list = dictionary[tag]
                    temp_list.append(word)
                    dictionary[tag] = temp_list
            else:
                wordFrequencies[word] = 1
    except Exception as e:
        print(e.with_traceback())
        print("error!!!: " + token)
        exit(-1)


def handleMultipleSlashes(token):
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

fileScope = "train"
with open('./../dataSets/dumas_' + fileScope + '_replaced', 'r') as dataset:
    with open('./../dataSets/' + fileScope + '_dictionary', 'w') as tagDictionary:

            for line in dataset:
                # add every word to the dictionary (added only if its support reaches value 4)
                for token in line.split():
                    addToDictionary(token)
                toPrint = ""

            for key in dictionary:
                toPrint = ""
                for word in dictionary[key]:
                    toPrint = toPrint + word + "(" + str(wordFrequencies[word]) + ")" + " "

                toPrint = key + ":" + toPrint
                #print(toPrint)
                print(toPrint, file = tagDictionary)

with open('./../dataSets/' + fileScope + '_frequencies', 'w') as frequencies:
    lexiconSize = 0
    for word in wordFrequencies:
        print(word + " " + str(wordFrequencies[word]), file = frequencies)
        if wordFrequencies[word] >= 4:
            lexiconSize += 1

print("lexicon size = " + str(lexiconSize))
