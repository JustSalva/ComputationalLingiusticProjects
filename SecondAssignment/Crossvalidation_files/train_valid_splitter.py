from Utilities.utility import *
from operator import itemgetter


""""THIS PART COMES FROM AMBIGUITY_STATISTICS"""


wordDictionary0 = dict()
wordDictionary1 = dict()
wordDictionary2 = dict()
wordDictionary3 = dict()
testSet0 = []
testSet1 = []
testSet2 = []
testSet3 = []



def addTagToWordDictionary1(token):
    """
    Inserts a word into the dictionary of words, each word entry contains a dictionary of tags,
    containing the counters of the occurrences of those tags
    :param token: token to be added to the dictionary
    """
    # I use an HashMap inside the wordDictionary to contains the counters of all tags
    word, tag = splitWordAndToken(token)
    if word in wordDictionary1:
        if tag not in wordDictionary1[word]:
            wordDictionary1[word][tag] = 1
        else:
            wordDictionary1[word][tag] += 1
    else:
        wordDictionary1[word] = dict()
        wordDictionary1[word][tag] = 1


def addTagToWordDictionary2(token):
    """
    Inserts a word into the dictionary of words, each word entry contains a dictionary of tags,
    containing the counters of the occurrences of those tags
    :param token: token to be added to the dictionary
    """
    # I use an HashMap inside the wordDictionary to contains the counters of all tags
    word, tag = splitWordAndToken(token)
    if word in wordDictionary2:
        if tag not in wordDictionary2[word]:
            wordDictionary2[word][tag] = 1
        else:
            wordDictionary2[word][tag] += 1
    else:
        wordDictionary2[word] = dict()
        wordDictionary2[word][tag] = 1

def addTagToWordDictionary3(token):
    """
    Inserts a word into the dictionary of words, each word entry contains a dictionary of tags,
    containing the counters of the occurrences of those tags
    :param token: token to be added to the dictionary
    """
    # I use an HashMap inside the wordDictionary to contains the counters of all tags
    word, tag = splitWordAndToken(token)
    if word in wordDictionary3:
        if tag not in wordDictionary3[word]:
            wordDictionary3[word][tag] = 1
        else:
            wordDictionary3[word][tag] += 1
    else:
        wordDictionary3[word] = dict()
        wordDictionary3[word][tag] = 1

def addTagToWordDictionary0(token):
    """
    Inserts a word into the dictionary of words, each word entry contains a dictionary of tags,
    containing the counters of the occurrences of those tags
    :param token: token to be added to the dictionary
    """
    # I use an HashMap inside the wordDictionary to contains the counters of all tags
    word, tag = splitWordAndToken(token)
    if word in wordDictionary0:
        if tag not in wordDictionary0[word]:
            wordDictionary0[word][tag] = 1
        else:
            wordDictionary0[word][tag] += 1
    else:
        wordDictionary0[word] = dict()
        wordDictionary0[word][tag] = 1


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


def initializeWordDictionary_andcreateTestSets():
    """
    Loads from file the train set and saves it into the word dictionary
    (N.B a word is saved only if the min support is reached)
    """
    with open('./../dataSets/final/train', 'r') as dataset:
        position = 1
        for line in dataset:
            # add every word to the dictionary (added only if its support reaches value 4)
            for token in line.split():
                if position % 4 != 0:
                    addTagToWordDictionary0(token)
                if position % 4 != 1:
                    addTagToWordDictionary1(token)
                if position % 4 != 2:
                    addTagToWordDictionary2(token)
                if position % 4 != 3:
                    addTagToWordDictionary3(token)
                if position % 4 == 0:
                    testSet0.append(token)
                if position % 4 == 1:
                    testSet1.append(token)
                if position % 4 == 2:
                    testSet2.append(token)
                if position % 4 == 3:
                    testSet3.append(token)
            position += 1
    with open('./../trains_for_crossvalid/valid_set0', 'w') as valid_set:
        for element in testSet0:
            print(element, file = valid_set)
    with open('./../trains_for_crossvalid/valid_set1', 'w') as valid_set:
        for element in testSet1:
            print(element, file = valid_set)
    with open('./../trains_for_crossvalid/valid_set2', 'w') as valid_set:
        for element in testSet2:
            print(element, file = valid_set)
    with open('./../trains_for_crossvalid/valid_set3', 'w') as valid_set:
        for element in testSet3:
            print(element, file = valid_set)

