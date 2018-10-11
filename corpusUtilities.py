from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
import XMLparsing.XMLparser as XMLparsing
import regularExpressions as re

regExpr = re.regularExpressions()

def tokenizer(text, tokenized_text):
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
    tokenizer(XMLparsing.reader(input_file_path), tokenized_text)


def tagText(word):
    return re.regularExpressions.checkRE(regExpr, word)


# test line
text = []
tokenizer(XMLparsing.reader("data/train/input/train_22.input.tml"), text)
for sentence in text:
    print sentence
    for word in sentence:
        print word[0], word[3]

