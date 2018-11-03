from Utilities.utility import splitWordAndToken

wordTags = dict()
totalTagOccurrences = dict()
matchesMatrix = dict()
confusionMatrix = dict()


def loadWordTagMapping():
    """
    Loads the word - tag mapping from file, ad saves it in a dictionary
    (N.B. the baseline tagger associates a word with its most frequent tag in the train set
    """
    with open('./../trains_for_crossvalid/baselineTaggerWordTagAssociations_train0', 'r') as dataset:
        for line in dataset:
            # add every word to the dictionary (added only if its support reaches value 4)
            word, tag = line.split()
            wordTags[word] = tag


def tagWord(word):
    """
    Tags a word with its defined tag
    :param word: word to be tagged
    :return: the word's tag
    """
    try:
       return wordTags[word]
    except:
        return '<UNK>'


def incrementDictionaryCounter(tag, dictionary):
    """
    Increment the counter of a tag inside the dictionary
    :param tag: tag whose counter is to be incremented
    :param dictionary: dictionary that contains the tag
    """
    if tag in dictionary:
        dictionary[tag] += 1
    else:
        dictionary[tag] = 1


def incrementTotalTagOccurrences(actualTag):
    """
    Increments the total tag occurrences of a specific tag by one
    :param actualTag: tag whose counter is to be incremented
    """
    incrementDictionaryCounter(actualTag, totalTagOccurrences)


def insertIntoMatchesMatrix(actualTag, predictedTag):
    """
    Increments the counter of a match into the matrix containing all possible matches for all possible couples of tags
    :param actualTag: correct tag
    :param predictedTag: tag predicted by the baseline tagger
    """
    if actualTag in matchesMatrix:
        incrementDictionaryCounter(predictedTag, matchesMatrix[actualTag])
    else:
        matchesMatrix[actualTag] = dict()
        matchesMatrix[actualTag][predictedTag] = 1


def buildConfusionMatrix():
    """
    From the matrix of counters it builds the confusion matrix, computing the errors
    """
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
    """
    Computes the tagging error rate and the error rates for every tag
    :return: the computed errors
    """
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


def validation_tagger_0():
    """
    Tags the test-set according to the baseline tagger's word-tag pairings
    """
    testSetArray = []
    untaggedTestSetArray = []
    with open('./..//trains_for_crossvalid/valid_set0', 'r') as testSet:
        for line in testSet:
            list = []
            for token in line.split():
                word, tag = splitWordAndToken(token)
                list.append((word, tag))
            testSetArray.append(list)

    with open('./../trains_for_crossvalid/valid_untagged_0', 'r') as untaggedTestSet:
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
validation_tagger_0()
actualTestTaggingErrorRate, testErrorRatePerTag = computeErrorRates()
print("Test tagging error rate: " + str(actualTestTaggingErrorRate))
print("Test error rate per tag: " + str(testErrorRatePerTag))
print("matches matrix: "+ str(matchesMatrix))
