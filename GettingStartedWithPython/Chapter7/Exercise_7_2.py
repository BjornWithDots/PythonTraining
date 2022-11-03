# Use the file name mbox-short.txt as the file name
fname = input("Enter file name: ")
fh = open(fname)
noofrows = 0
totalvalues = 0
for line in fh:
    if not line.startswith("X-DSPAM-Confidence:"):
        continue
    startpos = line.find(':')
    value = line[startpos+1:]
    fvalue = float(value)
    totalvalues = totalvalues + fvalue
    noofrows = noofrows + 1

avgvalue = totalvalues / noofrows
print("Average spam confidence:", avgvalue)