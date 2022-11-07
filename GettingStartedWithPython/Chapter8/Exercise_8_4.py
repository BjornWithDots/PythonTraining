fname = input("Enter file name: ")
fh = open(fname)
lst = list([])
for line in fh:
    line = line.rstrip()
    sline = line.split()

    for word in sline:
        if lst is None:
            lst.append(word)
            continue
        if word in lst:
            continue
        lst.append(word)

lst.sort()
print(lst)