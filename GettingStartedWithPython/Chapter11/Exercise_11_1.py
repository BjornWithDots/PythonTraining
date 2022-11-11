import re

name = input("Enter file:")
if len(name) < 1:
    name = "regex_sum_42.txt"
handle = open(name)

numbers = list()
total = 0

for rows in handle:
    num = re.findall('[0-9]+', rows)
    if not num:
        continue
    else:
        numbers = numbers + num

for nums in numbers:
    number = int(nums)
    total = total + number

print(total)
