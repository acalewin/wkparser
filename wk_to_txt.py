# -*- coding: utf-8 -*-
import json
import requests
import sys
import codecs

url = "https://www.wanikani.com/api/user/%s/%s/" % (sys.argv[1], 'vocabulary')
resp = requests.get(url=url)
data = json.loads(resp.content)

#print data
#f = open('known_kanji.txt', 'w')
data = data[u'requested_information'][u'general']
for k in data:
#   print k
   if (k[u'user_specific']):
        if (k[u'user_specific'][u'srs'] in [u'enlighten', u'burned']):
           print k[u'character'].encode('utf-8')
#f.close
