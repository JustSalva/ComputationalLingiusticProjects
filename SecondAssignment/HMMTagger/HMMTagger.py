import numpy as np
from Utilities.utility import splitWordAndToken
import hmms

totalTagOccurrences = dict()
matchesMatrix = dict()
confusionMatrix = dict()
tagMapping = dict()
wordMapping = dict()
actualSentenceProbabilities = []


def incrementDictionaryCounter(tag, dictionary):
    """
    Increments the counter of a tag in its corresponding dictionary
    :param tag: tag whose counter is to be incremented
    :param dictionary: dictionary that contains the counter
    """
    if tag in dictionary:
        dictionary[tag] += 1
    else:
        dictionary[tag] = 1


def incrementTotalTagOccurrences(actualTag):
    """
    Increments the tag occurrences counter of the specified tag
    :param actualTag: tag whose counter is to be incremented
    """
    incrementDictionaryCounter(actualTag, totalTagOccurrences)


def insertIntoMatchesMatrix(actualTag, predictedTag):
    """
    Inserts a match into the matrix that keeps the count of the matches between the predicted and the actual tags
    :param actualTag: actual tag whose counter is to be incremented
    :param predictedTag: predicted tag whose counter is to be incremented
    """
    if actualTag in matchesMatrix:
        incrementDictionaryCounter(predictedTag, matchesMatrix[actualTag])
    else:
        matchesMatrix[actualTag] = dict()
        matchesMatrix[actualTag][predictedTag] = 1


def buildConfusionMatrix():
    """
    Builds the confusion matrix using the counters already initialized during the evaluation phase
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


def initializeMappings():
    """
    Initialize the dictionaries that maps the tags and the maps with the "numbers" associated
    to them by the HMM library
    """
    with open('./../results/4/tagMapping', 'r') as tagMappingFile:
        for line in tagMappingFile:
            list = line.split()
            tagMapping[int(list[1])] = list[0]

    with open('./../results/4/wordMapping', 'r') as wordMappingFile:
        for line in wordMappingFile:
            list = line.split()
            wordMapping[list[0]] = int(list[1])


def evaluate(testSet, dhmm):
    """
        Evaluates the performances of the HMM POS tagger
        :param testSet: test set that must be used to evaluate the tagger
        :param dhmm: HMM POS tagger to be evaluated
        :return: the tagging error rate
        """
    for i in range(0, len(testSet)):
        testLine = testSet[i]
        wordSequence_temp_list = np.zeros(len(testLine), dtype=int)

        for k in range(0, len(testLine)):
            wordSequence_temp_list[k] = wordMapping[testLine[k][0]]
        (log_prob, state_sequence) = dhmm.viterbi(wordSequence_temp_list)
        actualSentenceProbabilities.append(log_prob)
        for j in range(0, len(testLine)):
            word, actualTag = testLine[j][0], testLine[j][1]
            predictedTag = tagMapping[state_sequence[j]]
            insertIntoMatchesMatrix(actualTag, predictedTag)
            incrementTotalTagOccurrences(actualTag)
    buildConfusionMatrix()
    return computeErrorRates()


def computeErrorRates():
    """
        Compute the tagging error rate and the average error rates for each tag
        :return: the tagging error rate and the averag error rates for each tag
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
        errorRatePerTag[actualTag] = sumOfErrors / len(matchesMatrix)
    return totalSumOfWeightedErrors / totalNumberOfTagsOccurrences, errorRatePerTag


def loadTestSet():
    """
        Loads the test set from its file to a list of sentences, each one containing a list of tokens
        """
    with open('./../dataSets/final/test', 'r') as testSet:
        for line in testSet:
            list = []
            for token in line.split():
                word, tag = splitWordAndToken(token)
                list.append((word, tag))
            testSetArray.append(list)


testSetArray = []
loadTestSet()
initializeMappings()
dhmm = hmms.DtHMM.from_file('./../results/4/hmmParameters.npz')

actualTestTaggingErrorRate, testErrorRatePerTag = evaluate(testSetArray, dhmm)
print("Test tagging error rate: " + str(actualTestTaggingErrorRate))
print("Test error rate per tag: " + str(testErrorRatePerTag))
print("Actual probability of the first sentence: " + str(actualSentenceProbabilities[0]))
print("Actual probability of all sentences(in order): " + str(actualSentenceProbabilities))
print("matches matrix: " + str(matchesMatrix))
