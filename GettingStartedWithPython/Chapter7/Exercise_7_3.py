fname = input("Enter file name: ")

if fname == "na na boo boo":
    print("NA NA BOO BOO TO YOU - You have been punk'd!")
    exit()

else:
    try:
        fh = open(fname)
    except:
        print("File cannot be opened", fname)
        exit()


noofrows = 0
for line in fh:
    if not line.startswith("Subject"):
        continue
    noofrows = noofrows + 1

print("There was", noofrows, "subject lines in file", fname)