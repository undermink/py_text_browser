#!/usr/bin/env python

import curses
from bs4 import BeautifulSoup
from os import popen
import urllib
import re
from commands import *

body = ""
count = 0
linklist = ''
rows, columns = popen('stty size', 'r').read().split()
columns = int(columns) / 2
rows = int(rows) / 2
tworows = rows * 2
twocolumns = columns + columns
source = False
script = False
scr = curses.initscr()

curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
scr.border(0)
header = curses.newwin(1, (columns-2)*2, 1, 2)
header.addstr(0,columns-23, 10 * "#" + " undermink's Textbrowser " + 10 * "#")
header.bkgd(curses.color_pair(2))
getUrl = curses.newwin(1,(columns-2)*2,4,3)

scr.keypad(1)
scr.refresh()
header.refresh()
pad_pos = 0
pad_posx = 0
lpad_pos = 0
links = []
lnkdict = {}
url = getinput(getUrl)

try : Response = urllib.urlopen("http://"+url)
except : 

	scr.addstr(rows,columns-7,"!!!!ERROR!!!!\n", curses.A_BOLD)
	scr.refresh()
	scr.getch()
	exit(scr)

bs = BeautifulSoup(Response.read(), "lxml")

if Response.code != 200 :

	fehler = "Fehler: %i" % Response.code
	scr.addstr(rows,columns-5,fehler)
	
