import pywrapfst as fst


def nextState(current_state, required_next_state):
    for arc in f.arcs(current_state):
        next_state = arc.nextstate
        if next_state == required_next_state:
            return arc.nextstate, arc.olabel
    return None


f = fst.Fst.read("example.fst")
sequence = [1, 2, 3, 4, 5]
current_state = f.states().value()
print current_state
"""
for state in f.states():
    for arc in f.arcs(state):
        print arc.ilabel, arc.olabel, arc.nextstate
"""

for elem in sequence:
    print "iteration: "+ str(current_state) + str(elem)
    current_state, olabel = nextState(current_state, elem)
    print current_state
    if current_state is None:
        print "no path"
        break
print current_state