text = "X-DSPAM-Confidence:    0.8475"
startpos = text.find(':')

num = text[startpos+1:]
num = num.strip()

fnum = float(num)

print(num)
