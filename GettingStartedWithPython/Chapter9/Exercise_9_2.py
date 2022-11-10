name = input("Enter file:")
if len(name) < 1:
    name = "mbox-short.txt"
handle = open(name)

count = 0
sendingdays = dict()

for rows in handle:
    if not rows.startswith("From"):
        continue
    #print(rows)
    rows.rstrip()
    srows = rows.split()
    if len(srows)<3:
        continue
    #print(srows)
    day = srows[2]

    if day not in sendingdays:
        sendingdays[day] = 1
    else:
        sendingdays[day] = sendingdays[day]+1

print(sendingdays)