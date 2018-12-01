import sys
from math import log, inf

nonTerminalRules = dict()  # key = left hand side, value = dict with key = right hand side, value = probability
terminalRules = dict()
invertedTerminalRules = dict()  # key = right hand side, value = dict with key = left hand side, value = probability
invertedNonTerminalRules = dict()
vocabulary = dict()
nonTerminalsMapping = dict()  # key = nonTerminal, value = its mapping int value
nonTerminalsMappingReversed = dict()
initialSymbol = "SBARQ"


class TreeNode(object):
    """
    Class used to construct the syntax trees that are built during the search
    """

    def __init__(self, leftHandSide):
        self.leftHandSide = leftHandSide
        self.left_rightHandSide = None
        self.right_rightHandSide = None
        # self.logProbability = None
        self.isTerminal = False
        self.wordCounter = -1

    def setLeft_rightHandSide(self, leftNode):
        """
        Sets the "B" left hand side rule (NB rules are A-> BC, C might be missing)
        :param leftNode: left hand side rule node's to be added
        """
        self.left_rightHandSide = leftNode

    def setRight_rightHandSide(self, rightNode):
        """
        Sets the "C" left hand side rule (NB rules are A-> BC, C might be missing)
        :param rightNode: left hand side rule node's to be added
        """
        self.right_rightHandSide = rightNode

    # def setLogProbability(self, probability):
    #     self.logProbability = probability

    def setIsTerminal(self, isTerminal):
        self.isTerminal = isTerminal

    def setWordCounter(self, wordCounter):
        """
        Word counters ar used when we must recover a word that has been substituted with the "unknown" tag
        This method is used to set it
        :param wordCounter: counter of the word
        """
        self.wordCounter = wordCounter


def splitRuleLine(line):
    """
    Splits a file line into the rule's left and right hand sides and in its probability
    :param line: line to be split
    :return: the three elements in which the line is split
    """
    leftHandSide, rightHandSideWithProbability = line.split('→', 1)
    rightHandSide, stringProbability = rightHandSideWithProbability.split('[', 1)
    probability = float(stringProbability.replace("]", ""))
    return leftHandSide, rightHandSide, probability


def writeInDictionaryOfDictionary(dictionary, firstKey, secondKey, value):
    """
    Generic function used to write in a two-levels dictionary structure a value
    :param dictionary: dictionary in which the value must be written
    :param firstKey: key that identifies the first level of the dictionary
    :param secondKey: key that identifies the second level of the dictionary
    :param value: value to be written in the dictionary
    """
    if firstKey in dictionary:
        if secondKey not in dictionary[firstKey]:
            dictionary[firstKey][secondKey] = value

        else:
            sys.exit("The dictionary file contains duplicates... Aborting")
    else:
        dictionary[firstKey] = dict()
        dictionary[firstKey][secondKey] = value


def addRule(leftHandSide, rightHandSide, probability):
    """
    Adds a rule into the rule dictionary mappings (either terminal or non-terminal)
    :param leftHandSide: left hand side of the rule (string)
    :param rightHandSide: right hand side of the rule (string)
    :param probability: probability of the rule
    """
    if " " not in rightHandSide:
        writeInDictionaryOfDictionary(terminalRules, leftHandSide, rightHandSide, probability)
    else:
        writeInDictionaryOfDictionary(nonTerminalRules, leftHandSide, rightHandSide, probability)


def addInversedRule(leftHandSide, rightHandSide, probability):
    """
    Adds a rule into the inverted rule dictionary mappings (either terminal or non-terminal)
    This inverted mappings structures are very useful duing the CYK probabilistic parsing
    :param leftHandSide: left hand side of the rule (string)
    :param rightHandSide: right hand side of the rule (string)
    :param probability: probability of the rule
    """
    if " " not in rightHandSide:
        writeInDictionaryOfDictionary(invertedTerminalRules, rightHandSide, leftHandSide, probability)
    else:
        writeInDictionaryOfDictionary(invertedNonTerminalRules, rightHandSide, leftHandSide, probability)


def addToRulesDictionaries(leftHandSide, rightHandSide, probability):
    """
    Adds a rule into either inverted or not rule dictionary mappings (either terminal or non-terminal)
    This inverted mappings structures are very useful duing the CYK probabilistic parsing
    :param leftHandSide: left hand side of the rule (string)
    :param rightHandSide: right hand side of the rule (string)
    :param probability: probability of the rule
    """
    addRule(leftHandSide, rightHandSide, log(probability))  # N.B. log probabilities!
    addInversedRule(leftHandSide, rightHandSide, log(probability))


def initializeRules():
    """
    Loads the rules from file
    """
    with open('./../data/projectFiles/rules', 'r') as dataset:
        for line in dataset:
            leftHandSide, rightHandSide, probability = splitRuleLine(line)
            addToRulesDictionaries(leftHandSide, rightHandSide, probability)


