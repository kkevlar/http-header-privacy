from cons import cons, cdr, car
import csv
import functools

datafile = open('start-data.txt', 'r')
datareader = csv.reader(datafile, delimiter='~')
data = []

for row in datareader:
    data.append(row)    

def same_user(a, b):
    comps_indecies = [1, 5, 11]
    return all(map(lambda index: a[index] == b[index], comps_indecies))

def group_users(raw_rows):
    groups = []
    for row in raw_rows:
        found = False
        for group in groups:
            if same_user(row, group[0]):
                group.append(row)
                found = True
                break
        if not found:
            groups.append([row])
    return groups


print(functools.reduce(lambda a,b : a if len(a) > len(b) else b,group_users(data)))


