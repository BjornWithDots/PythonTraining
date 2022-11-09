name = input("Enter file:")
if len(name) < 1:
    name = "mbox-short.txt"
handle = open(name)

count = 0
senders = dict()

for rows in handle:
    if not rows.startswith("From:"):
        continue
    #print(rows)
    rows.rstrip()
    srows = rows.split()

    sender = srows[1]

    if sender not in senders:
        senders[sender] = 1
    else:
        senders[sender] = senders[sender]+1

print(senders)