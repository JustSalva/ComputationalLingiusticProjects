from Utilities.utility import *
dictionary = dict()
wordFrequencies = dict()


def addToDictionary(token):
    try:
        word, tag = splitWordAndToken(token)
        if tag in dictionary:
            if word in wordFrequencies:
                wordFrequencies[word] += 1

                if wordFrequencies[word] == 4:
                    temp_list = dictionary[tag]
                    temp_list.append(word)
                    dictionary[tag] = temp_list
            else:
                wordFrequencies[word] = 1
        else:
            temp_list = []
            dictionary[tag] = temp_list
            if word in wordFrequencies:
                wordFrequencies[word] += 1
                if wordFrequencies[word] == 4:
                    temp_list = dictionary[tag]
                    temp_list.append(word)
                    dictionary[tag] = temp_list
            else:
                wordFrequencies[word] = 1
    except Exception as e:
        print(e.with_traceback())
        print('error!!!: ' + token)
        exit(-1)


def replaceWordIfNotFrequent(token):
    word, tag = splitWordAndToken(token)

    if (word in wordFrequencies) and (wordFrequencies[word]) >= 4:
        return token

    return '<UNK>' + '/' + tag


# build frequency and restricted lexicon tables
with open('./../dataSets/dumas_train_replaced', 'r') as dataset:
    with open('./../dataSets/train_dictionary', 'w') as tagDictionary:

        for line in dataset:
            # add every word to the dictionary (added only if its support reaches value 4)
            for token in line.split():
                addToDictionary(token)
            toPrint = ''

        for key in dictionary:
            toPrint = ''
            for word in dictionary[key]:
                toPrint = toPrint + word + ' '

            toPrint = key + ':' + toPrint
            # print(toPrint)
            print(toPrint, file=tagDictionary)

with open('./../dataSets/train_frequencies', 'w') as frequencies:
    lexiconSize = 0
    for word in wordFrequencies:
        print(word + ' ' + str(wordFrequencies[word]), file=frequencies)
        if wordFrequencies[word] >= 4:
            lexiconSize += 1

print('restricted lexicon size = ' + str(lexiconSize))

# create new train and test files
for fileScope in ['train', 'test']:
    with open('./../dataSets/dumas_' + fileScope + '_replaced', 'r') as dataset:
        with open('./../dataSets/final/' + fileScope, 'w') as finalDataset:
            for line in dataset:
                list = []
                for token in line.split():
                    list.append(replaceWordIfNotFrequent(token))
                toPrint = ''
                for i in range(0, len(list) - 1):
                    toPrint = toPrint + list[i] + ' '
                toPrint = toPrint + list[len(list) - 1]
                print(toPrint, file=finalDataset)
