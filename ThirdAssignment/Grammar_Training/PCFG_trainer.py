leftHandSideCounter = dict()  # dictionary of non terminal symbols appearing in the left hand side of the rule
ruleCounter = dict()  # contains key = left hand side, value = dict(key = left hand side, value = )


def incrementLeftHandSideCounter(nonTerminal):
    if nonTerminal in leftHandSideCounter:
        leftHandSideCounter[nonTerminal] += 1
    else:
        leftHandSideCounter[nonTerminal] = 1


def incrementRuleCounter(leftNonTerminal, rightRule):
    if leftNonTerminal in ruleCounter:
        if rightRule not in ruleCounter[leftNonTerminal]:
            ruleCounter[leftNonTerminal][rightRule] = 1
        else:
            ruleCounter[leftNonTerminal][rightRule] += 1
    else:
        ruleCounter[leftNonTerminal] = dict()
        ruleCounter[leftNonTerminal][rightRule] = 1


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
            incrementRuleCounter(tree[0], tree[1])  # tree[0] == label
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
#print(len(listOfTrees))
