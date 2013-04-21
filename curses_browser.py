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

curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
scr.border(0)
header = curses.newwin(1, (columns-1)*2, 1, 1)
header.addstr(0,columns-23, 10 * "#" + " undermink's Textbrowser " + 10 * "#")
header.bkgd(curses.color_pair(2))
scr.addstr(4,3,"Bitte eine URL eingeben: ")
curses.echo()
curses.nocbreak()
scr.refresh()
header.refresh()
InputUrl = scr.getstr()
url = InputUrl.strip("http://")
pad_pos = 0
pad_posx = 0

try: Response = urllib.urlopen("http://"+url)
except all : scr.addstr(rows,columns-4,"wrong url")
bs = BeautifulSoup(Response.read(), "lxml")

if Response.code != 200 :
	
	fehler = "Fehler: %i" % Response.code
	scr.addstr(rows,columns-5,fehler)

else:
	
	pad = curses.newpad(10000,3000)
	pad.bkgd(curses.color_pair(1))
	scr.addstr(6,3,bs.title.text, curses.color_pair(1))
	try: text = bs.body.text.strip()
	except all: pass
	text1 = re.sub("(.{1,%i})(\s+|\Z)" %columns, "\\1\n", text)

	for line in text1.split("\n") :

		if line.strip() :

			body += line + "\n"

	#scr.addstr(8,1,body)
	utfbody = body.encode('utf-8')
	try: pad.addstr(utfbody)
	except curses.error: pass
	curses.cbreak()
	curses.noecho()
	pad.refresh(0,0,8,3,rows+rows/2,columns+columns/4)
	while True:
		cmd = scr.getch()
		if  cmd == ord('s') :
			if pad_pos <= 10000 :
				pad_pos += 1
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+rows/2, columns+columns/4)
		elif  cmd == ord('w') :
			if pad_pos >= 1 :
				pad_pos -= 1
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+rows/2, columns+columns/4)
		elif cmd == ord('a') :
			if pad_posx >= 1 :
				pad_posx -= 1
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+rows/2, columns+columns/4)
		elif cmd == ord('d') :
			if pad_posx <= 2999 :
				pad_posx += 1
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+rows/2, columns+columns/4)

		elif cmd == ord('x') :
			break

curses.endwin()
