from Utilities.utility import *
from operator import itemgetter

wordDictionary = dict()


def addTagToWordDictionary(token):
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
    counter = 0
    sumOfOccurrences = 0
    for element in listNumberOfTagsPerWord:
        if element[1] == numberOfOccurrences:
            counter += 1
            sumOfOccurrences += element[2]
    return counter, sumOfOccurrences


def countNumberOfAssociationsGivenLowerBound(listNumberOfTagsPerWord, numberOfOccurrences):
    counter = 0
    sumOfOccurrences = 0
    for element in listNumberOfTagsPerWord:
        if element[1] >= numberOfOccurrences:
            counter += 1
            sumOfOccurrences += element[2]
    return counter, sumOfOccurrences


def extractWordStatistics(listTagStatisticsPerWord, word):
    for element in listTagStatisticsPerWord:
        if element[0] == word:
            return element


def extractElementWithMaxNumberOfTags(listTagStatisticsPerWord):
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
    with open('./../dataSets/final/train', 'r') as dataset:
        for line in dataset:
            # add every word to the dictionary (added only if its support reaches value 4)
            for token in line.split():
                addTagToWordDictionary(token)


def writeResultsForBaselineTagger():
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
print("Words associated to a single POStag (number and occurrences): " + str(countNumberOfAssociations(listNumberOfTagsPerWord, 1)))
print("Words associated to 2 POStags: (number and occurrences)" + str(countNumberOfAssociations(listNumberOfTagsPerWord, 2)))
print("Words associated to 3 POStags: (number and occurrences)" + str(countNumberOfAssociations(listNumberOfTagsPerWord, 3)))
print(
    "Words associated to 4 or more POStags: (number and occurrences)" + str(
        countNumberOfAssociationsGivenLowerBound(listNumberOfTagsPerWord, 4)))
print("\"start\" statistics: " + str(extractWordStatistics(listTagStatisticsPerWord, "start")))
print("Word with max number of tags: " + str(extractElementWithMaxNumberOfTags(listTagStatisticsPerWord)))
