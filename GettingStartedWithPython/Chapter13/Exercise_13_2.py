import urllib.request, urllib.parse, urllib.error
import json
import ssl

file = input("Enter location: ")

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

parms = dict()
url = file
print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)

data = uh.read()
print('Retrieved', len(data), 'characters')


info = json.loads(data)
print('Count:', len(info['comments']))

total = 0

for i in info['comments']:
    value = (i['count'])
    total = total + value

print("Sum:", total)

#for item in info:
#    print('Name', item['comment'])
#    print('Id', item['id'])
#    print('Attribute', item['x'])