import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter URL: ')
count = input('Enter count: ')
pos = int(input('Enter position: '))
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

# Retrieve all of the anchor tags
tags = soup('a')
x = 1

for tag in tags:
    if x != pos:
       # print("Don't want:",(tag.get('href', None)))
        x = x + 1
        continue
    row = (tag.get('href', None))
    #print("Want:",row)
    break

#print(row)



#row = row.split('_')
#print(row)