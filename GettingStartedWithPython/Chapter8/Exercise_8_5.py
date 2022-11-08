fname = input("Enter file name: ")
if len(fname) < 1:
    fname = "mbox-short.txt"

fh = open(fname)
count = 0

for rows in fh:
    if not rows.startswith("From:"):
        continue
    rows.rstrip()
    srows = rows.split()
    print(srows[1])
    count = count+1

print("There were", count, "lines in the file with From as the first word")
