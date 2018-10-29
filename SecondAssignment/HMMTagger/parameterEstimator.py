from Utilities.utility import splitWordAndToken


def initialState():
    return states[0]

wordList = []
states = '<S>', 'CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB', '$', '#', '``', '\'\'', '-LRB-', '-RRB-', ',', '.', ':'
with open('./../results/2/allWordsDictionary', 'r') as words:
    for line in words:
        wordList.append(line.split()[0])
numberOfWords = len(wordList)
numberOfStates = len(states)
A = dict() # of states
B = dict() # of words
numberOfWordsObservedPerState = dict() # of states
numberOfTimesStateIsFollowedByState = dict() # of states
numberOfVisitsPerState = dict() # of states
for state in states:
    A[state] = dict() # of states
    for secondState in states:
        temp = A[state]
        temp[secondState] = 0
for word in wordList:
    B[word] = dict() # of states
    for state in states:
        temp = B[word]
        temp[state] = 0
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

            if word not in numberOfTimesStateIsFollowedByState[state]:
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

for state in states:
    if(state in numberOfVisitsPerState) and (state in numberOfWordsObservedPerState):
        for word in wordList:
            if word in numberOfWordsObservedPerState[state]:
                B[word][state] = numberOfWordsObservedPerState[state][word] / numberOfVisitsPerState[state]
for secondState in states:
    if (secondState in numberOfTimesStateIsFollowedByState) and (secondState in numberOfVisitsPerState):
        for state in states:
            if state in numberOfTimesStateIsFollowedByState[secondState]:
                A[state][secondState] = numberOfTimesStateIsFollowedByState[secondState][state] / numberOfVisitsPerState[secondState]
print("A")
for state in states:
    print(A[state])
print("B")
for word in wordList:
    print(B[word])