import re
import urllib.request
import os
import json
from bs4 import BeautifulSoup

cases_urls=[]
notes_urls=[]

def get_html(url):
	req = urllib.request.Request(url)
	response = urllib.request.urlopen(req)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36')
	return response.read()

def get_soup(html,par):
	return BeautifulSoup(html,par)

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


def save_img(folder,img_addrs,mid_url):
	for each in img_addrs:
		filename = each
		with open(filename,'wb') as f:
			f.write(get_html(mid_url+each))

html = get_html('http://marathon.csee.usf.edu/Mammography/Database.html')
soup = get_soup(html,'html.parser').prettify()
folder = 'breastcancer_img'
'''
os.mkdir(folder)
'''
os.chdir(folder)

for i in re.finditer(r'<a href=".*">\n.*(thumbnails).*\n.*',soup):
	cases_urls.append(i.group())
'''
for each in cases_urls:
	st = each.find('="')
	en = each.find('">')
	cases_url = each[st+2:en]
	mid_url = cases_url[0:cases_url.find('/overview.html')]+'/'
	cases_html = get_html(cases_url)
	cases_soup = get_soup(cases_html,'html.parser').prettify()
	for i in re.finditer(r'<a href=".*">\n.*(case).*\n.*',cases_soup):
		try:
			st = i.group().find('="')
			en = i.group().find('">')
			mid2_url = mid_url+i.group()[st+2:en]
			imgaddrs = get_img(get_html(mid2_url).decode('utf-8'))
			mid3_url = mid2_url[0:mid2_url.find('/case')+10]
			save_img(folder,imgaddrs,mid3_url)
		except:
			print(mid_url+i.group()[st+2:en])
'''
for i in re.finditer(r'<a href=".*">\n.*(notes).*\n.*',soup):
	notes_urls.append(i.group())
for each in notes_urls:
	st = each.find('="')
	en = each.find('">')
	note_url = each[st+2:en]
	note_html = get_html(note_url)
	note_soup = get_soup(note_html,'html.parser').prettify()
	st = 0
	ed = 0
	mid_str = note_html.decode('utf-8')
	while st != -1:
		st = mid_str.find('<B>',ed)
		ed = mid_str.find('</B>',st)
		if mid_str[st+3:st+4] != 'u':
			mix = mid_str.find('</TD>',ed)
		else:
			mix = ed
		if st != -1:
			print(mid_str[st+3:ed]+mid_str[ed+3:mix])