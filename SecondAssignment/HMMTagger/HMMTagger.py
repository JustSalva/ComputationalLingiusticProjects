import numpy as np
from Utilities.utility import splitWordAndToken
import hmms

totalTagOccurrences = dict()
matchesMatrix = dict()
confusionMatrix = dict()
tagMapping = dict()
wordMapping = dict()


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


def initializeMappings():
    with open('./../results/4/tagMapping', 'r') as tagMappingFile:
        for line in tagMappingFile:
            list = line.split()
            tagMapping[int(list[1])] = list[0]

    with open('./../results/4/wordMapping', 'r') as wordMappingFile:
        for line in wordMappingFile:
            list = line.split()
            wordMapping[list[0]] = int(list[1])


def evaluate(testSet, dhmm):
    for i in range(0, len(testSet)):
        testLine = testSet[i]
        wordSequence_temp_list = np.zeros(len(testLine), dtype=int)

        for k in range(0, len(testLine)):
            wordSequence_temp_list[k] = wordMapping[testLine[k][0]]
        (log_prob, state_sequence) = dhmm.viterbi(wordSequence_temp_list)
        for j in range(0, len(testLine)):
            word, actualTag = testLine[j][0], testLine[j][1]
            predictedTag = tagMapping[state_sequence[j]]
            insertIntoMatchesMatrix(actualTag, predictedTag)
            incrementTotalTagOccurrences(actualTag)
    buildConfusionMatrix()
    return computeErrorRates()


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
        errorRatePerTag[actualTag] = sumOfErrors / len(matchesMatrix)
    return totalSumOfWeightedErrors / totalNumberOfTagsOccurrences, errorRatePerTag

def loadTestSet():

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
dhmm = hmms.DtHMM.from_file( './../results/4/hmmParameters.npz')

actualTestTaggingErrorRate, testErrorRatePerTag = evaluate(testSetArray, dhmm)
print("Test tagging error rate: " + str(actualTestTaggingErrorRate))
print("Test error rate per tag: " + str(testErrorRatePerTag))
print("matches matrix: "+ str(matchesMatrix))
