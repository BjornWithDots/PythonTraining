name = input("Enter file:")
if len(name) < 1:
    name = "mbox-short.txt"
handle = open(name)

hours = dict()

for rows in handle:
    if not rows.startswith("From"):
        continue
    rows.rstrip()
    srows = rows.split()
    if len(srows)<5:
        continue
    fname = srows[5]
    splitted = fname.split(':')
    hour = splitted[0]

    if hour not in hours:
        hours[hour] = 1
    else:
        hours[hour] = hours[hour] + 1

l = list()

for key, val in list(hours.items()):
    l.append( (key,val) )

l.sort()

for key, val in l:
    print(key,val)
