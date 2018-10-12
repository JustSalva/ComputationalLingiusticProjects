import pywrapfst as fst
import constants.finalStatesConstants as finalStates

PATH_TO_FST = "timextractor.fst"


def nextState(state, inputLabel):
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
    current_state = f.states().value()
    oLabel = finalStates.NO_MATCH
    temporary_match = None
    indexFirstWord = None
    indexLastWord = None
    for i, word in enumerate(sentence):
        if word[4] >= 0:  # word with a match

            next_state, nextOLabel = nextState(current_state, word[4])
            if next_state is not None:
                if indexFirstWord is None:
                    indexFirstWord = i

                current_state = nextState
                oLabel = nextOLabel
                if finalStates.isFinalState(oLabel):
                    temporary_match = oLabel
                    indexLastWord = i
            else:
                if temporary_match is not None:
                    matches.append((indexFirstWord, indexLastWord, temporary_match))
                    temporary_match = None
                indexFirstWord, indexLastWord = resetSequenceTaggers()
        else:
            if temporary_match is not None:
                matches.append((indexFirstWord, indexLastWord, temporary_match))
                temporary_match = None
            indexFirstWord, indexLastWord = resetSequenceTaggers()

        return matches


def resetSequenceTaggers():
    return None, None


f = fst.Fst.read(PATH_TO_FST)
current_state = f.states().value()
print current_state
sentence = [(u'Italian', 0, 7, 'NO_MATCH', 0), (u'invasion', 8, 16, 'NO_MATCH', 0), (u'On', 18, 20, 'NO_MATCH', 0), (u'March', 21, 26, 'MONTH_IN_LETTERS', 12), (u'28', 27, 29, 'NUMBER', 6), (u',', 29, 30, 'COMMA', 38), (u'1935', 31, 35, 'NUMBER', 6), (u',', 35, 36, 'COMMA', 38), (u'General', 37, 44, 'NO_MATCH', 0), (u'Emilio', 45, 51, 'NO_MATCH', 0), (u'De', 52, 54, 'NO_MATCH', 0), (u'Bono', 55, 59, 'NO_MATCH', 0), (u'was', 60, 63, 'NO_MATCH', 0), (u'named', 64, 69, 'NO_MATCH', 0), (u'as', 70, 72, 'NO_MATCH', 0), (u'the', 73, 76, 'THE', 42), (u'Commander-in-Chief', 77, 95, 'PARTIAL_MATCH', 37), (u'of', 96, 98, 'OF', 28), (u'all', 99, 102, 'NO_MATCH', 0), (u'Italian', 103, 110, 'NO_MATCH', 0), (u'armed', 111, 116, 'NO_MATCH', 0), (u'forces', 117, 123, 'NO_MATCH', 0), (u'in', 124, 126, 'IN', 33), (u'East', 127, 131, 'TIME_ZONES', 36), (u'Africa', 132, 138, 'NO_MATCH', 0), (u'.', 138, 139, 'DOT', 40)]
matches = analyzeSentence(sentence)
print matches
"""
for state in f.states():
    for arc in f.arcs(state):
        print arc.ilabel, arc.olabel, arc.nextstate
"""
"""
sequenceOfInputs = [1,2,4]
for inputLabel in sequenceOfInputs:
    print "iteration: " + str(current_state) + str(inputLabel)
    current_state, olabel = nextState(current_state, inputLabel)
    print current_state
    if current_state is None:
        print "no path"
        break
print current_state
"""