import csv
import functools
import sys

same_user_indecies = [1,2,3,5,11]

datafile = open(sys.argv[1], 'r')
datareader = csv.reader(datafile, delimiter='~')
data = []
for row in datareader:
    data.append(row)    

data = list(filter(lambda row: len(row) >= 15, data))
print("Found %d rows\n" % len(data))

def cols_match(indecies,a, b):
    return all(map(lambda index: a[index] == b[index], indecies))

def same_user(a,b):
    return cols_match(same_user_indecies, a, b)

def group_users(comp, raw_rows):
    groups = []
    for row in raw_rows:
        found = False
        for group in groups:
            if comp(row, group[0]):
                group.append(row)
                found = True
                break
        if not found:
            groups.append([row])
    return groups

uniq_users = group_users(same_user, data)

print("Discovered %d unique users!" % len(uniq_users))

userinfo = []
for user in uniq_users:
    userinfo.append(user[0])
with open("preliminary-user-info.csv", "w", newline="") as f:
    writer = csv.writer(f, delimiter="~") 
    writer.writerows(userinfo)

#pref = []
#for user in uniq_users:
#    pref.append(group_users(lambda a,b: cols_match([7],a,b), user))
#print(pref[2][1])



