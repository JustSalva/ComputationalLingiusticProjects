from Utilities.utility import splitWordAndToken
import numpy as np
import hmms
def initialState():
    return states[0]


epsilonA = 0
epsilonB = 0
wordList = []
states = '<S>', 'CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB', '$', '#', '``', '\'\'', '-LRB-', '-RRB-', ',', '.', ':'
actualStates = 'CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB', '$', '#', '``', '\'\'', '-LRB-', '-RRB-', ',', '.', ':'

with open('./../results/2/allWordsDictionary', 'r') as words:
    for line in words:
        wordList.append(line.split()[0])
numberOfWords = len(wordList)
numberOfStates = len(states)
#A = dict()  # of states
#B = dict()  # of words
numberOfWordsObservedPerState = dict()  # of states
numberOfTimesStateIsFollowedByState = dict()  # of states
numberOfVisitsPerState = dict()  # of states
"""
for state in states:
    A[state] = dict()  # of states
    for secondState in states:
        temp = A[state]
        temp[secondState] = 0
for word in wordList:
    B[word] = dict()  # of states
    for state in states:
        temp = B[word]
        temp[state] = 0
"""
numberOfWordsObservedPerState[initialState()] = dict()
numberOfTimesStateIsFollowedByState[initialState()] = dict()
numberOfVisitsPerState[initialState()] = 0

with open('./../dataSets/final/train', 'r') as dataset:
    for line in dataset:
        state = initialState()
        # add every word to the dictionary (added only if its support reaches value 4)
        for token in line.split():
            word, tag = splitWordAndToken(token)
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
B = np.zeros((numberOfStates- 1, numberOfWords))
i = 0
for state in actualStates:
    j = 0
    for word in wordList:
        if (state in numberOfVisitsPerState) and (state in numberOfWordsObservedPerState) and (
                word in numberOfWordsObservedPerState[state]):
            B[i][j] = (numberOfWordsObservedPerState[state][word] + epsilonB) / (
                        numberOfVisitsPerState[state] + epsilonB * numberOfWords)
        else:
            if epsilonB != 0:
                B[i][j] = 1 / numberOfWords
        j += 1
    i += 1

A = np.zeros((numberOfStates- 1, numberOfStates -1))
pi = np.zeros(numberOfStates - 1 )
i = -1
for state in actualStates:
    j = 0
    for secondState in actualStates:
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
    i+=1
i = 0
for state in actualStates:
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
"""
print("pi")
print(pi)
print("A")
print(A)
print("B")
print(B)
print(actualStates)
"""

dhmm = hmms.DtHMM(A,B,pi)

dhmm.save_params('./../results/4/hmmParameters')