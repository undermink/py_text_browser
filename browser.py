#!/usr/bin/env python

from bs4 import BeautifulSoup
from os import popen
import urllib
import re

body = ""
count= 0
linklist = {}
rows, columns = popen('stty size', 'r').read().split()
columns = int(columns)/2
print "\nWillkommen...\n"

InputUrl = raw_input('\nBitte eine URL eingeben: ')

url = InputUrl.strip("http://")

Response = urllib.urlopen("http://"+url)
bs = BeautifulSoup(Response.read(), "lxml")

if Response.code != 200 :

	print "Fehler :",Response.code

else :

	print bs.title.text
	html = bs.body.text.strip()
	html1 = re.sub("(.{1,%i})(\s+|\Z)" %columns, "\\1\n", html)

	for line in html1.split("\n") :

		if line.strip() :

			body += line + "\n"

	print body
	
	print "\nLinks:\n"
	for link in bs.find_all('a') :

		if link.get('href') != None :
			count += 1
			print [count], str(link.text.strip()), '=>', link.get('href')
			linklist[link.get("href")] = count


