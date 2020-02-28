import csv
import functools
import sys
import re

same_user_indecies = [1,2,3,5,11]

datafile = open(sys.argv[1], 'r')
datareader = csv.reader(datafile, delimiter='~')
data = []
for row in datareader:
    data.append(row)    

ua_key_file = open('user-agent-key.csv', 'r')
ua_key_reader = csv.reader(ua_key_file, delimiter=',')
ua_keys = []
for row in ua_key_reader:
    ua_keys.append(row)

temp = []
for row in data:
    if len(row) >= 15:
        temp.append(row)
    else:
        print("Throwing out a short row!")
data = temp
print("Found %d rows\n" % len(data))

print("About to add more info by decoding user agent strings.....")
temp = []
for row in data:
    extra = None
    for key in ua_keys:
        if row[11] == key[0]:
            extra = list(map(lambda s:s.strip(),key[1:]))
    if extra is None and row[1] != '-':
        print("Error! A non-human row has an unmatched user agent! %s" % (row[0:5]))
    elif not extra is None:
        row.extend(extra)
        temp.append(row)
    else:
        row.extend(['?' for i in range(len(ua_keys[0]))]) 
        temp.append(row)
data = temp

print("About to add more info by splitting IPS.....")
temp = []
for row in data:
    if row[1] != '-':
        extra = list(re.match("for= \\\\x22(.+)\\.(.+)\\.(.+)\\.(.+)\\\\x22",row[1]).groups() )
        extra.append(int(extra[0]) // 100)
        extra.append(int(extra[0]) // 10)
        row.extend(extra)
        temp.append(row)
    else:
        row.extend(['?' for i in range(6)]) 
        temp.append(row)
data = temp

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

    
def print_col_indecies_with_examples(data):
    for col in range(len(data[0])):
        print("%5d: " % col, end='')
        for row in range(0,1500,123):
            print(data[row][col], end='')
        print("\n")
        
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

def output_cookie_acceptance_by_group(groups, csvname):
    cookie = []
    for group in groups:
        acceptances = list(map(lambda row: 1 if len(row[16]) > 5 else 0, group))
        cookie.append([sum(acceptances) / len(acceptances)])
    for i in range(len(groups[0][0])):
        if all(map(lambda group: all(map(lambda row: row[i] == group[0][i] , group)), groups)):
            for j in range(len(cookie)):
                cookie[j].append(groups[j][0][i])
    out_csv(cookie, csvname)

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
    for i in range(len(groups[0][0])):
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

def bread(data_rows_only, cols, name):
    raw_uniq = group_users(lambda a,b: cols_match(cols,a,b), data_rows_only)
    uniq = list(filter(lambda u: not u[0][1] == '-', raw_uniq))
    print("\nThe bots use %d unique %s!" % (len(uniq), name))
    uniq_users_in = list(map(lambda lang: group_users(same_user, lang), uniq))
    counts = list(map(lambda u: len(u), uniq_users_in))
    print("\t%03d bots - %03d bots" % (min(counts), max(counts)))
    output_preferences_by_group(uniq, "pref-by-%s" % name)

raw_uniq_users = group_users(same_user, data)
uniq_users = list(filter(lambda u: not u[0][1] == '-', raw_uniq_users))
print("Threw out %d humans!" % (len(raw_uniq_users) - len(uniq_users)))
print("Discovered %d unique bots!" % len(uniq_users))
output_preferences_by_group(uniq_users, "pref-by-unique-user")

bread(data, [1], "ipA") 
bread(data, [5], "language") 
bread(data, [11], "user-agent") 
bread(data, [21], "browser") 
bread(data, [22], "platform") 
bread(data, [23], "device") 
bread(data, [24], "gendevice") 
bread(data, [5,11], "lang-and-ua") 
bread(data, [21,22], "browser-and-platform") 
bread(data, [5,24], "lang-and-gendevice") 
bread(data, [25], "ip1") 
bread(data, [29], "ip-digit-1") 
bread(data, [5,25,29], "language-gendevice-and-ip-digit-1") 



