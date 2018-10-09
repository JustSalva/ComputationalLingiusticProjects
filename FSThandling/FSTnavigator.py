import pywrapfst as fst
import constants.finalStatesConstants as finalStates

PATH_TO_FST = "example.fst"


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
    firstWord = None
    lastWord = None
    for i, word in enumerate(sentence):
        if word[4] >= 0:  # word with a match

            next_state, nextOLabel = nextState(current_state, word[4])
            if next_state is not None:
                if firstWord is None:
                    firstWord = i

                current_state = nextState
                oLabel = nextOLabel
                if finalStates.isFinalState(oLabel):
                    temporary_match = oLabel
                    lastWord = i
            else:
                if temporary_match is not None:
                    matches.append((firstWord, lastWord, temporary_match))
                    temporary_match = None
                firstWord, lastWord = resetSequenceTaggers()
        else:
            if temporary_match is not None:
                matches.append((firstWord, lastWord, temporary_match))
                temporary_match = None
            firstWord, lastWord = resetSequenceTaggers()

        return matches


def resetSequenceTaggers():
    return None, None


f = fst.Fst.read(PATH_TO_FST)
current_state = f.states().value()
print current_state
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