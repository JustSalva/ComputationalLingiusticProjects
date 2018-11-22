leftHandSideCounter = dict()  # dictionary of non terminal symbols appearing in the left hand side of the rule
ruleCounter = dict()  # contains key = left hand side, value = dict(key = left hand side, value = )
terminalCounter = dict()


def incrementDictionary(key, dictionary):
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1


def incrementLeftHandSideCounter(nonTerminal):
    incrementDictionary(nonTerminal, leftHandSideCounter)


def incrementTerminalCounter(terminal):
    incrementDictionary(terminal, terminalCounter)


def incrementRuleCounter(leftNonTerminal, rightRule):
    global numberOfRules
    if leftNonTerminal in ruleCounter:
        if rightRule not in ruleCounter[leftNonTerminal]:
            ruleCounter[leftNonTerminal][rightRule] = 1
            numberOfRules += 1
        else:
            ruleCounter[leftNonTerminal][rightRule] += 1
    else:
        ruleCounter[leftNonTerminal] = dict()
        ruleCounter[leftNonTerminal][rightRule] = 1
        numberOfRules += 1


def printRules(filepath):
    rulesSumOfProbabilities = dict()
    if(filepath != None):
        with open(filepath, 'w') as dataset:
            for leftHandSide in ruleCounter:
                sum = 0
                for rightHandSide in ruleCounter[leftHandSide]:
                    probability = ruleCounter[leftHandSide][rightHandSide] / leftHandSideCounter[leftHandSide]
                    print(leftHandSide + " → " + rightHandSide + " [" + str(probability) + "]", file=dataset)
                    sum += probability
                rulesSumOfProbabilities[leftHandSide] = sum
    else:
        for leftHandSide in ruleCounter:
            sum = 0
            for rightHandSide in ruleCounter[leftHandSide]:
                probability = ruleCounter[leftHandSide][rightHandSide] / leftHandSideCounter[leftHandSide]
                print(leftHandSide + " → " + rightHandSide + " [" + str(probability) + "]", file=dataset)
                sum += probability
            rulesSumOfProbabilities[leftHandSide] = sum
    return rulesSumOfProbabilities

def printRequestedRules(listOfRulesLeftHandSizeToPrint):
    for leftHandSide in listOfRulesLeftHandSizeToPrint:
        print("Rules with " + leftHandSide + " as left hand side")
        for rightHandSide in ruleCounter[leftHandSide]:
            probability = ruleCounter[leftHandSide][rightHandSide] / leftHandSideCounter[leftHandSide]
            print(leftHandSide + " → " + rightHandSide + " [" + str(probability) + "]")
def readTree(text, ind):
    # verbose = True
    """The basic idea here is to represent the file contents as a long string
    and iterate through it character-by-character (the 'ind' variable
    points to the current character). Whenever we get to a new tree,
    we call the function again (recursively) to read it in."""
    # Reading new subtree

    # consume any spaces before the tree
    while text[ind].isspace():
        ind += 1

    if text[ind] == "(":
        # Found open parenthesis
        tree = []
        ind += 1

        # record the label after the paren
        label = ""
        while not text[ind].isspace() and text != "(":
            label += text[ind]
            ind += 1
        incrementLeftHandSideCounter(label)
        tree.append(label)
        # Read in label "label"

        # read in all subtrees until right paren
        subtree = True
        while subtree:
            # if this call finds only the right paren it'll return False
            subtree, ind = readTree(text, ind)
            if subtree:
                tree.append(subtree)

        # consume the right paren itself
        ind += 1
        assert (text[ind] == ")")
        ind += 1
        if (len(tree) == 2):
            # rule of type "A-> terminal"
            terminal = tree[1]
            incrementRuleCounter(tree[0], terminal)  # tree[0] == label
            incrementTerminalCounter(terminal)
        elif (len(tree) == 3):
            # rule of type "A-> BC"
            rightHandSide = tree[1][0] + " " + tree[2][0]
            incrementRuleCounter(tree[0], rightHandSide)

        # End of tree "tree"

        return tree, ind

    elif text[ind] == ")":
        # there is no subtree here; this is the end paren of the parent tree
        # which we should not consume
        ind -= 1
        return False, ind

    else:
        # the subtree is just a terminal (a word)
        word = ""
        while not text[ind].isspace() and text[ind] != ")":
            word += text[ind]
            ind += 1

        # Read in word: "word"

        return word, ind


listOfTrees = []
numberOfRules = 0
with open('./../data/train/train.unknown.txt', 'r') as dataset:
    for line in dataset:
        ind = 0

        while ind < len(line) - 1:
            tree, ind = readTree(line, ind)
            listOfTrees.append(tree)
            # print(tree)
            # print(leftHandSideCounter)
            # print(ruleCounter)
print("leftHandSideCounter: " + str(leftHandSideCounter))
print("ruleCounter: " + str(ruleCounter))
print("number of nonterminals = " + str(len(leftHandSideCounter)))
print("number of terminals = " + str(len(terminalCounter)))
print("number of rules: " + str(numberOfRules))
listOfRulesLeftHandSizeToPrint = ["QP", "WRB"]
rulesSumOfProbabilities = printRules("./../data/projectFiles/rules")
printRequestedRules(listOfRulesLeftHandSizeToPrint)
print("sum of probabilities for each rule's left hand size: " + str(rulesSumOfProbabilities))

