import pywrapfst as fst

f = fst.Fst.read("example.fst")

for state in f.states():
    for arc in f.arcs(state):
        print state, arc.ilabel, arc.olabel, arc.weight, arc.nextstate

f.draw("f.gv")