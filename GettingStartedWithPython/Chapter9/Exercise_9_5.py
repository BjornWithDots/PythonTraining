name = input("Enter file:")
if len(name) < 1:
    name = "mbox-short.txt"
handle = open(name)

count = 0
domains = dict()

for rows in handle:
    if not rows.startswith("From:"):
        continue
    rows.rstrip()
    srows = rows.split()
    fname = srows[1]
    mailsplit = fname.split('@')
    domain = mailsplit[1]
    #print(domain)

    if domain not in domains:
        domains[domain] = 1
    else:
        domains[domain] = domains[domain] + 1

print(domains)

