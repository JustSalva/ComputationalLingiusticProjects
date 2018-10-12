import pywrapfst as fst
import constants.finalStatesConstants as finalStates

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
    arcs = f.arcs(state)
    for arc in arcs:
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


f = fst.Fst.read(PATH_TO_FST)
current_state = f.states().value()
print current_state
sentence = [ (u'March', 21, 26, 'MONTH_IN_LETTERS', 12), (u'28', 27, 29, 'NUMBER', 6), (u',', 29, 30, 'COMMA', 38), (u'1935', 31, 35, 'NUMBER', 6),(u'United', 20462, 20468, 'NO_MATCH', 0),  (u'March', 21, 26, 'MONTH_IN_LETTERS', 12), (u'28', 27, 29, 'NUMBER', 6), (u',', 29, 30, 'COMMA', 38), (u'1935', 31, 35, 'NUMBER', 6)]
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