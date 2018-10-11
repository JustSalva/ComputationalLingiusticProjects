import re
import constants.REconstants as constants
import constants.REmatches as tagMatch

class regularExpressions:

    def __init__(self):
        self.reList = []

        __STRING_AM_PM = '(a\.?|p\.?)m\.?'
        self.reList.append(('AM_PM', re.compile('(?<!\S)('+__STRING_AM_PM+')(?!\S)', flags=re.IGNORECASE)))
        __STRING_NUMBERS = '((([1-9][0-9]*)|[1-9]|0[1-9]))'
        self.reList.append(('NUMBER',
                            re.compile('(' + __STRING_NUMBERS + ')',
                                flags=re.IGNORECASE)))  # NB check always after ordinal numbers!
        self.reList.append(('NUMBER_IN_LETTER',
                            re.compile(constants.NUMBERS_IN_LETTER,
                                flags=re.IGNORECASE)))  # NB check always after ordinal numbers!

        # numbers from 1 to 12 even with a zero before for one-digit numbers
        self.reList.append(('AMBIGUOUS_NUMBER', re.compile('0[1-9]|1[0-2]|[1-9]')))
        __STRING_NOT_AMBIGUOUS_NUMBER_DAY = '1[3-9]|2[0-9]|3[0-1]'
        self.reList.append(('NOT_AMBIGUOUS_NUMBER_DAY', re.compile(__STRING_NOT_AMBIGUOUS_NUMBER_DAY)))

        __STRING_NUMBER_DAY = '([1-2][0-9]|3[0-1]|0[1-9]|((?<!\S)\d{1}(?!\S)))'
        self.reList.append(('NUMBER_DAY', re.compile(__STRING_NUMBER_DAY)))
        __STRING_ORDINAL_TAGS = '(st|nd|rd|th)'

        __STRING_ORDINAL_NUMBERS = __STRING_NUMBERS + __STRING_ORDINAL_TAGS
        self.reList.append(('ORDINAL_NUMBERS',
                            re.compile('(' + __STRING_ORDINAL_NUMBERS + ')|('+constants.ORDINALS_IN_LETTER + ')',
                                       flags=re.IGNORECASE)))

        self.reList.append(('NUMBER',
                            re.compile('(' + __STRING_NUMBERS + ')|(' + '\b('+constants.NUMBERS_IN_LETTER + ')\b'+')',
                                       flags=re.IGNORECASE)))  # NB check always after ordinal numbers!

        __STRING_ORDINAL_NUMBERS_DAY = __STRING_NUMBER_DAY + __STRING_ORDINAL_TAGS
        self.reList.append(('ORDINAL_NUMBERS_DAY', re.compile(__STRING_ORDINAL_NUMBERS_DAY, flags=re.IGNORECASE)))

        self.reList.append(('NOT_AMBIGUOUS_DAY',
                            re.compile(__STRING_NOT_AMBIGUOUS_NUMBER_DAY + __STRING_ORDINAL_TAGS + '?',
                                       flags=re.IGNORECASE)))  # NB ambiguous to be handled
        __STRING_AGES = 'A\.?D\.?|B\.?C\.?|C\.?E\.?|B\.?C\.?E\.?'
        self.reList.append(('AGES', re.compile('(?<!\S)('+__STRING_AGES+')(?!\S)', flags=re.IGNORECASE)))

        __STRING_TRIAD = 'present|future|past'
        __STRING_TEMPORAL_POSITION = 'next|last|previous|following|final|' + __STRING_TRIAD
        self.reList.append(('TEMPORAL_POSITION', re.compile(__STRING_TEMPORAL_POSITION, flags=re.IGNORECASE)))
        self.reList.append(('TRIAD', re.compile(__STRING_TRIAD, flags=re.IGNORECASE)))

        self.reList.append(
            ('MONTH_IN_LETTERS', re.compile('('+constants.MONTHS+')$', flags=re.IGNORECASE)))  # NB rules for ambiguity
        self.reList.append(('DAYTIMES_PLURAL', re.compile(constants.DAYTIMES_PLURAL, flags=re.IGNORECASE)))
        self.reList.append(('DAYTIMES_SINGULAR', re.compile(constants.DAYTIMES_SINGULAR, flags=re.IGNORECASE)))
        self.reList.append(('SEASON', re.compile(constants.SEASON, flags=re.IGNORECASE)))
        self.reList.append(('TIME_UNIT_PLURAL', re.compile('hours|days|weeks|months|years|hrs',
                                                           flags=re.IGNORECASE)))  # NB match before singular
        __STRING_TIMEUNIT_SINGULAR = 'day|month|year|decade|century|week| ' + constants.DAYTIMES_SINGULAR
        self.reList.append(('TIME_UNIT_SINGULAR', re.compile(__STRING_TIMEUNIT_SINGULAR)))

        self.reList.append(('NOT_AMBIGUOUS_YEARS',
                            re.compile('([1-9][0-9]{3,10}|(3[2-9]|[4-9][0-9])('+__STRING_AGES+')?)|\'[0-9][0-9]')))
        self.reList.append(('DECADES',
                            re.compile('[1-9][0-9]{3,10}s')))
        self.reList.append(('ITERATION', re.compile('(?<!\S)(every|each)(?!\S)', flags=re.IGNORECASE)))

        self.reList.append(('COMPARATOR', re.compile('(?<!\S)(more|less)(?!\S)', flags=re.IGNORECASE)))

        self.reList.append(('APPROXIMATOR', re.compile('another|about|nearly|around', flags=re.IGNORECASE)))

        self.reList.append(('QUANTITY', re.compile('several|hundred|thousand|(?<!\S)a(?!\S)|few|lot', flags=re.IGNORECASE)))
        __STRING_TIME = '((1[0-9]|2[0-4]|0[0-9]|((?<!\S)[0-9])):([0-5][0-9]|([1-9](?!\S))))(' + __STRING_AM_PM + ')?'
        self.reList.append(('TIME', re.compile(__STRING_TIME, flags=re.IGNORECASE)))

        self.reList.append(('HOLIDAY', re.compile('\b('+constants.HOLIDAYS+')\b', flags=re.IGNORECASE)))

        self.reList.append(('THAN', re.compile('(?<!\S)than(?!\S)', flags=re.IGNORECASE)))
        self.reList.append(('AT', re.compile('(?<!\S)at(?!\S)', flags=re.IGNORECASE)))
        self.reList.append(('OF', re.compile('(?<!\S)of(?!\S)', flags=re.IGNORECASE)))
        self.reList.append(('OLD', re.compile('(?<!\S)old(?!\S)', flags=re.IGNORECASE)))
        self.reList.append(('LEAST', re.compile('(?<!\S)least(?!\S)', flags=re.IGNORECASE)))
        self.reList.append(('RIGHT', re.compile('(?<!\S)right(?!\S)', flags=re.IGNORECASE)))
        self.reList.append(('DAYTIME', re.compile('(?<!\S)daytime(?!\S)', flags=re.IGNORECASE)))
        self.reList.append(('IN', re.compile('(?<!\S)in(?!\S)', flags=re.IGNORECASE)))

        self.reList.append(('TEMPORAL_MOMENTS',
                            re.compile(
                                'now|time|tonight|current|recently|currently|today|tomorrow|yesterday|coming|previously',
                                flags=re.IGNORECASE)))

        self.reList.append(('TEMP_EXPRESSION', re.compile(
            'later|earlier|start|middle|early|late|end|beginning|same|ago|this|' + __STRING_TEMPORAL_POSITION,
            flags=re.IGNORECASE)))  # NB. sempre dopo temporal position
        # punctuation
        self.reList.append(('TIME_ZONES', re.compile('(?<!\S)('+constants.TIME_ZONES+')(?!\S)', flags=re.IGNORECASE)))
        self.reList.append(('DASH', re.compile('-')))
        self.reList.append(('COMMA', re.compile(',')))
        self.reList.append(('COLUMN', re.compile(':')))
        self.reList.append(('DOT', re.compile('\.')))
        self.reList.append(('SLASH', re.compile('/')))
        self.reList.append(('DURATION',
                            re.compile('(([1-9][0-9]{3}-[1-9][0-9]{3})|((' + constants.NUMBERS_IN_LETTER + '|'
                                       + '[1-9][0-9]*)-(' + __STRING_TIMEUNIT_SINGULAR + '))|' + __STRING_TIME
                                       + '-' + __STRING_TIME + 'hrs)', flags=re.IGNORECASE)))
        self.reList.append(('THE', re.compile('the')))
        pass

    def checkRE(self, string):
        max_length = 0
        length = 0
        elementExtracted = None
        tag = None
        for elem in self.reList:
            for result in re.finditer(elem[1], string):
                length = result.span()[1] - result.span()[0]
                if length > max_length:
                    elementExtracted = result.group()
                    tag = elem[0]
                    max_length = length
                # print result.group(), result.span(), elem[0]
        if tag is None:
            return "NO_MATCH", tagMatch.getTagCode(tag)
        if elementExtracted != string:
            print constants.WARNING_COLOR + 'WARNING: \"' + elementExtracted + '\" does not entirely match the string: \"' + string +'\"'+ constants.STANDARD_COLOR
            print tag
            return "PARTIAL_MATCH", tagMatch.getTagCode(tag)
        return tag, tagMatch.getTagCode(tag)


# TEST LINES
"""
for elem in re.finditer(re.compile('(([1-9][0-9]{3}-[1-9][0-9]{3})|((' + constants.NUMBERS_IN_LETTER + '|'
                                       + '[1-9][0-9]*)-' + __STRING_TIMEUNIT_SINGULAR + ')|' + __STRING_TIME
                                       + '-' + __STRING_TIME + 'hrs)', flags=re.IGNORECASE), 'three-month'):
    print elem.group(), elem.span()
"""
a = regularExpressions()
print (regularExpressions.checkRE(a, "three-year"))


