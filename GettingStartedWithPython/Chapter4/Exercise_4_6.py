def computepay(h, r):
    if h <= 40:
        pay = h * r
    else:
        pay = (h - 40) * (r * 1.5)
        pay = pay + (40 * r)
    return pay

hrs = input("Enter Hours:")
rate = input("Enter rate:")

try:
    fhrs = float(hrs)
    frate = float(rate)
except:
    print("No number entered")
    exit()

p = computepay(fhrs, frate)
print("Pay", p)