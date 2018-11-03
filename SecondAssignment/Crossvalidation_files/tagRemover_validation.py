from Utilities.utility import splitWordAndToken
"""
    This script removes the tags from a data-set and saves into file the obtained new data-set
"""
with open('./../results/trains_for_crossvalid/valid_set0', 'r') as dataSet:
    with open('./../results/trains_for_crossvalid/valid_untagged_0', 'w') as  untaggedDataSet:
        for line in dataSet:
            list = []
            for token in line.split():
                word, tag = splitWordAndToken(token)
                list.append(word)
            toPrint = ""
            for i in range(0, len(list) - 1):
                toPrint = toPrint + list[i] + " "
            toPrint = toPrint + list[len(list) - 1]
            print(toPrint, file = untaggedDataSet)

with open('./../results/trains_for_crossvalid/valid_set1', 'r') as dataSet:
    with open('./../results/trains_for_crossvalid/valid_untagged_1', 'w') as  untaggedDataSet:
        for line in dataSet:
            list = []
            for token in line.split():
                word, tag = splitWordAndToken(token)
                list.append(word)
            toPrint = ""
            for i in range(0, len(list) - 1):
                toPrint = toPrint + list[i] + " "
            toPrint = toPrint + list[len(list) - 1]
            print(toPrint, file = untaggedDataSet)

with open('./../results/trains_for_crossvalid/valid_set2', 'r') as dataSet:
    with open('./../results/trains_for_crossvalid/valid_untagged_2', 'w') as  untaggedDataSet:
        for line in dataSet:
            list = []
            for token in line.split():
                word, tag = splitWordAndToken(token)
                list.append(word)
            toPrint = ""
            for i in range(0, len(list) - 1):
                toPrint = toPrint + list[i] + " "
            toPrint = toPrint + list[len(list) - 1]
            print(toPrint, file = untaggedDataSet)

with open('./../results/trains_for_crossvalid/valid_set3', 'r') as dataSet:
    with open('./../results/trains_for_crossvalid/valid_untagged_3', 'w') as  untaggedDataSet:
        for line in dataSet:
            list = []
            for token in line.split():
                word, tag = splitWordAndToken(token)
                list.append(word)
            toPrint = ""
            for i in range(0, len(list) - 1):
                toPrint = toPrint + list[i] + " "
            toPrint = toPrint + list[len(list) - 1]
            print(toPrint, file = untaggedDataSet)