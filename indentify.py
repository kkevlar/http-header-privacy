import csv
import functools
import sys

same_user_indecies = [1,2,3,5,11]

datafile = open(sys.argv[1], 'r')
datareader = csv.reader(datafile, delimiter='~')
data = []
for row in datareader:
    data.append(row)    

temp = []
for row in data:
    if len(row) >= 15:
        temp.append(row)
    else:
        print("Throwing out a short row!")
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

raw_uniq_users = group_users(same_user, data)
uniq_users = list(filter(lambda u: not u[0][1] == '-', raw_uniq_users))
print("Threw out %d humans!" % (len(raw_uniq_users) - len(uniq_users)))
print("Discovered %d unique bots!" % len(uniq_users))

raw_uniq_languages = group_users(lambda a,b: cols_match([5],a,b), data)
uniq_languages = list(filter(lambda u: not u[0][1] == '-', raw_uniq_languages))
print("\nThe bots use %d unique languages!" % len(uniq_languages))

raw_uniq_user_agents = group_users(lambda a,b: cols_match([11],a,b), data)
uniq_user_agents = list(filter(lambda u: not u[0][1] == '-', raw_uniq_user_agents))
print("The bots use %d unique user agents!" % len(uniq_user_agents))

def out_csv(data2d, name):
    print("Writing to %s.csv" % name)
    with open("%s.csv" % name, "w", newline="") as f:
        writer = csv.writer(f, delimiter="~") 
        writer.writerows(data2d)

def output_prelim_unique_user_info():
    userinfo = []
    for user in uniq_users:
        userinfo.append(user[0])
    out_csv(userinfo, "base-user-info")

def output_preferences_by_group(groups, csvname):
    pref = []
    options = [
            "GET /img/kitten1 HTTP/1.1 ",
            "GET /img/kitten2 HTTP/1.1 ",
            "GET /img/kitten3 HTTP/1.1 ",
            "GET /img/puppy1 HTTP/1.1 ",
            "GET /img/puppy2 HTTP/1.1 ",
            "GET /img/puppy3 HTTP/1.1 ",
            ]
    for user in groups:
        scores = [0,0,0, 0,0,0, 0,0,0,0]
        for row in user:
            match = False
            for i in range(len(options)):
                if options[i].strip() == row[7].strip():
                    scores[i] += 1
                    if i < 3: 
                        scores[7] += 1
                    elif i < 6:
                        scores[8] += 1
                    match = True
            if not match:
                scores[6] += 1 
            scores[9] += 1
        pref.append(scores)
    for i in range(len(user[0][0])):
        if all(map(lambda group: all(map(lambda row: row[i] == group[0][i] , group)), groups)):
            for j in range(len(pref)):
                pref[j].append(groups[j][0][i])
    labelstring = options
    labelstring.append("Other (Not Puppy/Kitten)")
    labelstring.append("Kitten Total")
    labelstring.append("Puppy Total")
    labelstring.append("Total Hits")
    while len(labelstring) < len(pref[0]):
        labelstring.append("?")
    pref.insert(0, labelstring)
    out_csv(pref, csvname)

output_preferences_by_group(uniq_languages, "pref-by-language")




