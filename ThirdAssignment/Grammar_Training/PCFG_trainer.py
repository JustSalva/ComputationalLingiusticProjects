leftHandSideCounter = dict()  # dictionary of non terminal symbols appearing in the left hand side of the rule
ruleCounter = dict() # contains key = left hand side, value = dict(key = left hand side, value = )


def readTree(text, ind, verbose=False):
    """The basic idea here is to represent the file contents as a long string
    and iterate through it character-by-character (the 'ind' variable
    points to the current character). Whenever we get to a new tree,
    we call the function again (recursively) to read it in."""
    if verbose:
        print("Reading new subtree", text[ind:][:10])

    # consume any spaces before the tree
    while text[ind].isspace():
        ind += 1

    if text[ind] == "(":
        if verbose:
            print("Found open paren")
        tree = []
        ind += 1

        # record the label after the paren
        label = ""
        while not text[ind].isspace() and text != "(":
            label += text[ind]
            ind += 1

        tree.append(label)
        if verbose:
            print("Read in label:", label)

        # read in all subtrees until right paren
        subtree = True
        while subtree:
            # if this call finds only the right paren it'll return False
            subtree, ind = readTree(text, ind, verbose=verbose)
            if subtree:
                tree.append(subtree)

        # consume the right paren itself
        ind += 1
        assert(text[ind] == ")")
        ind += 1

        if verbose:
            print("End of tree", tree)

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

        if verbose:
            print("Read in word:", word)

        return word, ind

if __name__ == "__main__":
    ff = open("/home/justsalva/PycharmProjects/ComputationalLinguistic/ThirdAssignment/data/train/train.unknown.txt")
    filetxt = "".join(ff.readlines())

    #read all the trees in a file
    ind = 0
    while ind < len(filetxt) - 1:
        tree, ind = readTree(filetxt, ind)
        print(tree)
        # print "new ind", ind