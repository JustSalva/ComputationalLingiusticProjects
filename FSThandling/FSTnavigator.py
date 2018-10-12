import pywrapfst as fst

import constants.finalStatesConstants as finalStates
from XMLparsing.XMLparser import createTimeML, addItem, reader, writer
from constants.finalStatesConstants import printName

PATH_TO_FST = "timextractor.fst"


def nextState(state, inputLabel, f):
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
    return None, None


def analyzeEntireText(listOfSentences, text):
    resultTree = createTimeML()
    for sentence in listOfSentences:
        matches = analyzeSentence(sentence)
        for match in matches:
            initial_char = sentence[match[0]][1]
            final_char = sentence[match[1]][2]
            extracted_text = text[initial_char:final_char]
            addItem(resultTree, initial_char, final_char, printName(match[2]), extracted_text)
    return resultTree



text= reader("data/train/input/train_07.input.tml")
sentence = [[(u'At', 966, 968, 'AT', 27), (u'5:34', 969, 973, 'HHMM', 24), (u'AM', 974, 976, 'AM_PM', 1), (u'Baghdad', 977, 984, 'NO_MATCH', 0), (u'time', 985, 989, 'NO_MATCH', 0), (u'on', 990, 992, 'NO_MATCH', 0), (u'March', 993, 998, 'MONTH_IN_LETTERS', 12), (u'20', 999, 1001, 'NUMBER', 6), (u',', 1001, 1002, 'COMMA', 38), (u'2003', 1003, 1007, 'NUMBER', 6), (u'(', 1008, 1009, 'NO_MATCH', 0), (u'9:34', 1009, 1013, 'HHMM', 24), (u'p.m.', 1014, 1018, 'AM_PM', 1), (u',', 1018, 1019, 'COMMA', 38), (u'March', 1020, 1025, 'MONTH_IN_LETTERS', 12), (u'19', 1026, 1028, 'NUMBER', 6), (u'EST', 1029, 1032, 'TIME_ZONES', 36), (u')', 1032, 1033, 'NO_MATCH', 0), (u'the', 1034, 1037, 'THE', 42), (u'military', 1038, 1046, 'NO_MATCH', 0), (u'invasion', 1047, 1055, 'NO_MATCH', 0), (u'of', 1056, 1058, 'OF', 28), (u'Iraq', 1059, 1063, 'NO_MATCH', 0), (u'began', 1064, 1069, 'NO_MATCH', 0), (u'.', 1069, 1070, 'DOT', 40)]]

matches = analyzeEntireText(sentence, text)
print matches

"""
for state in f.states():
    for arc in f.arcs(state):
        print arc.ilabel, arc.olabel, arc.nextstate
"""
