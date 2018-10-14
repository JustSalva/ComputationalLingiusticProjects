from nltk.tokenize import sent_tokenize, word_tokenize
import XMLparsing.XMLparser as XMLparsing
from REhandling import regularExpressions as re

regExpr = re.regularExpressions()


def tokenizer(text, tokenized_text):
    """
    divides in tokens the text and adds some additional info such as initial and final char number, and a tag
    :param text: original text
    :param tokenized_text: list in which we must add the list of sentences containing list of tokens
    :return: the tagged text
    """
    totalLength = len(text)
    offset, length = 0, 0
    sent_text = sent_tokenize(text)  # this gives us a list of sentences
    # now loop over each sentence and tokenize it separately
    for sentence in sent_text:
        words = word_tokenize(sentence)
        # tagged = pos_tag(words)
        tokenized_sentence = []
        # print sentence
        correction = False
        for word in words:

            if correction == True:
                offset = offset - 1
                correction = False

            if word == u"``" or word == u"''":  # aperte e chiuse virgolette
                # print word
                usedWord = "\""
                correction = True
            else:
                usedWord = word

            while text[offset] != usedWord[0]:
                # print "offset char: " + text[offset] + " word char: " + usedWord
                offset = offset + 1
                length = length + 1

            length = offset + len(usedWord)

            if length - offset - len(usedWord) != 0:
                print "ERROR: something went wrong...!"
                print length, offset, len(usedWord)
                exit(0)
            # print usedWord, offset, length, len(usedWord)
            tag, tagNumber = tagText(usedWord)
            tokenized_sentence.append((usedWord, offset, length, tag, tagNumber))

            offset = offset + len(word)

        # print tokenized_sentence
        tokenized_text.append(tokenized_sentence)

    if length != totalLength:
        print "ERROR: the total lenght does not match the index of the last token!"
        exit(0)
    return tokenized_text


def tokenize(input_file_path, tokenized_text):
    """
    given an input file name it returns the tokenized text contained inside
    :param input_file_path: input file name
    :param tokenized_text: list in which we must add the list of sentences containing list of tokens
    :return: the tagged text
    """
    text = XMLparsing.reader(input_file_path)
    return tokenizer(text, tokenized_text), text


def tagText(word):
    """
    return the tag to be assigned to a single word
    :param word: word to be tagged
    :return: its tag
    """
    return re.regularExpressions.checkRE(regExpr, word)


# test line
"""
text = []
tokenizer(XMLparsing.reader("data/train/input/train_22.input.tml"), text)
for sentence in text:
    print sentence
    for word in sentence:
        print word[0], word[3]
"""