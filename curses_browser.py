#!/usr/bin/env python

import curses
from bs4 import BeautifulSoup
from os import popen
import urllib
import re
import locale
from commands import *

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

body = ""
count = 0
linklist = ''
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
scr.keypad(1)
curses.nocbreak()
scr.refresh()
header.refresh()
InputUrl = scr.getstr()
url = InputUrl.strip("http://")
pad_pos = 0
pad_posx = 0
lpad_pos = 0

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
	pad.refresh(0,0,8,3,rows+rows/2,(columns+columns/4)-3)
	lpad = curses.newpad(5000,(columns+columns)/3)
	lpad.bkgd(curses.color_pair(2))
	for link in bs.find_all('a') :
		if link.get('href') != None :
			count += 1
			linklist += "[" + str(count) + "] " + link.text.strip() + " => " + link.get('href') + "\n"
			#linklist = re.sub("\xbb","",linklist)
	try: 
		utflinks = linklist.encode('utf-8')
		lpad.addstr(utflinks)
	except curses.error: pass
	lpad.refresh(0,0,8,columns+columns/4,rows+rows/2,columns+columns-4)

	while True:
		cmd = scr.getch()
		if  cmd == curses.KEY_DOWN :
			if pad_pos <= 10000 :
				pad_pos += 1
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+rows/2, (columns+columns/4)-3)
		elif  cmd == curses.KEY_UP :
			if pad_pos >= 1 :
				pad_pos -= 1
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+rows/2, (columns+columns/4)-3)
		elif cmd == curses.KEY_LEFT :
			if pad_posx >= 1 :
				pad_posx -= 1
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+rows/2, (columns+columns/4)-3)
		elif cmd == curses.KEY_RIGHT :
			if pad_posx <= 2999 :
				pad_posx += 1
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+rows/2, (columns+columns/4)-3)
		elif cmd == ord('k') :
			if pad_posx <= 4999 :
				lpad_pos += 1
			lpad.refresh(lpad_pos,0,8,columns+columns/4,rows+rows/2,columns+columns-4)
		elif cmd == ord('i') :
			if lpad_pos >= 1 :
				lpad_pos -= 1
			lpad.refresh(lpad_pos,0,8,columns+columns/4,rows+rows/2,columns+columns-4)
		elif cmd == ord('h') :
			show_help(rows,columns)
		elif cmd == ord('x') :
			break

curses.nocbreak(); scr.keypad(0); curses.echo()
curses.endwin()
