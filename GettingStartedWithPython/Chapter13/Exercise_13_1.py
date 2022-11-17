import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import ssl

file = input("Link to the xml file: ")

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
tree = ET.fromstring(data)

lst = tree.findall('comments/comment')
print('Number of values:', len(lst))
total = 0

for item in lst:
    value = item.find('count').text
    value = int(value)
    total = total + value

print(total)

 #   results = tree.findall('result')
 #   lat = results[0].find('geometry').find('location').find('lat').text
 #   lng = results[0].find('geometry').find('location').find('lng').text
 #   location = results[0].find('formatted_address').text

 #   print('lat', lat, 'lng', lng)
 #   print(location)
