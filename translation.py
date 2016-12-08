import urllib.request
import urllib.parse
import json
import time


url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=dict2.top"
data = {}
data['type'] = 'AUTO'
data['i'] = 'my name'
data['doctype'] = 'json'
data['xmlVersion'] = '1.8'
data['keyfrom'] = 'fanyi.web'
data['ue'] = 'UTF-8'
data['action'] = 'FY_BY_ENTER'
data['typoResult'] = 'true'
data = urllib.parse.urlencode(data).encode('UTF-8')

head = {}
head['User-Agent'] ='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'



req = urllib.request.Request(url,data,head)
response = urllib.request.urlopen(req)
html = response.read().decode('UTF-8')
json.loads(html)
target = json.loads(html)

print(target['translateResult'][0][0]['tgt'])
print(req.headers)