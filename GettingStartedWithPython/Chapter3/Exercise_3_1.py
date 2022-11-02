hrs = input("Enter Hours:")
rate = input("Enter rate:")

h = float(hrs)
r = float(rate)

workhours = 40

if h > 40:
    pay = (h-workhours) * (r * 1.5)
    pay = pay + (workhours * r)
else:
    pay = h * r

print(pay)