import pywrapfst as fst

import constants.finalStatesConstants as finalStates
from XMLparsing.XMLparser import createTimeML, addItem, reader
from constants.finalStatesConstants import printName

PATH_TO_FST = "FSTfiles/timextractor.fst"


def nextState(state, inputLabel, f):
    # type: (int, int, object) -> fst.Fst
    """
    Given the current state, and the label received in input,
    returns the state, if exist, in which the transition lead
    :param state: current state
    :param inputLabel: label to process
    :return: the number of the next state and its output label, or
             None if it does not exist
    """
    for arc in f.arcs(state):
        if arc.ilabel == inputLabel:
            return arc.nextstate, arc.olabel
    return None, None


def analyzeSentence(sentence):
    """
    analyze a tagged sentence and return the found temporal expressions
    :param sentence: sentence tagged to be analyzed
    :return: list of matches
    """
    matches = []
    f = fst.Fst.read(PATH_TO_FST)
    initial_state = f.states().value()
    current_state = initial_state
    oLabel = finalStates.NO_MATCH
    temporary_match = None
    indexFirstWord = None
    indexLastWord = None
    recursive = False
    print sentence
    for i, word in enumerate(sentence):
        if word[4] > 0:  # word with a match

            next_state, nextOLabel = nextState(current_state, word[4], f)
            print "next_state: "+ str(next_state)
            if next_state is not None:
                if indexFirstWord is None:
                    indexFirstWord = i

                current_state = next_state
                oLabel = nextOLabel
                if finalStates.isFinalState(oLabel):
                    temporary_match = oLabel
                    print "temporary match" + str(temporary_match)
                    indexLastWord = i
            else:
                if indexFirstWord is not None:
                    recursive_index = indexFirstWord + 1
                    print "match" + str(temporary_match)
                    if temporary_match is not None:
                        matches.append((indexFirstWord, indexLastWord, temporary_match))
                        temporary_match = None
                        recursive_index = indexLastWord + 1
                    indexFirstWord, indexLastWord = resetSequenceTaggers()
                    current_state = initial_state
                    oLabel = finalStates.NO_MATCH
                    recursive = True
                    print "recursion index:" + str(recursive_index)
                    break
        else:
            if temporary_match is not None:
                matches.append((indexFirstWord, indexLastWord, temporary_match))
                print "match" + str(temporary_match)
                temporary_match = None
            elif indexFirstWord is not None:
                recursive_index = indexFirstWord + 1
                print "no match for path "
                indexFirstWord, indexLastWord = resetSequenceTaggers()
                current_state = initial_state
                oLabel = finalStates.NO_MATCH
                recursive = True
                print "recursion index:" + str(recursive_index)
                break
            current_state = initial_state
            oLabel = finalStates.NO_MATCH
            indexFirstWord, indexLastWord = resetSequenceTaggers()
    if recursive == True:
        return analyzeSentenceAfterWrongPath(sentence, recursive_index, matches)
    if temporary_match is not None:
        matches.append((indexFirstWord, indexLastWord, temporary_match))
        print "match" + str(temporary_match)
        temporary_match = None
        current_state = initial_state
        oLabel = finalStates.NO_MATCH
        indexFirstWord, indexLastWord = resetSequenceTaggers()
        print matches
    return matches


def analyzeSentenceAfterWrongPath(sentence, start_index, matches):
    """
    same behaviour as analyze sentence but this method is used to perform recursive calls
    after a false match(= path without a final transition)
    :param sentence: sentence tagged to be analyzed
    :param start_index: index of the sentence from which the analysis must start
    :param matches: matches already found before the recursive call
    :return: list of matches
    """
    f = fst.Fst.read(PATH_TO_FST)
    initial_state = f.states().value()
    current_state = initial_state
    oLabel = finalStates.NO_MATCH
    temporary_match = None
    indexFirstWord = None
    indexLastWord = None
    i = start_index
    recursive = False
    for word in sentence[start_index:]:
        if word[4] > 0:  # word with a match

            next_state, nextOLabel = nextState(current_state, word[4], f)
            print "next_state: " + str(next_state)
            if next_state is not None:
                if indexFirstWord is None:
                    indexFirstWord = i

                current_state = next_state
                oLabel = nextOLabel
                if finalStates.isFinalState(oLabel):
                    temporary_match = oLabel
                    print "temporary match" + str(temporary_match)
                    indexLastWord = i
            else:
                if indexFirstWord is not None:
                    recursive_index = indexFirstWord + 1
                    print "match" + str(temporary_match)
                    if temporary_match is not None:
                        matches.append((indexFirstWord, indexLastWord, temporary_match))
                        temporary_match = None
                        recursive_index = indexLastWord + 1
                    indexFirstWord, indexLastWord = resetSequenceTaggers()
                    current_state = initial_state
                    oLabel = finalStates.NO_MATCH
                    recursive = True
                    print "recursion index:" + str(recursive_index)
                    break
        else:
            if temporary_match is not None:
                matches.append((indexFirstWord, indexLastWord, temporary_match))
                print "match" + str(temporary_match)
                temporary_match = None
            elif indexFirstWord is not None:
                recursive_index = indexFirstWord + 1
                print "no match for path "
                indexFirstWord, indexLastWord = resetSequenceTaggers()
                current_state = initial_state
                oLabel = finalStates.NO_MATCH
                recursive = True
                print "recursion index:" + str(recursive_index)
                break
            current_state = initial_state
            oLabel = finalStates.NO_MATCH
            indexFirstWord, indexLastWord = resetSequenceTaggers()
        i += 1
    if recursive == True:
        return analyzeSentenceAfterWrongPath(sentence, recursive_index, matches)
    if temporary_match is not None:
        matches.append((indexFirstWord, indexLastWord, temporary_match))
        print "match" + str(temporary_match)
        temporary_match = None
        current_state = initial_state
        oLabel = finalStates.NO_MATCH
        indexFirstWord, indexLastWord = resetSequenceTaggers()
    print matches
    return matches


def resetSequenceTaggers():
    """
    Auxiliary function to set to None the match taggers
    """
    return None, None


def analyzeEntireText(listOfSentences, text):
    """
    Recursively analyze and search for tags into a tagged and tokenized text
    :param listOfSentences: tagged text
    :param text: original text
    :return: a XML tree with the results
    """
    resultTree = createTimeML()
    for sentence in listOfSentences:
        matches = analyzeSentence(sentence)
        for match in matches:
            initial_char = sentence[match[0]][1]
            final_char = sentence[match[1]][2]
            extracted_text = text[initial_char:final_char]
            addItem(resultTree, initial_char, final_char, printName(match[2]), extracted_text)
    return resultTree


"""
text= reader("data/train/input/train_01.input.tml")
sentence = [[(u'ended', 1171, 1176, 'PARTIAL_MATCH', -2), (u'in', 1177, 1179, 'IN', 33), (u'March', 1180, 1185, 'MONTH_IN_LETTERS', 12), (u'1940', 1186, 1190, 'NOT_AMBIGUOUS_YEARS', 18), (u'with', 1191, 1195, 'NO_MATCH', 0)]]
matches = analyzeEntireText(sentence, text)
print matches
"""

"""
for state in f.states():
    for arc in f.arcs(state):
        print arc.ilabel, arc.olabel, arc.nextstate
"""
