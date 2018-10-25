EPSILON = 0
DATE = 1
DURATION = 2
SET = 3
TIME = 4
NO_MATCH = -1


def printName(state):
    # type: (int) -> str
    """
    Prints the string name of the final states
    :param state: state codified as integer
    :return: the name as a string
    """
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
    """
    checks if the state code represent a final state of the FST
        :param state: code to be checked
        :return: the answer as a boolean
        """
    if 0 < state <= 4:
        return True
    return False
