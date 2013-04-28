#!/usr/bin/env python

import curses
import re

def show_help(rows,columns) :
	
	curses.curs_set(0)
	begin_x = columns-columns/2
	begin_y = rows/2
	height = rows
	width = columns
	helpwin = curses.newwin(height, width, begin_y, begin_x)
	helpwin.bkgd(curses.color_pair(0))
	helpwin.box()
	helpwin.addstr(1,columns/2-6,"---Hilfe---", curses.A_BOLD)
	helpwin.addstr(3,2,"h = diesen Hilfetext anzeigen")
	helpwin.addstr(4,2,"s = Seitenquelltext zeigen")
	helpwin.addstr(5,2,"j = Javascript anzeigen")
	helpwin.addstr(6,2,"u = URL eingeben")
	#helpwin.addstr(6,2,"a = Seiteninhalt nach links scrollen")
	#helpwin.addstr(7,2,"d = Seiteninhalt nach rechts scrollen")
	helpwin.addstr(7,2,"i = Linkliste nach oben scrollen")
	helpwin.addstr(8,2,"k = Linkliste nach unten scrollen")
	helpwin.addstr(9,2,"x = Programm beenden")
	helpwin.addstr(11,2,"Pfeiltasten = Seiteninhalt scrollen")
	helpwin.refresh()
	helpwin.getch()
	helpwin.clear()
	helpwin.refresh()

def regex(text,columns) :
	text1 = re.sub("<br\s*/?>", "\n",str(text))
	text1 = re.sub("<(script.*?|script)>([^<]+)<\/script>","[java-script]",text1)
	text1 = re.sub("<p.*?>","\n",text1)
	text1 = re.sub("<div.*?>","\n",text1)
	text1 = re.sub("<tr.*?>","\n",text1)
	text1 = re.sub("<.*?>","",text1)
	text1 = re.sub("(.{1,%i})(\s+|\Z)" %columns, "\\1\n", text1)
	return text1


