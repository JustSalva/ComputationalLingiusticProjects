from operator import itemgetter
from Utilities.utility import *

tagFrequencies = dict()
wordFrequencies = dict()


def incrementWordFrequency(word):
    if word in wordFrequencies:
        wordFrequencies[word] += 1
    else:
        wordFrequencies[word] = 1


def incrementTagFrequency(tag):
    if tag in tagFrequencies:
        tagFrequencies[tag] += 1
    else:
        tagFrequencies[tag] = 1


def incrementCounters(token):
    try:
        word, tag = splitWordAndToken(token)
        incrementTagFrequency(tag)
        incrementWordFrequency(word)
    except Exception as e:
        print(e.with_traceback())
        print('error!!!: ' + token)
        exit(-1)


def transformMapInList(list, dictionary):
    for element in dictionary:
        list.append((element, int(dictionary[element])))


with open('./../dataSets/train', 'r') as dataset:
    for line in dataset:
        # add every word to the dictionary (added only if its support reaches value 4)
        for token in line.split():
            incrementCounters(token)

wordFrequencyList = []
tagFrequencyList = []

transformMapInList(wordFrequencyList, wordFrequencies)
wordFrequencyList = sorted(wordFrequencyList, key=itemgetter(1), reverse=True)

transformMapInList(tagFrequencyList, tagFrequencies)
tagFrequencyList = sorted(tagFrequencyList, key=itemgetter(1), reverse=True)

with open('./../results/mostFrequentWords', 'w') as frequentWords:
    for i in range(0, 10):
        word, frequency = wordFrequencyList[i]
        print(word + " " + str(frequency), file=frequentWords)

with open('./../results/POS_tagSet_train', 'w') as POStagset:
    for element in tagFrequencyList:
        print(element[0] + " " + str(element[1]), file=POStagset)

"""
frequencyList = []
with open('./../dataSets/train_frequencies', 'r') as dataset:
    for line in dataset:
        word, frequency = line.split(' ', 1)
        frequencyList.append((word, int(frequency)))

frequencyList = sorted(frequencyList, key=itemgetter(1), reverse=True)
print(frequencyList)
with open('./../dataSets/mostFrequentWords', 'w') as frequentWords:
    for i in range(0, 10):
        word, frequency = frequencyList[i]
        print(word + " " + str(frequency), file=frequentWords)
"""
