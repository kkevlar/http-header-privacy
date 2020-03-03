import csv
import functools
import sys
import re


datafile = open("diff-priv-set.csv", 'r')
datareader = csv.reader(datafile, delimiter=',')
data = []
for row in datareader:
    data.append(row)    

data = data[1:]

newdata = []
for row in data:
    newrow = row[0:5]
    newrow.append(int(row[5]) / int(row[7]))
    newdata.append(newrow)

comparison = None 
if sys.argv[1] == "kitten":
    comparison = lambda val: val >= float(sys.argv[2])
elif sys.argv[1] == "puppy":
    comparison = lambda val: (1-val) >= float(sys.argv[2])
else:
    print("First arg must be kitten or puppy")
    sys.exit(1)

temp = []
for row in newdata:
    if comparison(float(row[5])):
        temp.append(row)
newdata = temp

for i in range(5):
    print(i)
    temp = []
    for row in newdata:
        if sys.argv[3+i] == '*' or sys.argv[3+i] == row[i]:
            temp.append(row)
    newdata = temp

print("We got %d users" % len(newdata))


