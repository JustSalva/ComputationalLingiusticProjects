from Utilities.utility import *
from operator import itemgetter

wordDictionary = dict()


def addTagToWordDictionary(token):
    """
    Inserts a word into the dictionary of words, each word entry contains a dictionary of tags,
    containing the counters of the occurrences of those tags
    :param token: token to be added to the dictionary
    """
    # I use an HashMap inside the wordDictionary to contains the counters of all tags
    word, tag = splitWordAndToken(token)
    if word in wordDictionary:
        if tag not in wordDictionary[word]:
            wordDictionary[word][tag] = 1
        else:
            wordDictionary[word][tag] += 1
    else:
        wordDictionary[word] = dict()
        wordDictionary[word][tag] = 1


def countNumberOfAssociations(listNumberOfTagsPerWord, numberOfOccurrences):
    """
    Counts how many words are associated to a certain number of POS tags and the number of occurrences of those words
    :param listNumberOfTagsPerWord: list in which elements contains the following info: (word, tagCounter, numberOfOccurrences)
    :param numberOfOccurrences: requested number of occurrences
    :return: how many words are associated to a certain number of POS tags and the number of occurrences of those words
    """
    counter = 0
    sumOfOccurrences = 0
    for element in listNumberOfTagsPerWord:
        if element[1] == numberOfOccurrences:
            counter += 1
            sumOfOccurrences += element[2]
    return counter, sumOfOccurrences


def countNumberOfAssociationsGivenLowerBound(listNumberOfTagsPerWord, numberOfOccurrences):
    """
    Counts how many words are associated to a number of POS tags that is greater or equal to a specified one
    and the number of occurrences of those words
    :param listNumberOfTagsPerWord: list in which elements contains the following info: (word, tagCounter, numberOfOccurrences)
    :param numberOfOccurrences: requested number of occurrences
    :return: how many words are associated to a number of POS tags that is greater or equal to a specified one
                and the number of occurrences of those words
    """
    counter = 0
    sumOfOccurrences = 0
    for element in listNumberOfTagsPerWord:
        if element[1] >= numberOfOccurrences:
            counter += 1
            sumOfOccurrences += element[2]
    return counter, sumOfOccurrences


def extractWordStatistics(listTagStatisticsPerWord, word):
    """
    Extracts from the given list the statistics of a single word
    :param listTagStatisticsPerWord: list containing an entry for each word, that contains a list of couples
            (tag, number of occurrences of the tag, when associated to the word)
    :param word: the word to be queried
    :return: the statistics of the requested word
    """
    for element in listTagStatisticsPerWord:
        if element[0] == word:
            return element


def extractElementWithMaxNumberOfTags(listTagStatisticsPerWord):
    """
    Queries the given list in order to extract the word with maximum number of tags
    :param listTagStatisticsPerWord: list containing an entry for each word, that contains a list of couples
            (tag, number of occurrences of the tag, when associated to the word)
    :return: the word with maximum number of tags, together with the tag's names and occurrences
    """
    maxNumberOfTags = 0
    maxElement = None
    collision = False
    for element in listTagStatisticsPerWord:
        if len(element[1]) == maxNumberOfTags:
            collision = True
        if len(element[1]) > maxNumberOfTags:
            maxNumberOfTags = len(element[1])
            maxElement = element
            collision = False

    if collision:
        print("WARNING: collision!!!")
    return maxElement, maxNumberOfTags


def initializeWordDictionary():
    """
    Loads from file the train set and saves it into the word dictionary
    (N.B a word is saved only if the min support is reached)
    """
    with open('./../dataSets/final/train', 'r') as dataset:
        for line in dataset:
            # add every word to the dictionary (added only if its support reaches value 4)
            for token in line.split():
                addTagToWordDictionary(token)


def writeResultsForBaselineTagger():
    """
    Writes the results of this script to a file
    """
    with open('./../results/3/baselineTaggerWordTagAssociations', 'w') as dataset:
        for element in listTagStatisticsPerWord:
            print(element[0] + " " + element[1][0][0], file=dataset)  # element and tag with max value


initializeWordDictionary()
listNumberOfTagsPerWord = []
listTagStatisticsPerWord = []
for element in wordDictionary:
    tagCounter = 0
    numberOfOccurrences = 0
    tempList = []
    for tag in wordDictionary[element]:
        tagCounter += 1
        numberOfOccurrences += wordDictionary[element][tag]
        tempList.append((tag, wordDictionary[element][tag]))
    listNumberOfTagsPerWord.append((element, tagCounter, numberOfOccurrences))
    tempList = sorted(tempList, key=itemgetter(1), reverse=True)
    listTagStatisticsPerWord.append((element, tempList))

writeResultsForBaselineTagger()
print(listNumberOfTagsPerWord)
print("Words associated to a single POStag (number and occurrences): " + str(
    countNumberOfAssociations(listNumberOfTagsPerWord, 1)))
print("Words associated to 2 POStags: (number and occurrences)" + str(
    countNumberOfAssociations(listNumberOfTagsPerWord, 2)))
print("Words associated to 3 POStags: (number and occurrences)" + str(
    countNumberOfAssociations(listNumberOfTagsPerWord, 3)))
print(
    "Words associated to 4 or more POStags: (number and occurrences)" + str(
        countNumberOfAssociationsGivenLowerBound(listNumberOfTagsPerWord, 4)))
print("\"start\" statistics: " + str(extractWordStatistics(listTagStatisticsPerWord, "start")))
print("Word with max number of tags: " + str(extractElementWithMaxNumberOfTags(listTagStatisticsPerWord)))
