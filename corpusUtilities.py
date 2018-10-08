from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
import XMLparsing.XMLparser as XMLparsing


def tokenizer(text):
    totalLength = len(text)
    offset, length = 0, 0
    sent_text = sent_tokenize(text)  # this gives us a list of sentences
    tokenized_text = []
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
            tokenized_sentence.append((usedWord, offset, length))

            offset = offset + len(word)

        # print tokenized_sentence
        tokenized_text.append(tokenized_sentence)

    print tokenized_text
    if length != totalLength:
        print "ERROR: the total lenght does not match the index of the last token!"
        exit(0)


# test line
tokenizer(XMLparsing.reader("data/train/input/train_07.input.tml"))
