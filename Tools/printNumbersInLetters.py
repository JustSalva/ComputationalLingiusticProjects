from num2words import num2words
list = []
for i in range(1, 1000):
    # print(num2words(i, ordinal=True)+'|'),
    list.append(num2words(i, ordinal=True))
for i in reversed(list):
    print i
