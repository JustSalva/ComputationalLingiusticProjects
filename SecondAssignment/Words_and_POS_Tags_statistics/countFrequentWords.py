from operator import itemgetter

frequencyList = []
with open('./../dataSets/train_frequencies', 'r') as dataset:
    for line in dataset:
        word, frequency = line.split(' ', 1)
        frequencyList.append((word, int(frequency)))

frequencyList = sorted(frequencyList, key=itemgetter(1), reverse=True)
print(frequencyList)
with open('./../dataSets/mostFrequentWords', 'w') as frequentWords:
    for i in range(0, 10):
        word, frequency = frequencyList[i]
        print(word + " " + str(frequency), file=frequentWords)
