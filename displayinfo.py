#!/usr/bin/python
# KodiDisplayInfo v3.0
# Autor: Bjoern Reichert <opendisplaycase[at]gmx.net>
# License: GNU General Public License (GNU GPLv3)
#
# v1.0    XBMC 12 Frodo Release [April 2014]
# v1.1    ADD config.txt for Webserver
# v2.0    XBMC 13 Gotham
# v2.1    Bugfix: jsonrpc API - KeyError, IndexError
# v2.2    IF Player.GetItem title is empty check if label is set
# v3.0    Kodi 14 Release - Refactor Version
#         Published GitHub 03.10.2015
# v3.1    Watchmodus integration -> film (default), livetv [Asks the title more than once.]
# v3.2    Optimization movie title -> MOVIETITLEFORMAT -> oneline (default), twoline [smaller font size and optimized for two lines]
###
### Floyd's modifications
# v3.3    add separate audio display class, so you can have different settings for audio and video display
# v3.4    modify display, add title folding in two line mode on space and underscore
# v3.5    Add text scrolling for one line and text breaking for two line title display
# v3.6    Rewrite text scrolling to go circular; fix printing for unicode titles, hopefully

import os
import sys
import time
import datetime
import pygame
import ConfigParser
import unicodedata
import string
from pygame.locals import *
from classes.Helper import Helper
from classes.DrawToDisplay_Default import DrawToDisplay_Default
from classes.DrawToDisplay_VideoTime import DrawToDisplay_VideoTime
from classes.DrawToDisplay_AudioTime import DrawToDisplay_AudioTime
from classes.KODI_WEBSERVER import KODI_WEBSERVER

basedirpath = os.path.dirname(os.path.realpath(__file__)) + os.sep

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
ORANGE = (255,114,0)
GREEN = (0,255,0)

_ConfigDefault = {
	"basedirpath":              basedirpath,

	"mesg.grey":                30,
	"mesg.red":                 31,
	"mesg.green":               32,
	"mesg.yellow":              33,
	"mesg.blue":                34,
	"mesg.magenta":             35,
	"mesg.cyan":                36,
	"mesg.white":               37,

	"KODI.webserver.host":            "localhost",
	"KODI.webserver.port":            "8080",
	"KODI.webserver.user":            "",
	"KODI.webserver.pass":            "",

	"display.resolution":       "320x240",

	"config.screenmodus":       "time",
	"config.watchmodus":        "film",
	"config.movietitleformat":  "oneline",
	"config.musictitleformat":  "oneline",

	"color.black":              BLACK,
	"color.white":              WHITE,
	"color.red":                RED,
	"color.orange":             ORANGE,
	"color.green":              GREEN
	}

helper = Helper(_ConfigDefault)

# init config
helper.printout("[info]    ", _ConfigDefault['mesg.green'])
print "Parse Config"
configParser = ConfigParser.RawConfigParser()
configFilePath = r''+basedirpath+'config.txt'
configParser.read(configFilePath)
title = "" # has to be global so that draw_screen can use it only once
def_scr = "" # default screen exists

# check config
if configParser.has_option('CONFIG', 'SCREENMODUS'):
	temp = configParser.get('CONFIG', 'SCREENMODUS')
	if temp=="time" or temp=="thumbnail":
		_ConfigDefault['config.screenmodus'] = temp
	else:
		helper.printout("[warning]    ", _ConfigDefault['mesg.yellow'])
		print "Config [CONFIG] SCREENMODUS not set correctly - default is active!"

if configParser.has_option('CONFIG', 'WATCHMODUS'):
	temp = configParser.get('CONFIG', 'WATCHMODUS')
	if temp=="film" or temp=="livetv":
		_ConfigDefault['config.watchmodus'] = temp
	else:
		helper.printout("[warning]    ", _ConfigDefault['mesg.yellow'])
		print "Config [CONFIG] WATCHMODUS not set correctly - default is active!"

if configParser.has_option('CONFIG', 'MOVIETITLEFORMAT'):
	temp = configParser.get('CONFIG', 'MOVIETITLEFORMAT')
	if temp=="oneline" or temp=="twoline":
		_ConfigDefault['config.movietitleformat'] = temp
	else:
		helper.printout("[warning]    ", _ConfigDefault['mesg.yellow'])
		print "Config [CONFIG] MOVIETITLEFORMAT not set correctly - default is active!"

