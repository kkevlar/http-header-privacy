import csv
import functools
import sys
import re
import numpy


# Read in CSV of raw data
datafile = open("diff-priv-set.csv", 'r')
datareader = csv.reader(datafile, delimiter=',')
data = []
for row in datareader:
    data.append(row)    

# Strips Column Labels
data = data[1:]

# Strips last few columns- row[5] will now contain percentage 
#    of bot hits that were for a kitten
newdata = []
for row in data:
    newrow = row[0:5]
    newrow.append(int(row[5]) / int(row[7]))
    newdata.append(newrow)

# Sets comparison to a function to decide on if the user has the expected amount of puppy or kitten love
comparison = None 
if sys.argv[1] == "kitten":
    comparison = lambda val: val >= float(sys.argv[2])
elif sys.argv[1] == "puppy":
    comparison = lambda val: (1-val) >= float(sys.argv[2])
else:
    print("First arg must be kitten or puppy")
    sys.exit(1)

# Filters the rows based on this comparison
temp = []
for row in newdata:
    if comparison(float(row[5])):
        temp.append(row)
newdata = temp

# Filters the rows based on quasi identifiers matching
for i in range(5):
    temp = []
    for row in newdata:
        if sys.argv[3+i] == 'any' or sys.argv[3+i].lower() == row[i].lower():
            temp.append(row)
    newdata = temp

num = len(newdata)
# Adds differential privacy noise
num += numpy.random.normal(scale=1.0)
if(num < 0):
    num = 0
if(num > 325):
    num=325
print("We got %d users" % num)


