DATE = 0
DURATION = 1
SET = 2
TIME = 3
NO_MATCH = -1


def printName(state):
    # type: (int) -> str

    if state == 0:
        return "DATE"
    if state == 1:
        return "DURATION"
    if state == 2:
        return "SET"
    if state == 3:
        return "TIME"
    return "NO_MATCH"


def isFinalState(state):
    # type: (int) -> bool
    if 0 < state < 4:
        return True
    return False
