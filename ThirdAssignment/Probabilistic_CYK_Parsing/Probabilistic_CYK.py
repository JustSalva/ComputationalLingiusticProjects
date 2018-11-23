import sys
from math import log

nonTerminalrules = dict()  # key = left hand side, value = dict with key = right hand side, value = probability
terminalrules = dict()
inversedTerminalRules = dict()  # key = right hand side, value = dict with key = left hand side, value = probability
inversedNonTerminalRules = dict()
vocabulary = dict()
nonTerminalsMapping = dict() # key = nonTerminal, value = its mapping int value
initialSymbol = "SBARQ"


class TreeNode(object):
    """
    class used to construct the syntax trees that are built during the search

    """

    def __init__(self, leftHandSide):
        self.leftHandSide = leftHandSide
        self.left_rightHandSide = None
        self.right_rightHandSide = None
        self.logProbability = None
        self.isTerminal = False

    def setLeft_rightHandSide(self, leftNode):
        self.left_rightHandSide = leftNode

    def setRight_rightHandSide(self, RightNode):
        self.right_rightHandSide = RightNode

    def setLogProbability(self, probability):
        self.logProbability = probability

    def setIsTerminal(self, isTerminal):
        self.isTerminal = isTerminal


def splitRuleLine(line):
    leftHandSide, rightHandSideWithProbability = line.split('→', 1)
    rightHandSide, stringProbability = rightHandSideWithProbability.split('[', 1)
    probability = float(stringProbability.replace("]", ""))
    return leftHandSide, rightHandSide, probability


def writeInDictionaryOfDictionary(dictionary, firstKey, secondKey, value):
    if firstKey in dictionary:
        if secondKey not in dictionary[firstKey]:
            dictionary[firstKey][secondKey] = value

        else:
            sys.exit("The rule file contains duplicates... Aborting")
    else:
        dictionary[firstKey] = dict()
        dictionary[firstKey][secondKey] = value


def addRule(leftHandSide, rightHandSide, probability):
    if " " not in rightHandSide:
        writeInDictionaryOfDictionary(terminalrules, leftHandSide, rightHandSide, probability)
    else:
        writeInDictionaryOfDictionary(nonTerminalrules, leftHandSide, rightHandSide, probability)



def addInversedRule(leftHandSide, rightHandSide, probability):
    if " " not in rightHandSide:
        writeInDictionaryOfDictionary(inversedTerminalRules, rightHandSide, leftHandSide, probability)
    else:
        writeInDictionaryOfDictionary(inversedNonTerminalRules, rightHandSide, leftHandSide, probability)


def addToRulesDictionaries(leftHandSide, rightHandSide, probability):
    addRule(leftHandSide, rightHandSide, log(probability))  # N.B. log probabilities!
    addInversedRule(leftHandSide, rightHandSide, probability)




def initializeRules():
    with open('./../data/projectFiles/rules', 'r') as dataset:
        for line in dataset:
            leftHandSide, rightHandSide, probability = splitRuleLine(line)
            addToRulesDictionaries(leftHandSide, rightHandSide, probability)


def initializeVocabulary():
    with open('./../data/projectFiles/vocabulary', 'r') as vocabularyDataset:
        for word in vocabularyDataset:
            vocabulary[word] = True  # just to mark an element as present

def initializeNonTerminalMapping():
    with open('./../data/projectFiles/nonTerminalsMapping', 'r') as nonTerminalMappingDataset:
        for line in nonTerminalMappingDataset:
            nonTerminal, indexString = line.split()
            nonTerminalsMapping[nonTerminal] = int(indexString)

def initializeStructures():
    initializeRules()
    initializeVocabulary()
    initializeNonTerminalMapping()

def replaceOOVWords(words):
    newWords = []
    for word in words:
        if word in vocabulary:
            newWords.append(word)
        else:
            newWords.append("<unknown>")
    return newWords


def splitNonTerminalRightHandSide(rightHandSide):
    leftNonTerminal, rightNonTerminal = rightHandSide.split(" ",1)
    return leftNonTerminal, rightNonTerminal

def buildTree(back):
    print()  # TODO

def startProbabilisticCYK(words):
    words = replaceOOVWords(words)
    back = [[[None for k in range(0, len(nonTerminalsMapping))] for j in range(0, len(words))] for i in range(0, len(words))]
    table = [[[0 for k in range(0, len(nonTerminalsMapping))] for j in range(0, len(words))] for i in range(0, len(words))]
    for j in range(1, len(words)+1):
        #init with terminal rules
        for nonTerminal in inversedTerminalRules[words[j]]:
            nonTerminalIndex = nonTerminalsMapping[nonTerminal]
            table[j-1][j][nonTerminalIndex] = inversedTerminalRules[words[j]][nonTerminal]

        for i in range(j-2, -1, -1):  # i ← j − 2 down to 0
            for k in range(i+1, j):
                for leftHandSide in nonTerminalrules:

                    leftHandSideIndex =  nonTerminalsMapping[leftHandSide] # = A

                    for rightHandSide in nonTerminalrules[leftHandSide]:

                        leftNonTerminal, rightNonTerminal = splitNonTerminalRightHandSide(rightHandSide)

                        leftNonTerminalIndex = nonTerminalsMapping[leftNonTerminal] # = B
                        rightNonTerminalIndex = nonTerminalsMapping[rightNonTerminal] # = C

                        if table[i][j][leftNonTerminalIndex] >0 and table[k][j][rightNonTerminalIndex]:
                            conditionValue = nonTerminalrules[leftHandSide][rightHandSide] \
                                             * table[i][j][leftNonTerminalIndex] \
                                             * table[k][j][rightNonTerminalIndex]
                            if table[i][j][leftHandSideIndex] < conditionValue:
                                table[i][j][leftHandSideIndex] = conditionValue
                                table[i][j][leftHandSideIndex] = (k, leftNonTerminalIndex, rightNonTerminalIndex)
    return buildTree(back[0][len(words)][nonTerminalsMapping[initialSymbol]]), table[0][len(words)][nonTerminalsMapping[initialSymbol]]


initializeStructures()
with open('./../data/two_sentences.txt', 'r') as sentencesDataset:
    for sentence in sentencesDataset:
        words = sentence.split()
        print(startProbabilisticCYK(words))