def writeResultsForBaselineTagger_all_trains():
    """
    Writes the results of this script to a file
    """
    with open('./../trains_for_crossvalid/baselineTaggerWordTagAssociations_train0', 'w') as dataset:
        for element in listTagStatisticsPerWord_train0:
            print(element[0] + " " + element[1][0][0], file=dataset)  # element and tag with max value
    with open('./../trains_for_crossvalid/baselineTaggerWordTagAssociations_train1', 'w') as dataset:
        for element in listTagStatisticsPerWord_train1:
            print(element[0] + " " + element[1][0][0], file=dataset)  # element and tag with max value
    with open('./../trains_for_crossvalid/baselineTaggerWordTagAssociations_train2', 'w') as dataset:
        for element in listTagStatisticsPerWord_train2:
            print(element[0] + " " + element[1][0][0], file=dataset)  # element and tag with max value
    with open('./../trains_for_crossvalid/baselineTaggerWordTagAssociations_train3', 'w') as dataset:
        for element in listTagStatisticsPerWord_train3:
            print(element[0] + " " + element[1][0][0], file=dataset)  # element and tag with max value

"""THIS PART COMES FROM baselineTagger FILE"""


initializeWordDictionary_andcreateTestSets()

listNumberOfTagsPerWord_train0 = []
listNumberOfTagsPerWord_train1 = []
listNumberOfTagsPerWord_train2 = []
listNumberOfTagsPerWord_train3 = []

listTagStatisticsPerWord_train0 = []
listTagStatisticsPerWord_train1 = []
listTagStatisticsPerWord_train2 = []
listTagStatisticsPerWord_train3 = []

for element in wordDictionary0:
    tagCounter = 0
    numberOfOccurrences = 0
    tempList = []
    for tag in wordDictionary0[element]:
        tagCounter += 1
        numberOfOccurrences += wordDictionary0[element][tag]
        tempList.append((tag, wordDictionary0[element][tag]))
    listNumberOfTagsPerWord_train0.append((element, tagCounter, numberOfOccurrences))
    tempList = sorted(tempList, key=itemgetter(1), reverse=True)
    listTagStatisticsPerWord_train0.append((element, tempList))

for element in wordDictionary1:
    tagCounter = 0
    numberOfOccurrences = 0
    tempList = []
    for tag in wordDictionary1[element]:
        tagCounter += 1
        numberOfOccurrences += wordDictionary1[element][tag]
        tempList.append((tag, wordDictionary1[element][tag]))
    listNumberOfTagsPerWord_train1.append((element, tagCounter, numberOfOccurrences))
    tempList = sorted(tempList, key=itemgetter(1), reverse=True)
    listTagStatisticsPerWord_train1.append((element, tempList))

for element in wordDictionary2:
    tagCounter = 0
    numberOfOccurrences = 0
    tempList = []
    for tag in wordDictionary2[element]:
        tagCounter += 1
        numberOfOccurrences += wordDictionary2[element][tag]
        tempList.append((tag, wordDictionary2[element][tag]))
    listNumberOfTagsPerWord_train2.append((element, tagCounter, numberOfOccurrences))
    tempList = sorted(tempList, key=itemgetter(1), reverse=True)
    listTagStatisticsPerWord_train2.append((element, tempList))

for element in wordDictionary3:
    tagCounter = 0
    numberOfOccurrences = 0
    tempList = []
    for tag in wordDictionary3[element]:
        tagCounter += 1
        numberOfOccurrences += wordDictionary3[element][tag]
        tempList.append((tag, wordDictionary3[element][tag]))
    listNumberOfTagsPerWord_train3.append((element, tagCounter, numberOfOccurrences))
    tempList = sorted(tempList, key=itemgetter(1), reverse=True)
    listTagStatisticsPerWord_train3.append((element, tempList))