def initializeVocabulary():
    """
    Loads the word's dictionary from file
    """
    with open('./../data/projectFiles/vocabulary', 'r') as vocabularyDataset:
        for word in vocabularyDataset:
            vocabulary[word.replace("\n", "")] = True  # just to mark an element as present


def initializeNonTerminalMapping():
    """
    Loads the nonTerminal's to integer key mappings from file
    """
    with open('./../data/projectFiles/nonTerminalsMapping', 'r') as nonTerminalMappingDataset:
        for line in nonTerminalMappingDataset:
            nonTerminal, indexString = line.split()
            nonTerminalsMapping[nonTerminal] = int(indexString)
            nonTerminalsMappingReversed[int(indexString)] = nonTerminal


def initializeStructures():
    """
    Initialize the structures used to perform the parsing
    """
    initializeRules()
    initializeVocabulary()
    initializeNonTerminalMapping()


def replaceOOVWords(words):
    """
    Replaces, in a list of words, the ones that are not in the parser's vocabulary with the "<unknown>" placeholder
    :param words: list to be analyzed
    :return: the corrected list
    """
    newWords = []
    for word in words:
        if word in vocabulary:
            newWords.append(word)
        else:
            newWords.append("<unknown>")
    return newWords


def splitNonTerminalRightHandSide(rightHandSide):
    """
    Splits the right hand side of a rule into the two non-terminals
    :param rightHandSide: right hand side  to be splitted
    :return: the two non-terminals
    """
    leftNonTerminal, rightNonTerminal = rightHandSide.split(" ", 1)
    return leftNonTerminal, rightNonTerminal


def buildTree(lowerPos, higherPos, symbolIndex, back):
    """
    From the search results recursively build the parsing tree
    :param lowerPos: word position in the sentence from which the current node's rule starts
    :param higherPos: word position in the sentence in which the current node's rule ends
    :param symbolIndex: index of the left hand side non-terminal symbol
    :param back: triangular pointer's table built during the probabilistic CYK parsing
    :return: the built tree
    """
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
    """
    Prints the tree as a string
    :param tree: tree to be printed
    :param words: initial sentence word's list
    :return: the string that represent the tree
    """
    if tree is None:
        return "()", 0
    if not tree.isTerminal:
        return "(" + tree.leftHandSide + " " + printTree(tree.left_rightHandSide, words) + printTree(
            tree.right_rightHandSide, words) + ")"
    else:
        return "(" + tree.leftHandSide + " " + words[tree.wordCounter] + ")"


def startProbabilisticCYK(words):
    """
    Performs the probabilistic parsing of a sentence
    :param words: sentence word's list
    :return: the obtained parse tree
    """
    words = replaceOOVWords(words)
    back = [[[None for _ in range(len(nonTerminalsMapping))] for _ in range(len(words) + 1)]
            for _ in range(len(words) + 1)]

    table = [[[- inf for _ in range(len(nonTerminalsMapping))] for _ in range(len(words) + 1)]
             for _ in range(len(words) + 1)]

    for j in range(1, len(words) + 1):
        # init with terminal rules
        for nonTerminal in invertedTerminalRules[words[j - 1]]:
            nonTerminalIndex = nonTerminalsMapping[nonTerminal]
            ruleValue = invertedTerminalRules[words[j - 1]][nonTerminal]
            table[j - 1][j][nonTerminalIndex] = ruleValue

        for i in range(j - 2, -1, -1):  # i ← j − 2 down to 0
            for k in range(i + 1, j):
                for leftNonTerminal in nonTerminalsMapping:
                    leftNonTerminalIndex = nonTerminalsMapping[leftNonTerminal]  # = B
                    # check first non-terminal in right hand side of the rule
                    if table[i][k][leftNonTerminalIndex] > -inf:
                        for rightNonTerminal in nonTerminalsMapping:
                            rightNonTerminalIndex = nonTerminalsMapping[rightNonTerminal]  # = C
                            # check second non-terminal in right hand side of the rule
                            if table[k][j][rightNonTerminalIndex] > -inf:
                                rightHandSide = leftNonTerminal + " " + rightNonTerminal
                                if rightHandSide in invertedNonTerminalRules:
                                    for leftHandSide in invertedNonTerminalRules[rightHandSide]:
                                        probability = invertedNonTerminalRules[rightHandSide][leftHandSide]
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
        return None, 0


initializeStructures()

with open('./../data/two_sentences.txt', 'r') as sentencesDataset:
    for sentence in sentencesDataset:
        words = sentence.split()
        tree, probability = startProbabilisticCYK(words)
        print(printTree(tree, words))
        print(probability)
fileNames = ["train", "test"]
for fileName in fileNames:
    with open('./../data/' + fileName + '/' + fileName + '.input.txt', 'r') as sentencesDataset:
        with open('./../data/results/' + fileName + ".system.txt", 'w') as outputDataset:
            for sentence in sentencesDataset:
                words = sentence.split()
                tree, probability = startProbabilisticCYK(words)
                print(printTree(tree, words), file=outputDataset)
