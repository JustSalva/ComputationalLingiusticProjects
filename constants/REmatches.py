"""
    file used to store the mapping between tag names and their corresponding integer codification in the FST
"""
NO_MATCH = -1
PARTIAL_MATCH = -2
EPSILON = 0
AM_PM = 1
AMBIGUOUS_NUMBER = 2
NOT_AMBIGUOUS_NUMBER_DAY = 3
NUMBER_DAY = 4
ORDINAL_NUMBERS = 5
NUMBER = 6
ORDINAL_NUMBERS_DAY = 7
NOT_AMBIGUOUS_DAY = 8
AGES = 9
TEMPORAL_POSITION = 10
TRIAD = 11
MONTH_IN_LETTERS = 12
DAYTIMES_PLURAL = 13
DAYTIMES_SINGULAR = 14
SEASON = 15
TIME_UNIT_PLURAL = 16
TIME_UNIT_SINGULAR = 17
NOT_AMBIGUOUS_YEARS = 18
DECADES = 19
ITERATION = 20
COMPARATOR = 21
APPROXIMATOR = 22
QUANTITY = 23
HHMM = 24
HOLIDAY = 25
THAN = 26
AT = 27
OF = 28
OLD = 29
LEAST = 30
RIGHT = 31
DAYTIME = 32
IN = 33
TEMPORAL_MOMENTS = 34
TEMP_EXPRESSION = 35
TIME_ZONES = 36
DASH = 37
COMMA = 38
COLUMN = 39
DOT = 40
SLASH = 41
THE = 42
DATE = 43
DURATION = 44
WEEK_DAY = 45
FALL = 46
PERIODICAL_ADVERB = 47


def getTagCode(tag):
    # type: (str) -> int
    """
    return the integer codification of a tag
    :param tag: tag name
    :return: its corresponding integer
    """
    if tag == "PARTIAL_MATCH": return PARTIAL_MATCH
    if tag == 'AM_PM': return AM_PM
    if tag == 'NUMBER': return NUMBER
    if tag == 'AMBIGUOUS_NUMBER': return AMBIGUOUS_NUMBER
    if tag == 'NOT_AMBIGUOUS_NUMBER_DAY': return NOT_AMBIGUOUS_NUMBER_DAY
    if tag == 'NUMBER_DAY': return NUMBER_DAY
    if tag == 'ORDINAL_NUMBERS': return ORDINAL_NUMBERS
    if tag == 'ORDINAL_NUMBERS_DAY': return ORDINAL_NUMBERS_DAY
    if tag == 'NOT_AMBIGUOUS_DAY': return NOT_AMBIGUOUS_DAY
    if tag == 'AGES': return AGES
    if tag == 'TEMPORAL_POSITION': return TEMPORAL_POSITION
    if tag == 'TRIAD': return TRIAD
    if tag == 'MONTH_IN_LETTERS': return MONTH_IN_LETTERS
    if tag == 'DAYTIMES_PLURAL': return DAYTIMES_PLURAL
    if tag == 'DAYTIMES_SINGULAR': return DAYTIMES_SINGULAR
    if tag == 'SEASON': return SEASON
    if tag == 'TIME_UNIT_PLURAL': return TIME_UNIT_PLURAL
    if tag == 'TIME_UNIT_SINGULAR': return TIME_UNIT_SINGULAR
    if tag == 'NOT_AMBIGUOUS_YEARS': return NOT_AMBIGUOUS_YEARS
    if tag == 'DECADES': return DECADES
    if tag == 'ITERATION': return ITERATION
    if tag == 'COMPARATOR': return COMPARATOR
    if tag == 'APPROXIMATOR': return APPROXIMATOR
    if tag == 'QUANTITY': return QUANTITY
    if tag == 'HHMM': return HHMM
    if tag == 'HOLIDAY': return HOLIDAY
    if tag == 'THAN': return THAN
    if tag == 'AT': return AT
    if tag == 'OF': return OF
    if tag == 'OLD': return OLD
    if tag == 'LEAST': return LEAST
    if tag == 'RIGHT': return RIGHT
    if tag == 'DAYTIME': return DAYTIME
    if tag == 'IN': return IN
    if tag == 'TEMPORAL_MOMENTS': return TEMPORAL_MOMENTS
    if tag == 'TEMP_EXPRESSION': return TEMP_EXPRESSION
    if tag == 'TIME_ZONES': return TIME_ZONES
    if tag == 'DASH': return DASH
    if tag == 'COMMA': return COMMA
    if tag == 'COLUMN': return COLUMN
    if tag == 'DOT': return DOT
    if tag == 'SLASH': return SLASH
    if tag == 'DURATION': return DURATION
    if tag == 'THE': return THE
    if tag == 'DATE': return DATE
    if tag == 'WEEK_DAY': return WEEK_DAY
    if tag == 'FALL': return FALL
    if tag == 'PERIODICAL_ADVERB': return PERIODICAL_ADVERB

    return 0  # no match
