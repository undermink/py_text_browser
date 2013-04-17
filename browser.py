#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib

body = ""
count= 0
linklist = {}

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

	for line in html.split("\n") :

		if line.strip() :

			body += line + "\n"

	print body
	
	print "\nLinks:\n"
	for link in bs.find_all('a') :

		if link.get('href') != None :
			count += 1
			print link.get('href') , [count]
			linklist[link.get("href")] = count


