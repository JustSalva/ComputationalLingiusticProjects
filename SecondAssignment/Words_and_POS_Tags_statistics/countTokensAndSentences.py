import sys

"""
    This small script simply counts the number of tokens and lines of a file printed on the standard output
"""
numberOfLines = 0
numberOfTokens = 0
for line in sys.stdin:
    numberOfLines += 1
    for word in line.split():
        numberOfTokens += 1

print("numberOfLines: " + str(numberOfLines))
print("numberOfTokens: " + str(numberOfTokens))
