import sys
from math import log

nonTerminalrules = dict()  # key = left hand side, value = dict with key = right hand side, value = probability
terminalrules = dict()
inversedTerminalRules = dict()  # key = right hand side, value = dict with key = left hand side, value = probability
inversedNonTerminalRules = dict()
vocabulary = dict()
nonTerminalsMapping = dict()  # key = nonTerminal, value = its mapping int value
nonTerminalsMappingReversed = dict()
initialSymbol = "SBARQ"


class TreeNode(object):
    """
    class used to construct the syntax trees that are built during the search

    """

    def __init__(self, leftHandSide):
        self.leftHandSide = leftHandSide
        self.left_rightHandSide = None
        self.right_rightHandSide = None
        # self.logProbability = None
        self.isTerminal = False
        self.wordCounter = -1

    def setLeft_rightHandSide(self, leftNode):
        self.left_rightHandSide = leftNode

    def setRight_rightHandSide(self, RightNode):
        self.right_rightHandSide = RightNode

    # def setLogProbability(self, probability):
    #     self.logProbability = probability

    def setIsTerminal(self, isTerminal):
        self.isTerminal = isTerminal

    def setWordCounter(self, wordCounter):
        self.wordCounter = wordCounter


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
            vocabulary[word.replace("\n", "")] = True  # just to mark an element as present


def initializeNonTerminalMapping():
    with open('./../data/projectFiles/nonTerminalsMapping', 'r') as nonTerminalMappingDataset:
        for line in nonTerminalMappingDataset:
            nonTerminal, indexString = line.split()
            nonTerminalsMapping[nonTerminal] = int(indexString)
            nonTerminalsMappingReversed[int(indexString)] = nonTerminal


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
    leftNonTerminal, rightNonTerminal = rightHandSide.split(" ", 1)
    return leftNonTerminal, rightNonTerminal


def buildTree(lowerPos, higherPos, symbolIndex, back):
    treeNode = TreeNode(nonTerminalsMappingReversed[symbolIndex])
    if back[lowerPos][higherPos][symbolIndex] is not None:
        k, leftNonTerminal, rightNonTerminal = back[lowerPos][higherPos][symbolIndex]

        leftNonTerminalIndex = nonTerminalsMapping[leftNonTerminal]  # = B
        rightNonTerminalIndex = nonTerminalsMapping[rightNonTerminal]  # = C

        treeNode.setLeft_rightHandSide(buildTree(lowerPos, k, leftNonTerminalIndex, back))
        treeNode.setRight_rightHandSide(buildTree(k, higherPos, rightNonTerminalIndex, back))
        treeNode.setIsTerminal(False)
        return treeNode
    else:
        treeNode.setIsTerminal(True)
        treeNode.setWordCounter(higherPos - 1)
        return treeNode


def printTree(tree, words):
    if not tree.isTerminal:
        return "(" + tree.leftHandSide + " " + printTree(tree.left_rightHandSide, words) + printTree(
            tree.right_rightHandSide, words) + ")"
    else:
        return "(" + tree.leftHandSide + " " + words[tree.wordCounter] + ")"


def startProbabilisticCYK(words):
    words = replaceOOVWords(words)
    back = [[[None for _ in range(len(nonTerminalsMapping))] for _ in range(len(words) + 1)]
            for _ in range(len(words) + 1)]

    table = [[[0 for _ in range(len(nonTerminalsMapping))] for _ in range(len(words) + 1)]
             for _ in range(len(words) + 1)]

    for j in range(1, len(words) + 1):
        # init with terminal rules
        for nonTerminal in inversedTerminalRules[words[j - 1]]:
            nonTerminalIndex = nonTerminalsMapping[nonTerminal]
            ruleValue = inversedTerminalRules[words[j - 1]][nonTerminal]
            table[j - 1][j][nonTerminalIndex] = ruleValue

        for i in range(j - 2, -1, -1):  # i ← j − 2 down to 0
            for k in range(i + 1, j):
                for leftNonTerminal in nonTerminalsMapping:
                    leftNonTerminalIndex = nonTerminalsMapping[leftNonTerminal]  # = B
                    if table[i][k][leftNonTerminalIndex] > 0:  # check first non-terminal in right hand side of the rule
                        for rightNonTerminal in nonTerminalsMapping:
                            rightNonTerminalIndex = nonTerminalsMapping[rightNonTerminal]  # = C
                            if table[k][j][
                                rightNonTerminalIndex] > 0:  # check second non-terminal in right hand side of the rule
                                rightHandSide = leftNonTerminal + " " + rightNonTerminal
                                if rightHandSide in inversedNonTerminalRules:
                                    for leftHandSide in inversedNonTerminalRules[rightHandSide]:
                                        probability = inversedNonTerminalRules[rightHandSide][leftHandSide]
                                        leftHandSideIndex = nonTerminalsMapping[leftHandSide]  # = A
                                        conditionValue = probability \
                                                         + table[i][k][leftNonTerminalIndex] \
                                                         + table[k][j][rightNonTerminalIndex]
                                        if table[i][j][leftHandSideIndex] < conditionValue:
                                            table[i][j][leftHandSideIndex] = conditionValue
                                            back[i][j][leftHandSideIndex] = (k, leftNonTerminal, rightNonTerminal)
    if back[0][len(words)][nonTerminalsMapping[initialSymbol]] is not None:
        return buildTree(0, len(words), nonTerminalsMapping[initialSymbol], back), table[0][len(words)][
            nonTerminalsMapping[initialSymbol]]
    else:
        return "()", 0


initializeStructures()

# with open('./../data/two_sentences.txt', 'r') as sentencesDataset:
#     for sentence in sentencesDataset:
#         words = sentence.split()
#         tree, probability = startProbabilisticCYK(words)
#         print(printTree(tree, words))
fileNames = ["train", "test"]
for fileName in fileNames:
    with open('./../data/' + fileName + '/' + fileName + '.input.txt', 'r') as sentencesDataset:
        with open('./../data/results/' + fileName + ".system.txt", 'w') as outputDataset:
            for sentence in sentencesDataset:
                words = sentence.split()
                tree, probability = startProbabilisticCYK(words)
                print(printTree(tree, words), file=outputDataset)
