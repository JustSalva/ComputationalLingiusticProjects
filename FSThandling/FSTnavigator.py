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
    for i, word in enumerate(sentence):
        if word[4] > 0:  # word with a match

            next_state, nextOLabel = nextState(current_state, word[4], f)
            if next_state is not None:
                if indexFirstWord is None:
                    indexFirstWord = i

                current_state = next_state
                oLabel = nextOLabel
                if finalStates.isFinalState(oLabel):
                    temporary_match = oLabel
                    indexLastWord = i
            else:
                if temporary_match is not None:
                    matches.append((indexFirstWord, indexLastWord, temporary_match))
                    temporary_match = None
                indexFirstWord, indexLastWord = resetSequenceTaggers()
                current_state = initial_state
                oLabel = finalStates.NO_MATCH
        else:
            if temporary_match is not None:
                matches.append((indexFirstWord, indexLastWord, temporary_match))
                temporary_match = None
                current_state = initial_state
                oLabel = finalStates.NO_MATCH
            indexFirstWord, indexLastWord = resetSequenceTaggers()
    if temporary_match is not None:
        matches.append((indexFirstWord, indexLastWord, temporary_match))
        temporary_match = None
        current_state = initial_state
        oLabel = finalStates.NO_MATCH
    indexFirstWord, indexLastWord = resetSequenceTaggers()
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
"""
text= reader("data/train/input/train_22.input.tml")
sentence = [[(u'March', 21, 26, 'MONTH_IN_LETTERS', 12), (u'28', 27, 29, 'NUMBER', 6), (u',', 29, 30, 'COMMA', 38),
            (u'1935', 31, 35, 'NUMBER', 6), (u'United', 20462, 20468, 'NO_MATCH', 0),
            (u'March', 21, 26, 'MONTH_IN_LETTERS', 12), (u'28', 27, 29, 'NUMBER', 6), (u',', 29, 30, 'COMMA', 38),
            (u'1935', 31, 35, 'NUMBER', 6)]]
matches = analyzeEntireText(sentence, text)
print matches
"""
"""
for state in f.states():
    for arc in f.arcs(state):
        print arc.ilabel, arc.olabel, arc.nextstate
"""

