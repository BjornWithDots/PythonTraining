# Used link http://py4e-data.dr-chuck.net/known_by_Fikret.html
# Link for actual http://py4e-data.dr-chuck.net/known_by_Konstancja.html

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter URL: ')
count = int(input('Enter count: '))
pos = int(input('Enter position: '))

def getnext(url):
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')
    x = 1
    for tag in tags:
        # Skip until input - pos number of links
        if x != pos:
            # print("Don't want:",(tag.get('href', None)))
            x = x + 1
            continue
        row = (tag.get('href', None))

        return row
        break

# Loop for input - count number of times
for links in range(count):
    print("Retrieving:",url)
    url = getnext(url)

print('Final:', url)

