import urllib.request
import urllib.parse
import os
import json

def get_html(url):
	req = urllib.request.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36')
	response = urllib.request.urlopen(req)
	html = response.read()
	return html

def get_page(url):
	html = get_html(url).decode('utf-8')
	url_num = []
	a = html.find('A HREF="')
	while a != -1:
		b = html.find('.html"',a,a+255)
		if b != -1:
			url_num.append(html[a+8:b+5])
		else:
			b = a+9
		a = html.find('A HREF="',b)

	return url_num

def get_img_page(url):
	html = get_html(url).decode('utf-8')
	img_page_num = []
	a = html.find('A HREF="')
	while a != -1:
		b = html.find('/A',a,a+255)
		if b != -1:
			img_page_num.append(html[a+8:b])
		else:
			b = a+9
		a = html.find('A HREF="',b)

	return img_page_num

def get_img(html):
	img_addrs=[]
	a = html.find('IMG SRC="')
	while a != -1:
		b = html.find('.gif',a,a+255)
		if b != -1:
			img_addrs.append(html[a+9:b+4])
		else:
			b = a+9

		a = html.find('IMG SRC="',b)
	return img_addrs

def save_img(url,img_addrs,dict_js):
	for each in img_addrs:
		filename = each
		html = get_html(url+'/'+each)
		dict_js[filename] = html

def get_data(html):
	a = html.find('PRE>')
	a = a+4
	b = html.find('</TD',a)
	dic={}
	ans = html[a+16:b] 
	mid = ans.find('filename') 
	mix = ans.find(' ',mid)
	dic[ans[mid:mix]] = ans[mix:ans.find('\n',mix)]
	fina = ans.find('\n',mix)
	mid = ans.find('DATE',fina)
	mix = ans.find(' ',mid)
	dic[ans[mid:mix]] = ans[mix:ans.find('\n',mix)]
	fina = ans.find('\n',mix)
	mid = ans.find('PATIENT',fina)
	mix = ans.find(' ',mid)
	dic[ans[mid:mix]] = ans[mix:ans.find('\n',mix)]
	fina = ans.find('\n',mix)
	mid = ans.find('FILM_TYPE',fina)
	mix = ans.find(' ',mid)
	dic[ans[mid:mix]] = ans[mix:ans.find('\n',mix)]
	fina = ans.find('\n',mix)
	mid = ans.find('DATE_DIGITIZED',fina)
	mix = ans.find(' ',mid)
	dic[ans[mid:mix]] = ans[mix:ans.find('\n',mix)]
	fina = ans.find('\n',mix)
	return dic
folder = 'breastcancer_database'

os.chdir(folder)
urlhome = 'http://marathon.csee.usf.edu/Mammography/DDSM/thumbnails/normals/normal_02/overview.html'
a = urlhome.find('/overview')
urlmid = urlhome[0:a]
url_num = get_page(urlhome)
img_pag_add = get_img_page(urlhome)
i = 0
for each in url_num:
	try:
		dict_js = {}
		url = urlmid+'/'+each
		html = get_html(url).decode('utf-8')
		dict_js = get_data(html)
		img_addrs = get_img(html)
		url = urlmid+'/'+img_pag_add[i]
		save_img(url,img_addrs,dict_js)
		print(dict_js)
		js = json.dumps(dict_js)
		with open(dict_js['filename']+'.json','wb') as f:
			f.write(dict_js)
		i += 1
	except:
		continue