from Utilities.utility import splitWordAndToken

wordTags = dict()
totalTagOccurrences = dict()
matchesMatrix = dict()
confusionMatrix = dict()


def loadWordTagMapping():
    with open('./../results/3/baselineTaggerWordTagAssociations', 'r') as dataset:
        for line in dataset:
            # add every word to the dictionary (added only if its support reaches value 4)
            word, tag = line.split()
            wordTags[word] = tag


def tagWord(word):
    return wordTags[word]


def incrementDictionaryCounter(tag, dictionary):
    if tag in dictionary:
        dictionary[tag] += 1
    else:
        dictionary[tag] = 1


def incrementTotalTagOccurrences(actualTag):
    incrementDictionaryCounter(actualTag, totalTagOccurrences)


def insertIntoMatchesMatrix(actualTag, predictedTag):
    if actualTag in matchesMatrix:
        incrementDictionaryCounter(predictedTag, matchesMatrix[actualTag])
    else:
        matchesMatrix[actualTag] = dict()
        matchesMatrix[actualTag][predictedTag] = 1


def buildConfusionMatrix():
    for actualTag in matchesMatrix:
        confusionMatrix[actualTag] = dict()
        for predictedTag in matchesMatrix[actualTag]:
            if predictedTag == actualTag:
                confusionMatrix[actualTag][predictedTag] = 0
            else:
                count = matchesMatrix[actualTag][predictedTag]
                errorPercentage = count / totalTagOccurrences[actualTag]
                confusionMatrix[actualTag][predictedTag] = errorPercentage


def computeErrorRates():
    totalSumOfWeightedErrors = 0
    totalNumberOfTagsOccurrences = 0
    errorRatePerTag = dict()
    for actualTag in confusionMatrix:
        sumOfErrors = 0
        tagFrequency = totalTagOccurrences[actualTag]
        totalNumberOfTagsOccurrences += tagFrequency
        for predictedTag in confusionMatrix[actualTag]:
            sumOfErrors += confusionMatrix[actualTag][predictedTag]
        totalSumOfWeightedErrors += tagFrequency * sumOfErrors
        errorRatePerTag[actualTag] = sumOfErrors
    return totalSumOfWeightedErrors / totalNumberOfTagsOccurrences, errorRatePerTag


def tagger():
    testSetArray = []
    untaggedTestSetArray = []
    with open('./../dataSets/final/test', 'r') as testSet:
        for line in testSet:
            list = []
            for token in line.split():
                word, tag = splitWordAndToken(token)
                list.append((word, tag))
            testSetArray.append(list)

    with open('./../dataSets/final/test_untagged', 'r') as untaggedTestSet:
        for line in untaggedTestSet:
            list = []
            for word in line.split():
                list.append(word)
            untaggedTestSetArray.append(list)

    for j in range(0, len(testSetArray)):
        testLine = testSetArray[j]
        untaggedTestLine = untaggedTestSetArray[j]
        for i in range(0, len(testLine)):
            word, actualTag = testLine[i][0], testLine[i][1]
            if word != untaggedTestLine[i]:
                print("wrong file!!!")
                exit(-1)
            predictedTag = tagWord(untaggedTestLine[i])
            insertIntoMatchesMatrix(actualTag, predictedTag)
            incrementTotalTagOccurrences(actualTag)

    buildConfusionMatrix()


loadWordTagMapping()
tagger()
actualTestTaggingErrorRate, testErrorRatePerTag = computeErrorRates()
print("Test tagging error rate: " + str(actualTestTaggingErrorRate))
print("Test error rate per tag: " + str(testErrorRatePerTag))
print("matches matrix: "+ str(matchesMatrix))

