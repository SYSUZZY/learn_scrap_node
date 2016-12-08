import urllib.request
import os

def get_page(url):
	req = urllib.request.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36')
	response = urllib.request.urlopen(url)
	html = response.read().decode('utf-8')

	a = html.find('current-comment-page')+23 
	b = html.find(']',a)

	return html[a:b]

def find_img(url):
	req = urllib.request.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36')
	response = urllib.request.urlopen(url)
	html = response.read().decode('utf-8')

	img_addrs = []

	a = html.find('img src=')

	while a != -1:
		b = html.find('.jpg',a,a+255)
		if b != -1:
			img_addrs.append(html[a+9:b+4])
		else:
			b = a+9

		a = html.find('img src=',b)
	return img_addrs
def save_img(folder,img_addrs):
	for each in img_addrs:
		filename = each.split('/')[-1]
		with open(filename,'wb') as f:
			req = urllib.request.Request(each)
			req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36')
			response = urllib.request.urlopen(each) 
			img = response.read()
			f.write(img)
folder = 'OOXX'
page = 200
'''
os.mkdir(folder)
'''
os.chdir(folder)

url = 'http://jandan.net/ooxx'
page_num = int(get_page(url))

for i in range (page):
	try:
		page_num -= i
		page_url = url + '/page-'+str(page_num)+'#comments'
		img_addrs = find_img(page_url)
		save_img(folder,img_addrs)
	except:
		continue