writeResultsForBaselineTagger_all_trains()

print("\n*******\n*******\nIN TRAINING SET 0: \n******* \n*******")
#print(listNumberOfTagsPerWord)
print("Words associated to a single POStag (number and occurrencces):" + str(
    countNumberOfAssociations(listNumberOfTagsPerWord_train0, 1)))
print("Words associated to 2 POStags: (number and occurrences)" + str(
    countNumberOfAssociations(listNumberOfTagsPerWord_train0, 2)))
print("Words associated to 3 POStags: (number and occurrences)" + str(
    countNumberOfAssociations(listNumberOfTagsPerWord_train0, 3)))
print(
    "Words associated to 4 or more POStags: (number and occurrences)" + str(
        countNumberOfAssociationsGivenLowerBound(listNumberOfTagsPerWord_train0, 4)))
print("\"start\" statistics: " + str(extractWordStatistics(listTagStatisticsPerWord_train0, "start")))
print("Word with max number of tags: " + str(extractElementWithMaxNumberOfTags(listTagStatisticsPerWord_train0)))


print("\n*******\n*******\nIN TRAINING SET 1: \n******* \n*******")
#print(listNumberOfTagsPerWord)
print("Words associated to a single POStag (number and occurrencces):" + str(
    countNumberOfAssociations(listNumberOfTagsPerWord_train1, 1)))
print("Words associated to 2 POStags: (number and occurrences)" + str(
    countNumberOfAssociations(listNumberOfTagsPerWord_train1, 2)))
print("Words associated to 3 POStags: (number and occurrences)" + str(
    countNumberOfAssociations(listNumberOfTagsPerWord_train1, 3)))
print(
    "Words associated to 4 or more POStags: (number and occurrences)" + str(
        countNumberOfAssociationsGivenLowerBound(listNumberOfTagsPerWord_train1, 4)))
print("\"start\" statistics: " + str(extractWordStatistics(listTagStatisticsPerWord_train1, "start")))
print("Word with max number of tags: " + str(extractElementWithMaxNumberOfTags(listTagStatisticsPerWord_train1)))


print("\n*******\n*******\nIN TRAINING SET 2: \n******* \n*******")
#print(listNumberOfTagsPerWord)
print("Words associated to a single POStag (number and occurrencces):" + str(
    countNumberOfAssociations(listNumberOfTagsPerWord_train2, 1)))
print("Words associated to 2 POStags: (number and occurrences)" + str(
    countNumberOfAssociations(listNumberOfTagsPerWord_train2, 2)))
print("Words associated to 3 POStags: (number and occurrences)" + str(
    countNumberOfAssociations(listNumberOfTagsPerWord_train2, 3)))
print(
    "Words associated to 4 or more POStags: (number and occurrences)" + str(
        countNumberOfAssociationsGivenLowerBound(listNumberOfTagsPerWord_train2, 4)))
print("\"start\" statistics: " + str(extractWordStatistics(listTagStatisticsPerWord_train2, "start")))
print("Word with max number of tags: " + str(extractElementWithMaxNumberOfTags(listTagStatisticsPerWord_train2)))


print("\n*******\n*******\nIN TRAINING SET 3: \n******* \n*******")
#print(listNumberOfTagsPerWord)
print("Words associated to a single POStag (number and occurrencces):" + str(
    countNumberOfAssociations(listNumberOfTagsPerWord_train3, 1)))
print("Words associated to 2 POStags: (number and occurrences)" + str(
    countNumberOfAssociations(listNumberOfTagsPerWord_train3, 2)))
print("Words associated to 3 POStags: (number and occurrences)" + str(
    countNumberOfAssociations(listNumberOfTagsPerWord_train3, 3)))
print(
    "Words associated to 4 or more POStags: (number and occurrences)" + str(
        countNumberOfAssociationsGivenLowerBound(listNumberOfTagsPerWord_train3, 4)))
print("\"start\" statistics: " + str(extractWordStatistics(listTagStatisticsPerWord_train3, "start")))
print("Word with max number of tags: " + str(extractElementWithMaxNumberOfTags(listTagStatisticsPerWord_train3)))