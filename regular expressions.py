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
ORDINAL_NUMBERS = re.compile('('+STRING_ORDINAL_NUMBERS+')|('+constants.ORDINALS_IN_LETTER+')', flags=re.IGNORECASE)

NUMBER = re.compile('('+STRING_NUMBERS+')|('+constants.NUMBERS_IN_LETTER+')', flags=re.IGNORECASE)   #NB check always after ordinal numbers!



STRING_ORDINAL_NUMBERS_DAY = STRING_NUMBER_DAY + STRING_ORDINAL_TAGS
ORDINAL_NUMBERS_DAY = re.compile(STRING_ORDINAL_NUMBERS_DAY, flags=re.IGNORECASE)

NOT_AMBIGUOUS_DAY = re.compile(STRING_NOT_AMBIGUOUS_NUMBER_DAY+STRING_ORDINAL_TAGS+'?', flags=re.IGNORECASE)  # NB ambiguous to be handled


AGES = re.compile('A\.?D\.?|B\.?C\.?|C\.?E\.?|B\.?C\.?E\.?', flags=re.IGNORECASE)

STRING_TERNA = 'present|future|past'
TEMPORAL_POSITION = re.compile('next|last|previous|following|final|'+STRING_TERNA, flags=re.IGNORECASE)
TERNA = re.compile(STRING_TERNA, flags=re.IGNORECASE)

MONTH_IN_LETTERS = re.compile(constants.MONTHS, flags=re.IGNORECASE)  # NB rules for ambiguity
DAYTIMES = re.compile(constants.DAYTIMES, flags=re.IGNORECASE)
SEASON = re.compile(constants.SEASON, flags=re.IGNORECASE)
TIME_UNIT_SINGULAR = re.compile('day|month|year|decade|century|week|'+constants.MONTHS+'|'+constants.SEASON+'|'+constants.DAYTIMES)


NOT_AMBIGUOUS_YEARS = re.compile('[1-9][0-9]{3,10}|(3[2-9]|[4-9][0-9])') #CONTINUE
# TEST LINES

for elem in re.finditer(NOT_AMBIGUOUS_YEARS,"-d-fefegf01THg45-tjanu1000ary32a11ryhirJweekANfalluaryteFutURe1thensixthpresent 1001100folloadwingfuturethegC.E.geg"):
    print elem.group(), elem.span()