else : 

	pad = curses.newpad(10000,3000)
	pad.bkgd(curses.color_pair(3))
	urlheader = curses.newwin(1,columns,6,3)
	if bs.title :
		try : urlheader.addstr(0,0,bs.title.text, curses.color_pair(1))
		except : pass
	try: text = str(bs.body)
	except : pass
	
	text1 = regex(text,columns)
	urlheader.refresh()

	for line in text1.split("\n") :

		if line.strip() :
			
			body += line + "\n"

	try : 
		pad.addstr(body)
	except curses.error: pass
	curses.cbreak()
	curses.noecho()
	frames(rows,columns)
	pad.refresh(0,0,8,3,rows+(rows/4)*3,(columns+columns/4)-3)
	lpad = curses.newpad(5000,300)
	lpad.bkgd(curses.color_pair(2))
	for link in bs.find_all('a') :
		if link.get('href') != None :
			count += 1
			links.append(link.get("href"))
			lnkdict[count] = link.get("href")
			linklist += "[" + str(count) + "] " + link.text.strip() + " => " + link.get('href') + "\n"
	try: 
		utflinks = linklist.encode('utf-8', 'ignore')
		lpad.addstr(utflinks)
	except curses.error: pass
	lpad.refresh(0,0,8,columns+columns/4,rows+(rows/4)*3,columns+columns-4)


	
	while True:
		cmd = scr.getch()
		if  cmd == curses.KEY_DOWN :
			if pad_pos <= 10000 :
				pad_pos += 1
			frames(rows,columns)
			pad.clrtoeol()
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+(rows/4)*3, (columns+columns/4)-3)
			lpad.refresh(lpad_pos,0,8,columns+columns/4,rows+(rows/4)*3,columns+columns-4)
		elif  cmd == curses.KEY_UP :
			if pad_pos >= 1 :
				pad_pos -= 1
			frames(rows,columns)
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+(rows/4)*3, (columns+columns/4)-3)
			lpad.refresh(lpad_pos,0,8,columns+columns/4,rows+(rows/4)*3,columns+columns-4)
		elif cmd == curses.KEY_LEFT :
			if pad_posx >= 1 :
				pad_posx -= 1
			frames(rows,columns)
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+(rows/4)*3, (columns+columns/4)-3)
			lpad.refresh(lpad_pos,0,8,columns+columns/4,rows+(rows/4)*3,columns+columns-4)
		elif cmd == curses.KEY_RIGHT :
			if pad_posx <= 2999 :
				pad_posx += 1
			frames(rows,columns)
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+(rows/4)*3, (columns+columns/4)-3)
			lpad.refresh(lpad_pos,0,8,columns+columns/4,rows+(rows/4)*3,columns+columns-4)
		elif cmd == ord('k') :
			if pad_posx <= 4999 :
				lpad_pos += 1
			frames(rows,columns)
			lpad.refresh(lpad_pos,0,8,columns+columns/4,rows+(rows/4)*3,columns+columns-4)
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+(rows/4)*3, (columns+columns/4)-3)
		elif cmd == ord('i') :
			if lpad_pos >= 1 :
				lpad_pos -= 1
			frames(rows,columns)
			lpad.refresh(lpad_pos,0,8,columns+columns/4,rows+(rows/4)*3,columns+columns-4)
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+(rows/4)*3, (columns+columns/4)-3)
		elif cmd == ord('#') :
		    	number = linkwin(rows,columns)
			url = lnkdict[int(number)]
			try : Response = urllib.urlopen(url)
			except : pass
			pad.clear()
			lpad.clear()
			body = ''
			count = 0
			linklist = ''
			lnkdict = {}
			bs = BeautifulSoup(Response.read(), "lxml")
			try: urlheader.addstr(0,0,bs.title.text, curses.color_pair(1))
			except : pass
			try : text = bs.body
			except : pass
			text1 = regex(text,columns)
			for line in text1.split("\n") :
				if line.strip() :
					body += line + "\n"
			try : pad.addstr(body)
			except curses.error : pass
			for link in bs.find_all("a") :
			  	count += 1
				lnkdict[count] = link.get("href")
				linklist += "[" + str(count) + "] " + link.text.strip() + " => " + link.get('href') + "\n"
			frames(rows,columns)
			try :
			  	utflinks = linklist.encode('utf-8', 'ignore')
				lpad.addstr(utflinks)
			except curses.error: pass
			lpad.refresh(lpad_pos,0,8,columns+columns/4,rows+(rows/4)*3,columns+columns-4)
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+(rows/4)*3, (columns+columns/4)-3)
		elif cmd == ord('j') :
			if script == False :
				script = True
				js = ''
				for java in bs.find_all('script') :
					js += str(java) + "\n"
				pad.clear()
				js = re.sub("(.{1,%i})(\s+|\Z)" %columns, "\\1\n", js)
				pad.addstr(js)
			else :
				script = False
				pad.clear()
				try: pad.addstr(body)
				except curses.error: pass
			frames(rows,columns)
			lpad.refresh(lpad_pos,0,8,columns+columns/4,rows+(rows/4)*3,columns+columns-4)
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+(rows/4)*3, (columns+columns/4)-3)
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
				try: pad.addstr(body)
				except curses.error: pass
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+(rows/4)*3, (columns+columns/4)-3)
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
			try: text = bs.body
			except : pass
			text1 = regex(text,columns)
			body = ""
			count = 0
			linklist = ""
			for line in text1.split("\n") :
		
				if line.strip() :
		
					body += line + "\n"
		
			try: pad.addstr(body)
			except curses.error: pass
			pad.refresh(0,0,8,3,rows+(rows/4)*3,(columns+columns/4)-3)
			for link in bs.find_all('a') :
				if link.get('href') != None :
					count += 1
					linklist += "[" + str(count) + "] " + link.text.strip() + " => " + link.get('href') + "\n"
			try: 
				utflinks = linklist.encode('utf-8')
				lpad.addstr(utflinks)
			except curses.error: pass
			lpad.refresh(0,0,8,columns+columns/4,rows+(rows/4)*3,columns+columns-4)
		elif cmd == ord('h') :
			show_help(rows,columns)
			frames(rows,columns)
			lpad.refresh(lpad_pos,0,8,columns+columns/4,rows+(rows/4)*3,columns+columns-4)
			pad.refresh(pad_pos, pad_posx, 8, 3, rows+(rows/4)*3, (columns+columns/4)-3)
		elif cmd == ord('q') :
			break

exit(scr)
