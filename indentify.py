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

def output_preferences_by_bot():
    pref = []
    options = [
            "GET /img/kitten1 HTTP/1.1 ",
            "GET /img/kitten2 HTTP/1.1 ",
            "GET /img/kitten3 HTTP/1.1 ",
            "GET /img/puppy1 HTTP/1.1 ",
            "GET /img/puppy2 HTTP/1.1 ",
            "GET /img/puppy3 HTTP/1.1 ",
            ]
    for user in uniq_users:
        scores = [0,0,0, 0,0,0, 0,0,0,0]
        for row in user:
            match = False
            for i in range(len(options)):
                if options[i] == row[7]:
                    scores[i] += 1
                    if i < 3: 
                        scores[7] += 1
                    elif i < 6:
                        scores[8] += 1
                    match = True
            if not match:
                scores[6] += 1 
            scores[9] += 1
        baseuser = user[0]
        pref.append(scores.extend(baseuser))

    def options_index_to_char(index):
        return chr(ord('A') + index)
    print("The %dth col, (in sheets it will be column %c), begins the preference information" % (0, options_index_to_char(0)))
    y = 0
    while y < len(options):
        print("Column %c: %s" % (options_index_to_char(y), options[y]))
        y = y+1
    print("Column %c: %s" % (options_index_to_char(6), "Other Click"))
    print("Column %c: %s" % (options_index_to_char(7), "Kitten Total"))
    print("Column %c: %s" % (options_index_to_char(8), "Puppy Total"))
    print("Column %c: %s" % (options_index_to_char(9), "Total Hits"))
    out_csv(pref, "user-preferences")


output_prelim_unique_user_info()




