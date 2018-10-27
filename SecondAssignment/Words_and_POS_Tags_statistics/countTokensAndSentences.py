import sys

numberOfLines = 0
numberOfTokens = 0
for line in sys.stdin:
    numberOfLines +=1
    for word in line.split():
       numberOfTokens +=1;

print("numberOfLines: " + str(numberOfLines))
print("numberOfTokens: " + str(numberOfTokens))
