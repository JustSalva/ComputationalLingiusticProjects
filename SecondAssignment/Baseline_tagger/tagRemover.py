from Utilities.utility import splitWordAndToken
"""
    This script removes the tags from a data-set and saves into file the obtained new data-set
"""
with open('./../dataSets/final/test', 'r') as dataSet:
    with open('./../dataSets/final/test_untagged', 'w') as  untaggedDataSet:
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
