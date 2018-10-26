import sys

lexicon = {}
for line in sys.stdin:
    for word in line.split():
        if word not in lexicon:
            lexicon[word] = 1
    for word in sorted(lexicon.keys()):
        print(word)
