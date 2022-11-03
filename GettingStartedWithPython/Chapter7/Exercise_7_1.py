# Use words.txt as the file name
fname = input("Enter file name: ")
fh = open(fname)
content = fh.read()
content = content.rstrip()
print(content.upper())
