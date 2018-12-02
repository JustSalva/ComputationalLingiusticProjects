vocabulary = dict()
def initializeVocabulary():
    """
    Loads the word's dictionary from file
    """
    with open('./../data/projectFiles/vocabulary', 'r') as vocabularyDataset:
        for word in vocabularyDataset:
            vocabulary[word.replace("\n", "")] = True  # just to mark an element as present

initializeVocabulary()
counter = 0
with open('./../data/test/test.input.txt', 'r') as dataset:
    for line in dataset:
        for word in line.split():
            if word not in vocabulary:
                counter += 1
print (counter)