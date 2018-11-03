from Utilities.utility import splitWordAndToken
import numpy as np
import hmms
from random import shuffle
import math

actualStates = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT',
                'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP',
                'VBZ',
                'WDT', 'WP', 'WP$', 'WRB', '$', '#', '``', '\'\'', '-LRB-', '-RRB-', ',', '.', ':']


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


def computeErrorRates():
    """
    Compute the tagging error rate and the error rates for each tag
    :return: the tagging error rate and the error rates for each tag
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


def loadTrainSet():
    """
    Loads the train set from its file to a list of sentences, each one containing a list of tokens
    """
    with open('./../dataSets/final/train', 'r') as dataset:
        for line in dataset:
            tempList = []
            # add every word to the dictionary (added only if its support reaches value 4)
            for token in line.split():
                word, tag = splitWordAndToken(token)
                tempList.append((word, tag))
            trainSet.append(tempList)


def initialState():
    """
    :return: The initial state of the HMM tagger
    """
    return states[0]


def initializeWordList():
    """
    Loads from its file the dictionary of all words
    """
    with open('./../results/2/allWordsDictionary', 'r') as words:
        for line in words:
            wordList.append(line.split()[0])


def computeCounters(trainSet):
    """
    Compute the conters needed to estimate the HMM parameters
    :param trainSet: data-set form which the parameters must be learned
    """
    numberOfVisitsPerState[initialState()] = 0
    for line in trainSet:
        state = initialState()
        # add every word to the dictionary (added only if its support reaches value 4)
        for token in line:
            word, tag = token[0], token[1]
            if tag not in numberOfWordsObservedPerState:
                numberOfWordsObservedPerState[tag] = dict()
            if word not in numberOfWordsObservedPerState[tag]:
                numberOfWordsObservedPerState[tag][word] = 1
            else:
                numberOfWordsObservedPerState[tag][word] += 1

            if tag not in numberOfTimesStateIsFollowedByState[state]:
                numberOfTimesStateIsFollowedByState[state][tag] = 1
            else:
                numberOfTimesStateIsFollowedByState[state][tag] += 1

            numberOfVisitsPerState[state] += 1
            state = tag

            if state not in numberOfTimesStateIsFollowedByState:
                numberOfTimesStateIsFollowedByState[state] = dict()

            if state not in numberOfVisitsPerState:
                numberOfVisitsPerState[state] = 0


def computeA(epsilonA):
    """
    Computes the A matrix of the HMM
    :param epsilonA: smoothing parameter
    """
    i = 0
    for state in actualStates:
        j = 0
        if not (state in numberOfVisitsPerState):
            visits = 0
        else:
            visits = numberOfVisitsPerState[state]
        for secondState in actualStates:
            if (not (state in numberOfTimesStateIsFollowedByState)) or (
                    not (secondState in numberOfTimesStateIsFollowedByState[state])):
                followingStateCount = 0
            else:
                followingStateCount = numberOfTimesStateIsFollowedByState[state][secondState]
            if visits != 0 or followingStateCount != 0:
                A[i][j] = (float(followingStateCount + epsilonA)) / (
                    float(visits + epsilonA * numberOfStates))
            else:
                if epsilonA != 0:
                    A[i][j] = 1 / numberOfStates
                else:
                    A[i][j] = 0
            j += 1
        i += 1


def computeB(epsilonB):
    """
    Computes the B matrix of the HMM
    :param epsilonB: smoothing parameter
    """
    i = 0
    for state in actualStates:
        j = 0
        if not (state in numberOfVisitsPerState):
            visits = 0
        else:
            visits = numberOfVisitsPerState[state]
        for word in wordList:
            if (not (state in numberOfWordsObservedPerState)) or (not (word in numberOfWordsObservedPerState[state])):
                observedWords = 0
            else:
                observedWords = numberOfWordsObservedPerState[state][word]
            if visits != 0 or epsilonB != 0:
                B[i][j] = (float(observedWords + epsilonB)) / (
                    float(visits + epsilonB * numberOfWords))
            else:
                if epsilonB != 0:
                    B[i][j] = 1 / numberOfWords
                else:
                    B[i][j] = 0
            j += 1
        i += 1


def computePi(epsilonA):
    """
    Computes the Pi vector of the HMM
    :param epsilonA: smoothing parameter
    """
    i = 0
    for state in actualStates:
        if not (initialState() in numberOfVisitsPerState):
            visits = 0
        else:
            visits = numberOfVisitsPerState[initialState()]
        if (not (initialState() in numberOfTimesStateIsFollowedByState)) or (
                not (state in numberOfTimesStateIsFollowedByState[initialState()])):
            followingStateCount = 0
        else:
            followingStateCount = numberOfTimesStateIsFollowedByState[initialState()][state]
        if () and (initialState() in numberOfWordsObservedPerState) and (
        ):
            pi[i] = (float(followingStateCount + epsilonA)) / (
                float(visits + (epsilonA * numberOfStates)))
        else:
            if epsilonA != 0:
                pi[i] = 1 / numberOfStates
            else:
                pi[i] = 0
        i += 1


def computeParameters(epsilonA, epsilonB):
    """
    Computes the parameters of the HMM: A,B and pi
    :param epsilonA: smoothing parameter for A matrix and pi
    :param epsilonB: smoothing parameter for B matrix and
    """
    computeB(epsilonB)
    computeA(epsilonA)
    computePi(epsilonA)
    # printMappingToFile()


def evaluate(tempValidationSet, dhmm):
    """
    Evaluates the performances of the HMM POS tagger
    :param tempValidationSet: validation set that must be used to evaluate the tagger
    :param dhmm: HMM POS tagger to be evaluated
    :return: the tagging error rate
    """
    for i in range(0, len(tempValidationSet)):
        testLine = tempValidationSet[i]
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
    taggingErrorRate, tagRates = computeErrorRates()
    return taggingErrorRate


def addToPerformanceList(taggingErrorRate, epsilonA, epsilonB):
    """
    Adds to the performance list
    (one value for each fold of the cross validation and for each couple of meta parameters)
    :param taggingErrorRate: error rate to be added
    :param epsilonA: smoothing parameter for A matrix
    :param epsilonB: smoothing parameter for B matrix
    """
    if epsilonA in performanceErrors:
        if epsilonB in performanceErrors[epsilonA]:
            performanceErrors[epsilonA][epsilonB] += taggingErrorRate
        else:
            performanceErrors[epsilonA][epsilonB] = taggingErrorRate
    else:
        performanceErrors[epsilonA] = dict()
        performanceErrors[epsilonA][epsilonB] = taggingErrorRate
    # print("tagging error rate: " + str(taggingErrorRate))
    # print("epsilonA: " + str(epsilonA))
    # print("epsilonB: " + str(epsilonB))


def getBestEpsilons(performanceErrors):
    """
    Returns the best parameters according to the performance of the model for each couple of parameters
    :param performanceErrors: list of performances w.r.t. the parameters' values
    :return: the parameters whose performance is better
    """
    bestEpsilonA = 0
    bestEpsilonB = 0
    minError = math.inf
    for epsilonA in performanceErrors:
        for epsilonB in performanceErrors[epsilonA]:
            if performanceErrors[epsilonA][epsilonB] <= minError:
                minError = performanceErrors[epsilonA][epsilonB]
                bestEpsilonA = epsilonA
                bestEpsilonB = epsilonB
    return bestEpsilonA, bestEpsilonB


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


"""
def printMappingToFile():
    with open('./../results/4/tagMapping', 'w') as tagMappingFile:
        for state in statesMapping:
            print(state[0] + " " + str(state[1]), file=tagMappingFile)
        i = 0
    with open('./../results/4/wordMapping', 'w') as wordMappingFile:
        for word in wordList:
            print(word + " " + str(i), file=wordMappingFile)
            i += 1
