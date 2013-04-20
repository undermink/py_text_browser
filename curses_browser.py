#!/usr/bin/env python

import curses
from bs4 import BeautifulSoup
from os import popen
import urllib
import re
import locale

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

body = ""
count = 0
linklist = {}
rows, columns = popen('stty size', 'r').read().split()
columns = int(columns) / 2
rows = int(rows) / 2
tworows = rows * 2
twocolumns = columns + columns
scr = curses.initscr()

scr.border(0)
scr.addstr(2,columns-23, 10 * "#" + " undermink's Textbrowser " + 10 * "#")
scr.addstr(4,1,"Bitte eine URL eingeben: ")
curses.echo()
curses.nocbreak()
scr.refresh()

InputUrl = scr.getstr()
url = InputUrl.strip("http://")

Response = urllib.urlopen("http://"+url)                                   
bs = BeautifulSoup(Response.read(), "lxml")

if Response.code != 200 :
	
	fehler = "Fehler: %i" % Response.code
	scr.addstr(rows,columns-5,fehler)

else:
	
	pad = curses.newpad(tworows,twocolumns)
	scr.addstr(6,1,bs.title.text)
	text = bs.body.text.strip()
	text1 = re.sub("(.{1,%i})(\s+|\Z)" %columns, "\\1\n", text)

	for line in text1.split("\n") :

		if line.strip() :

			body += line + "\n"

	#scr.addstr(8,1,body)
	utfbody = body.encode('utf-8')
	try: pad.addstr(utfbody)
	except curses.error: pass
	pad.refresh(0,0,8,1,rows+rows/2,columns+columns/2)

scr.getch()
curses.endwin()
print InputUrl
