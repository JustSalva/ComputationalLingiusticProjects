wordTags = dict()


def loadWordTagMapping():
    with open('./../results/3/baselineTaggerWordTagAssociations', 'r') as dataset:
        for line in dataset:
            # add every word to the dictionary (added only if its support reaches value 4)
            word, tag = line.split()
            wordTags[word] = tag


