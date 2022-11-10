name = input("Enter file:")
if len(name) < 1:
    name = "mbox-short.txt"
handle = open(name)

count = 0
mailers = dict()

for rows in handle:
    if not rows.startswith("From:"):
        continue
    rows.rstrip()
    srows = rows.split()
    fname = srows[1]

    if fname not in mailers:
        mailers[fname] = 1
    else:
        mailers[fname] = mailers[fname] + 1

    count = count+1

maxmails = (max(mailers.values()))

for key in mailers:
    if mailers[key] == maxmails :
        print(key, mailers[key])