if configParser.has_option('CONFIG', 'MUSICTITLEFORMAT'):
	temp = configParser.get('CONFIG', 'MUSICTITLEFORMAT')
	if temp=="oneline" or temp=="twoline":
		_ConfigDefault['config.musictitleformat'] = temp
	else:
		helper.printout("[warning]    ", _ConfigDefault['mesg.yellow'])
		print "Config [CONFIG] MUSICTITLEFORMAT not set correctly - default is active!"

if configParser.has_option('DISPLAY', 'RESOLUTION'):
	temp = configParser.get('DISPLAY', 'RESOLUTION')
	if temp=="320x240" or temp=="480x272" or temp=="480x320":
		_ConfigDefault['display.resolution'] = temp
	else:
		helper.printout("[warning]    ", _ConfigDefault['mesg.yellow'])
		print "Config [DISPLAY] RESOLUTION not set correctly - default is active!"

if configParser.has_option('KODI_WEBSERVER', 'HOST'):
	_ConfigDefault['KODI.webserver.host'] = configParser.get('KODI_WEBSERVER', 'HOST')
if configParser.has_option('KODI_WEBSERVER', 'PORT'):
	_ConfigDefault['KODI.webserver.port'] = configParser.get('KODI_WEBSERVER', 'PORT')
if configParser.has_option('KODI_WEBSERVER', 'USER'):
	_ConfigDefault['KODI.webserver.user'] = configParser.get('KODI_WEBSERVER', 'USER')
if configParser.has_option('KODI_WEBSERVER', 'PASS'):
	_ConfigDefault['KODI.webserver.pass'] = configParser.get('KODI_WEBSERVER', 'PASS')

if configParser.has_option('COLOR', 'BLACK'):
	_ConfigDefault['color.black'] = helper.HTMLColorToRGB(configParser.get('COLOR', 'BLACK'))
if configParser.has_option('COLOR', 'WHITE'):
	_ConfigDefault['color.white'] = helper.HTMLColorToRGB(configParser.get('COLOR', 'WHITE'))
if configParser.has_option('COLOR', 'RED'):
	_ConfigDefault['color.red'] = helper.HTMLColorToRGB(configParser.get('COLOR', 'RED'))
if configParser.has_option('COLOR', 'GREEN'):
	_ConfigDefault['color.green'] = helper.HTMLColorToRGB(configParser.get('COLOR', 'GREEN'))
if configParser.has_option('COLOR', 'ORANGE'):
	_ConfigDefault['color.orange'] = helper.HTMLColorToRGB(configParser.get('COLOR', 'ORANGE'))

#Display FB
if configParser.get('DISPLAY', 'FBDEV') != "":
	os.environ["SDL_FBDEV"] = configParser.get('DISPLAY', 'FBDEV')

def remove_control_chars(s):
	return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def draw_screen(screen):
	global title

	time_now = datetime.datetime.now()
	###start draw, clear screen first
	screen.fill(_ConfigDefault['color.black'])
	### get type of player
	playerid, playertype = KODI_WEBSERVER.KODI_GetActivePlayers()

	### video player active
	if playertype == "video" and int(playerid) > 0:
		if _ConfigDefault['config.watchmodus']=="livetv":
			title = remove_control_chars(KODI_WEBSERVER.KODI_GetItem(playerid, "video")).strip()
		else:
			tt = remove_control_chars(KODI_WEBSERVER.KODI_GetItem(playerid, "video")).strip()
			if tt != title or title == "":
				title = tt
				draw_videotime._drawSetting['title_start'] = 0
				helper.printout("[info]    ", _ConfigDefault['mesg.green'])
				print "Video: " + title

		### get status times
		speed, media_time, media_timetotal = KODI_WEBSERVER.KODI_GetProperties(playerid)
		### convert media_timetotal to seconds
		seconds_timetotal = helper.get_sec(media_timetotal)

		if seconds_timetotal > 0:
			if _ConfigDefault['config.screenmodus']=="time":
				draw_videotime.drawProperties(title, time_now, speed, media_time, media_timetotal)
	### audio player active
	elif playertype == "audio" and int(playerid) >= 0:
		if _ConfigDefault['config.watchmodus']=="livetv":
			title = remove_control_chars(KODI_WEBSERVER.KODI_GetItem(playerid, "audio")).strip()
		else:
			tt = remove_control_chars(KODI_WEBSERVER.KODI_GetItem(playerid, "audio")).strip()
			if tt != title or title == "":
				title = tt
				draw_audiotime._drawSetting['title_start'] = 0
				helper.printout("[info]    ", _ConfigDefault['mesg.green'])
				print "Audio: " + title

		### get status times
		speed, media_time, media_timetotal = KODI_WEBSERVER.KODI_GetProperties(playerid)
		### convert media_timetotal to seconds
		seconds_timetotal = helper.get_sec(media_timetotal)

		if seconds_timetotal > 0:
			if _ConfigDefault['config.screenmodus']=="time":
				draw_audiotime.drawProperties(title, time_now, speed, media_time, media_timetotal)
	### something else
	else:
		# API has nothing, clear all values
		title = ""
		draw_audiotime._drawSetting['play_pause'] = Rect(0, 0, 0, 0) # null button
		draw_default.drawLogoStartScreen(time_now)
		draw_videotime._drawSetting['title_start'] = 0
		draw_audiotime._drawSetting['title_start'] = 0

