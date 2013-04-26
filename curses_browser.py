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
source = False
scr = curses.initscr()

curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
scr.border(0)
header = curses.newwin(1, (columns-2)*2, 1, 2)
header.addstr(0,columns-23, 10 * "#" + " undermink's Textbrowser " + 10 * "#")
header.bkgd(curses.color_pair(2))
getUrl = curses.newwin(4,(columns-2)*2,4,3)
getUrl.addstr(0,0,"Bitte eine URL eingeben: ")
curses.echo()
scr.keypad(1)
curses.nocbreak()
scr.refresh()
header.refresh()
getUrl.refresh()
InputUrl = getUrl.getstr()
curses.curs_set(0)
pad_pos = 0
pad_posx = 0
lpad_pos = 0

url = InputUrl.strip("http://")
try: Response = urllib.urlopen("http://"+url)
except : scr.addstr(rows,columns-4,"wrong url")
bs = BeautifulSoup(Response.read(), "lxml")
if Response.code != 200 :

	fehler = "Fehler: %i" % Response.code
	scr.addstr(rows,columns-5,fehler)
	
else:

	pad = curses.newpad(10000,3000)
	pad.bkgd(curses.color_pair(3))
	urlheader = curses.newwin(1,columns,6,3)
	if bs.title :
		urlheader.addstr(0,0,bs.title.text, curses.color_pair(1))
	try: text = bs.body.text.strip()
	except : pass
	text1 = re.sub("(.{1,%i})(\s+|\Z)" %columns, "\\1\n", text)
	urlheader.refresh()

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
	lpad = curses.newpad(5000,300)
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
		elif cmd == ord('s') :
			if source == False :
				source = True
				pad.clear()
				src = str(bs.html)
				src = re.sub("(.{1,%i})(\s+|\Z)" %columns, "\\1\n", src)
				try: pad.addstr(src)
				except curses.error: pass
			else :
				source = False
				pad.clear()
				try:
					pad.addstr(utfbody)
				except curses.error: pass
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+rows/2, (columns+columns/4)-3)
		elif cmd == ord('u') :
			getUrl.clear()
			getUrl.addstr(0,0,"Bitte eine URL eingeben: ")
			curses.echo()
			InputUrl = getUrl.getstr()
			curses.noecho()
			curses.cbreak()
			pad.clear()
			pad_pos = 0
			pad_posx = 0
			lpad_pos = 0
			lpad.clear()
			url = InputUrl.strip("http://")
			try: Response = urllib.urlopen("http://"+url)
			except IOError: scr.addstr(rows,columns-4,"wrong url")
			bs = BeautifulSoup(Response.read(), "lxml")
			urlheader.clear()
			try: urlheader.addstr(0,0,bs.title.text, curses.color_pair(1))
			except : pass
			urlheader.refresh()
			try: text = bs.body.text.strip()
			except all: pass
			text1 = re.sub("(.{1,%i})(\s+|\Z)" %columns, "\\1\n", text)
			body = ""
			count = 0
			linklist = ""
			for line in text1.split("\n") :
		
				if line.strip() :
		
					body += line + "\n"
		
			#scr.addstr(8,1,body)
			utfbody = body.encode('utf-8')
			try: pad.addstr(utfbody)
			except curses.error: pass
			pad.refresh(0,0,8,3,rows+rows/2,(columns+columns/4)-3)
			for link in bs.find_all('a') :
				if link.get('href') != None :
					count += 1
					linklist += "[" + str(count) + "] " + link.text.strip() + " => " + link.get('href') + "\n"
			try: 
				utflinks = linklist.encode('utf-8')
				lpad.addstr(utflinks)
			except curses.error: pass
			lpad.refresh(0,0,8,columns+columns/4,rows+rows/2,columns+columns-4)
		elif cmd == ord('h') :
			show_help(rows,columns)
			#scr.redrawwin()
			#scr.touchwin()
			lpad.refresh(lpad_pos,0,8,columns+columns/4,rows+rows/2,columns+columns-4)
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+rows/2, (columns+columns/4)-3)
		elif cmd == ord('x') :
			break

curses.nocbreak(); scr.keypad(0); curses.echo()
curses.endwin()
