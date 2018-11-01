from operator import itemgetter
from Utilities.utility import *

tagFrequencies = dict()
wordFrequencies = dict()


def incrementWordFrequency(word):
    """
    Increment the word frequency counter
    :param word: word whose counter must be incremented
    """
    if word in wordFrequencies:
        wordFrequencies[word] += 1
    else:
        wordFrequencies[word] = 1


def incrementTagFrequency(tag):
    """
    Increment the tag frequency counter
    :param tag: tag whose counter must be incremented
    """
    if tag in tagFrequencies:
        tagFrequencies[tag] += 1
    else:
        tagFrequencies[tag] = 1


def incrementCounters(token):
    """
    Increment both word and token counters, given the token that contains them
    :param token: token containing the pair word / tag
    """
    try:
        word, tag = splitWordAndToken(token)
        incrementTagFrequency(tag)
        incrementWordFrequency(word)
    except Exception as e:
        print(e.with_traceback())
        print('error!!!: ' + token)
        exit(-1)


def transformMapInList(list, dictionary):
    """
    Converts a dictionary into a list
    :param list: list to which add all the dictionary's elements
    :param dictionary: dictionary to be converted
    """
    for element in dictionary:
        list.append((element, int(dictionary[element])))

# the dataset is read in order to increment the counters
with open('./../dataSets/final/train', 'r') as dataset:
    for line in dataset:
        # add every word to the dictionary (added only if its support reaches value 4)
        for token in line.split():
            incrementCounters(token)

wordFrequencyList = []
tagFrequencyList = []

# the frequency lists are initialized and sorted in reverse order of frequency
transformMapInList(wordFrequencyList, wordFrequencies)
wordFrequencyList = sorted(wordFrequencyList, key=itemgetter(1), reverse=True)

transformMapInList(tagFrequencyList, tagFrequencies)
tagFrequencyList = sorted(tagFrequencyList, key=itemgetter(1), reverse=True)

# the obtained results are written in their corresponding files
with open('./../results/2/mostFrequentWords', 'w') as frequentWords:
    for i in range(0, 10):
        word, frequency = wordFrequencyList[i]
        print(word + " " + str(frequency), file=frequentWords)

with open('./../results/2/POS_tagSet_train', 'w') as POStagset:
    for element in tagFrequencyList:
        print(element[0] + " " + str(element[1]), file=POStagset)

"""
with open('./../results/2/allWordsDictionary', 'w') as allFrequentWords:
    for element in wordFrequencyList:
        print(element[0], file=allFrequentWords)
"""