def main_exit():
	pygame.quit()
	sys.exit()

def main():
	UPDATE_SCREEN = 500
	clock = pygame.time.Clock()
	update_screen = pygame.USEREVENT + 1

	helper.printout("[info]    ", _ConfigDefault['mesg.cyan'])
	print "Start: KodiDisplayInfo"

	pygame.init()
	screen = pygame.display.set_mode(getattr(draw_default, 'Screen'+_ConfigDefault['display.resolution'])(), 0, 32)
	pygame.display.set_caption('KodiDisplayInfo')
	pygame.mouse.set_visible(1)

	res = KODI_WEBSERVER.KODI_Get_Version()

	draw_default.setPygameScreen(pygame, screen)
	draw_videotime.setPygameScreen(pygame, screen, draw_default)
	draw_audiotime.setPygameScreen(pygame, screen, draw_default)
	### start timer for screen update
	pygame.time.set_timer(update_screen, UPDATE_SCREEN)
	# run the game loop
	running = True
	try:
		while running:
			clock.tick(30)
			try:
				for event in pygame.event.get():
					if event.type == pygame.MOUSEBUTTONDOWN:
						mousepress = pygame.mouse.get_pressed()
						mousepos = pygame.mouse.get_pos()
						if mousepress[0]:
							playerid, playertype = KODI_WEBSERVER.KODI_GetActivePlayers()
							if int(playerid) >=0:
								if draw_audiotime._drawSetting['play_pause'].collidepoint(mousepos): # play/pause button
									print "play/pause"
									res = KODI_WEBSERVER.KODI_Cmd(playerid, 'Player.PlayPause')
								if draw_audiotime._drawSetting['home'].collidepoint(mousepos): # home button
									print "home"
								if draw_audiotime._drawSetting['menu'].collidepoint(mousepos): # home button
									print "menu"
								if draw_audiotime._drawSetting['ff'].collidepoint(mousepos): # forward button
									print "forward"
									if int(res['major']) < 16:
										res = KODI_WEBSERVER.KODI_Cmd(playerid, 'Player.GoNext')
									#else:
									#	res = KODI_WEBSERVER.KODI_Cmd(playerid, 'Player.GoTo')
								if draw_audiotime._drawSetting['rew'].collidepoint(mousepos): # back button
									print "back"
									if int(res['major']) < 16:
										res = KODI_WEBSERVER.KODI_Cmd(playerid, 'Player.GoPrevious')
									#else:
									#	res = KODI_WEBSERVER.KODI_Cmd(playerid, 'Player.GoTo')
								if draw_audiotime._drawSetting['stop'].collidepoint(mousepos): # stop button
									print "stop"
									res = KODI_WEBSERVER.KODI_Cmd(playerid, 'Player.Stop')

					if event.type == pygame.KEYDOWN:
						print "key"
					if event.type == pygame.QUIT: ### closed window
						running = False
					if event.type == update_screen:
						draw_screen(screen)
			except KeyboardInterrupt:
				pygame.quit()

			pygame.display.flip()
			time.sleep(0.1)
			#pygame.time.wait(500)
			###pygame.display.update() # ? necessary ?

		### window closed, normal exit
		helper.printout("[end]     ", _ConfigDefault['mesg.magenta'])
		print "bye ..."
		main_exit()
	except SystemExit:
		main_exit()
	except KeyboardInterrupt:
		main_exit()

### main program
if __name__ == "__main__":
	draw_default = DrawToDisplay_Default(helper, _ConfigDefault)

	if _ConfigDefault['config.screenmodus']=="time":
		draw_videotime = DrawToDisplay_VideoTime(helper, _ConfigDefault)
		draw_audiotime = DrawToDisplay_AudioTime(helper, _ConfigDefault)

	KODI_WEBSERVER = KODI_WEBSERVER(helper, _ConfigDefault, draw_default)
	main()
