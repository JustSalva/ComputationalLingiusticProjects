import re
import constants

# punctuation
DASH = re.compile('-')
COMMA = re.compile(',')
COLUMN = re.compile(':')
DOT = re.compile('.')
SLASH = re.compile('/')
# numbers from 1 to 12 even with a zero before for one-digit numbers
AMBIGUOUS_NUMBER = re.compile('0[1-9]|1[0-2]|[1-9]')
STRING_NOT_AMBIGUOUS_NUMBER_DAY = '1[3-9]|2[0-9]|3[0-1]'
NOT_AMBIGUOUS_NUMBER_DAY = re.compile(STRING_NOT_AMBIGUOUS_NUMBER_DAY)

STRING_NUMBER_DAY = '([0-2][0-9]|3[0-1]|((?<!\S)\d{1}(?!\S)))'
NUMBER_DAY = re.compile(STRING_NUMBER_DAY)
STRING_ORDINAL_TAGS = '(st|nd|rd|th)'

STRING_NUMBERS = '((([1-9][0-9]*)|[1-9]|0[1-9]))'
STRING_ORDINAL_NUMBERS = STRING_NUMBERS + STRING_ORDINAL_TAGS
ORDINAL_NUMBERS = re.compile('(' + STRING_ORDINAL_NUMBERS + ')|(' + constants.ORDINALS_IN_LETTER + ')',
                             flags=re.IGNORECASE)

NUMBER = re.compile('(' + STRING_NUMBERS + ')|(' + constants.NUMBERS_IN_LETTER + ')',
                    flags=re.IGNORECASE)  # NB check always after ordinal numbers!

STRING_ORDINAL_NUMBERS_DAY = STRING_NUMBER_DAY + STRING_ORDINAL_TAGS
ORDINAL_NUMBERS_DAY = re.compile(STRING_ORDINAL_NUMBERS_DAY, flags=re.IGNORECASE)

NOT_AMBIGUOUS_DAY = re.compile(STRING_NOT_AMBIGUOUS_NUMBER_DAY + STRING_ORDINAL_TAGS + '?',
                               flags=re.IGNORECASE)  # NB ambiguous to be handled

AGES = re.compile('A\.?D\.?|B\.?C\.?|C\.?E\.?|B\.?C\.?E\.?', flags=re.IGNORECASE)

STRING_TRIAD = 'present|future|past'
STRING_TEMPORAL_POSITION = 'next|last|previous|following|final|' + STRING_TRIAD
TEMPORAL_POSITION = re.compile(STRING_TEMPORAL_POSITION, flags=re.IGNORECASE)
TRIAD = re.compile(STRING_TRIAD, flags=re.IGNORECASE)

MONTH_IN_LETTERS = re.compile(constants.MONTHS, flags=re.IGNORECASE)  # NB rules for ambiguity
DAYTIMES_PLURAL = re.compile(constants.DAYTIMES_PLURAL, flags=re.IGNORECASE)
DAYTIMES_SINGULAR = re.compile(constants.DAYTIMES_SINGULAR, flags=re.IGNORECASE)
SEASON = re.compile(constants.SEASON, flags=re.IGNORECASE)
TIME_UNIT_PLURAL = re.compile('hours|days|weeks|months|years|hrs', flags=re.IGNORECASE) # NB match before singular
TIME_UNIT_SINGULAR = re.compile(
    'day|month|year|decade|century|week|' + constants.MONTHS + '|' + constants.SEASON + '|' + constants.DAYTIMES_SINGULAR)


NOT_AMBIGUOUS_YEARS = re.compile('[1-9][0-9]{3,10}|(3[2-9]|[4-9][0-9])')  # TODO

STRING_AM_PM = '(a\.?|p\.?)m\.?'
AM_PM = re.compile(STRING_AM_PM, flags=re.IGNORECASE)

ITERATION = re.compile('every|each', flags=re.IGNORECASE)

COMPARATOR = re.compile('more|less', flags=re.IGNORECASE)

APPROXIMATOR = re.compile('another|about|nearly|around', flags=re.IGNORECASE)

QUANTITY = re.compile('several|hundred|thousand|a|few|lot', flags=re.IGNORECASE)

TIME = re.compile('((1[0-9]|2[0-4]|0[0-9]|(?<!\S)[0-9]):([0-5][0-9]|([1-9](?!\S))))('+STRING_AM_PM+')', flags=re.IGNORECASE)

HOLIDAY = re.compile(constants.HOLIDAYS, flags=re.IGNORECASE)

THAN = re.compile('than', flags=re.IGNORECASE)
AT = re.compile('at', flags=re.IGNORECASE)
OF = re.compile('of', flags=re.IGNORECASE)
OLD = re.compile('old', flags=re.IGNORECASE)
LEAST = re.compile('least', flags=re.IGNORECASE)
RIGHT = re.compile('right', flags=re.IGNORECASE)
DAYTIME = re.compile('daytime', flags=re.IGNORECASE)
IN = re.compile('in', flags=re.IGNORECASE)

TEMPORAL_MOMENTS = re.compile(
    'now|time|tonight|current|recently|currently|today|tomorrow|yesterday|coming|previously', flags=re.IGNORECASE)

TEMP_EXPRESSION = re.compile('start|middle|early|late|end|beginning|same|ago|this|'+STRING_TEMPORAL_POSITION, flags=re.IGNORECASE) #NB. sempre dopo temporal position


TIME_ZONES = re.compile(constants.TIME_ZONES, flags=re.IGNORECASE)

# TEST LINES

for elem in re.finditer(TEMP_EXPRESSION, '0:58a.m.start'):
    print elem.group(), elem.span()
