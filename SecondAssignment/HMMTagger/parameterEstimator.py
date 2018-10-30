from Utilities.utility import splitWordAndToken
import numpy as np
import hmms
from random import shuffle


def loadTrainSet():
    with open('./../dataSets/final/train', 'r') as dataset:
        for line in dataset:
            tempList = []
            # add every word to the dictionary (added only if its support reaches value 4)
            for token in line.split():
                word, tag = splitWordAndToken(token)
                tempList.append((word, tag))
            trainSet.append(tempList)


def initialState():
    return states[0]


def initializeWordList():
    with open('./../results/2/allWordsDictionary', 'r') as words:
        for line in words:
            wordList.append(line.split()[0])


def computeCounters(trainSet):
    numberOfVisitsPerState[initialState()] = 0
    for line in trainSet:
        state = initialState()
        # add every word to the dictionary (added only if its support reaches value 4)
        for token in line:
            word, tag = token[0], token[1]
            if word not in numberOfWordsObservedPerState[state]:
                numberOfWordsObservedPerState[state][word] = 1
            else:
                numberOfWordsObservedPerState[state][word] += 1

            if tag not in numberOfTimesStateIsFollowedByState[state]:
                numberOfTimesStateIsFollowedByState[state][tag] = 1
            else:
                numberOfTimesStateIsFollowedByState[state][tag] += 1

            numberOfVisitsPerState[state] += 1
            state = tag
            if state not in numberOfWordsObservedPerState:
                numberOfWordsObservedPerState[state] = dict()

            if state not in numberOfTimesStateIsFollowedByState:
                numberOfTimesStateIsFollowedByState[state] = dict()

            if state not in numberOfVisitsPerState:
                numberOfVisitsPerState[state] = 0


def computeParameters(epsilonA, epsilonB):
    states = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT',
              'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP',
              'VBZ',
              'WDT', 'WP', 'WP$', 'WRB', '$', '#', '``', '\'\'', '-LRB-', '-RRB-', ',', '.', ':']
    i = 0
    for state in states:
        j = 0
        for word in wordList:
            if (state in numberOfVisitsPerState) and (state in numberOfWordsObservedPerState) and (
                    word in numberOfWordsObservedPerState[state]):
                B[i][j] = (numberOfWordsObservedPerState[state][word] + epsilonB) / (
                        numberOfVisitsPerState[state] + epsilonB * numberOfWords)
            else:
                if epsilonB != 0:
                    B[i][j] = 1 / numberOfWords
                else:
                    B[i][j] = 0
            j += 1
        i += 1

    i = 0
    for state in states:
        j = 0
        for secondState in states:
            if (state in numberOfVisitsPerState) and (state in numberOfWordsObservedPerState) and (
                    secondState in numberOfTimesStateIsFollowedByState[state]):
                A[i][j] = (numberOfTimesStateIsFollowedByState[state][secondState] + epsilonA) / (
                        numberOfVisitsPerState[state] + epsilonA * numberOfStates)
            else:
                if epsilonA != 0:
                    A[i][j] = 1 / numberOfStates
                else:
                    A[i][j] = 0
            j += 1
        i += 1
    i = 0
    for state in states:
        if (initialState() in numberOfVisitsPerState) and (initialState() in numberOfWordsObservedPerState) and (
                state in numberOfTimesStateIsFollowedByState[initialState()]):
            pi[i] = (numberOfTimesStateIsFollowedByState[initialState()][state] + epsilonA) / (
                    numberOfVisitsPerState[initialState()] + epsilonA * numberOfStates)
        else:
            if epsilonA != 0:
                pi[i] = 1 / numberOfStates
            else:
                pi[i] = 0
        i += 1
    # printMappingToFile()


def evaluate(tempTestSet):
    print()  # TODO


def getBestEpsilons(performances):
    return 0, 0  # TODO


def initializeMappings():
    with open('./../results/4/tagMapping', 'r') as tagMappingFile:
        for line in tagMappingFile:
            list = line.split()
            tagMapping[list[0]] = int(list[1])

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
epsilon_possible_values = [0.000001, 0.000005, 0.00001, 0.00005, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5]
performances = []
tagMapping = dict()
wordMapping = dict()
initializeMappings()
for i in range(0, k):
    temp_performances = []
    numberOfWordsObservedPerState = dict()  # of states
    numberOfTimesStateIsFollowedByState = dict()  # of states
    numberOfVisitsPerState = dict()  # of states
    numberOfWordsObservedPerState[initialState()] = dict()
    numberOfTimesStateIsFollowedByState[initialState()] = dict()
    computeParameters(epsilonA, epsilonB)
    tempTrainSet = []
    tempTestSet = []
    for i in range(0, len(trainSet)):
        if i % k != 0:
            tempTrainSet.append(trainSet[i])
        else:
            tempTestSet.append(trainSet[i])
    computeCounters(tempTrainSet)
    for epsilonA in epsilon_possible_values:
        for epsilonB in epsilon_possible_values:
            A = np.zeros((numberOfStates, numberOfStates))
            pi = np.zeros(numberOfStates)
            B = np.zeros((numberOfStates, numberOfWords))
            computeParameters(epsilonA, epsilonB)
            dhmm = hmms.DtHMM(A, B, pi)
            temp_performances.append(evaluate(tempTestSet))
    performances.append(temp_performances)

epsilonA, epsilonB = getBestEpsilons(performances)
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
"""
print("pi")
print(pi)
print(pi.shape)
print("A")
print(A.shape)
print("B")
print(B.shape)
"""
dhmm = hmms.DtHMM(A, B, pi)
dhmm.save_params('./../results/4/hmmParameters')
