EPSILON = 0
DATE = 1
DURATION = 2
SET = 3
TIME = 4
NO_MATCH = -1


def printName(state):
    # type: (int) -> str

    if state == 1:
        return "DATE"
    if state == 2:
        return "DURATION"
    if state == 3:
        return "SET"
    if state == 4:
        return "TIME"
    return "NO_MATCH"


def isFinalState(state):
    # type: (int) -> bool
    if 0 < state <= 4:
        return True
    return False
