possibleTags = 'CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB', '$', '#', '``', '\'\'', '-LRB-', '-RRB-', ',', '.', ':'
#possibleTags = [line.rstrip('\n') for line in open('dataSets/Penn_TreeBank_tagSet_TAGS')]
# loading from file ignored cause it would happen every time a utility function is called

def isInTagSet(tag):
    return tag in possibleTags

def splitWordAndToken(token):
    word, tag = token.split('/', 1)
    if not isInTagSet(tag):
        word, tag = handleMultipleSlashes(token)
    return word, tag

def handleMultipleSlashes(token):
    i = 0
    found = False
    while not found:
        i += 1
        split = token.split('/', i)
        temp_word = '/'.join(split[:i])
        temp_tag = split[i]
        if isInTagSet(temp_tag):
            found = True
    return temp_word, temp_tag