"""

wordList = []
trainSet = []
states = ['<S>', 'CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT',
          'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',
          'WDT', 'WP', 'WP$', 'WRB', '$', '#', '``', '\'\'', '-LRB-', '-RRB-', ',', '.', ':']

initializeWordList()
# declaration of global variables
numberOfWords = len(wordList)
numberOfStates = len(states) - 1  # one state is <S> !
numberOfWordsObservedPerState = dict()  # of states
numberOfTimesStateIsFollowedByState = dict()  # of states
numberOfVisitsPerState = dict()  # of states
numberOfWordsObservedPerState[initialState()] = dict()
numberOfTimesStateIsFollowedByState[initialState()] = dict()
loadTrainSet()

# K- fold cross validation
k = 10
shuffle(trainSet)
epsilonA = 0
epsilonB = 0
# epsilon parameters' values to be tested
# epsilon_possible_values = [0.000001, 0.000005, 0.00001, 0.00005, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5]
epsilon_possible_valuesA = [0.002, 0.0025, 0.003, 0.0035, 0.004]
epsilon_possible_valuesB = [0.000001, 0.0000015, 0.000002, 0.0000025]
performanceErrors = dict()
tagMapping = dict()
wordMapping = dict()
initializeMappings()
# K - FOLD crossvalidation is commented since it has already been performed
"""
for i in range(0, k):
    print(" crossvalidation with fold = " + str(i))
    numberOfWordsObservedPerState = dict()  # of states
    numberOfTimesStateIsFollowedByState = dict()  # of states
    numberOfVisitsPerState = dict()  # of states
    numberOfWordsObservedPerState[initialState()] = dict()
    numberOfTimesStateIsFollowedByState[initialState()] = dict()
    tempTrainSet = []
    tempTestSet = []
    for i in range(0, len(trainSet)):
        if i % k != 0:
            tempTrainSet.append(trainSet[i])
        else:
            tempTestSet.append(trainSet[i])
    computeCounters(tempTrainSet)
    for epsilonA in epsilon_possible_valuesA:
        for epsilonB in epsilon_possible_valuesB:
            A = np.zeros((numberOfStates, numberOfStates))
            pi = np.zeros(numberOfStates)
            B = np.zeros((numberOfStates, numberOfWords))
            computeParameters(epsilonA, epsilonB)
            dhmm = hmms.DtHMM(A, B, pi)
            totalTagOccurrences = dict()
            matchesMatrix = dict()
            confusionMatrix = dict()
            taggingErrorRate = evaluate(tempTestSet, dhmm)
            addToPerformanceList(taggingErrorRate, epsilonA, epsilonB)
"""
# epsilonA, epsilonB = getBestEpsilons(performanceErrors)

# now we compute the final model with the entire train set,
# with the values obtained from the cross-validaton phase

epsilonA, epsilonB = 0.003, 0.000002
print("optimal epsilonA: " + str(epsilonA))
print("optimal epsilonB: " + str(epsilonB))
print(performanceErrors)
A = np.zeros((numberOfStates, numberOfStates))
pi = np.zeros(numberOfStates)
B = np.zeros((numberOfStates, numberOfWords))
numberOfWordsObservedPerState = dict()  # of states
numberOfTimesStateIsFollowedByState = dict()  # of states
numberOfVisitsPerState = dict()  # of states
numberOfWordsObservedPerState[initialState()] = dict()
numberOfTimesStateIsFollowedByState[initialState()] = dict()
computeCounters(trainSet)
computeParameters(epsilonA, epsilonB)

# Save the pos tagger to file
dhmm = hmms.DtHMM(A, B, pi)
dhmm.save_params('./../results/4/hmmParameters')

# compute the tagging error rate on the test set
totalTagOccurrences = dict()
matchesMatrix = dict()
confusionMatrix = dict()
taggingErrorRate = evaluate(trainSet, dhmm)
print(taggingErrorRate)
