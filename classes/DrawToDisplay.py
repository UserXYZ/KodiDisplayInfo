from datetime import timedelta
import re
from pygame import Rect
import os

class DrawToDisplay:

	# default for 320x240
	_drawSetting = {}
	#_drawSetting['progressbar.margin_top'] = 85
	#_drawSetting['progressbar.height'] = 25
	_drawSetting['progressbar.margin_top'] = 85
	_drawSetting['progressbar.height'] = 20

	_drawSetting['button.play'] = ""
	_drawSetting['button.break'] = ""
	_drawSetting['button.home'] = ""
	_drawSetting['button.rew'] = ""
	_drawSetting['button.ff'] = ""
	_drawSetting['button.stop'] = ""
	_drawSetting['button.menu'] = ""

	_drawSetting['title.fontsize'] = 40
	_drawSetting['title.height_margin'] = 4

	#_drawSetting['time_now.fontsize'] = 60
	#_drawSetting['time_now.height_margin'] = 68
	_drawSetting['time_now.fontsize'] = 38
	_drawSetting['time_now.height_margin'] = 40

	_drawSetting['time.fontsize'] = 38
	_drawSetting['time.margin_left'] = 0
	_drawSetting['time.margin_top'] = 54

	_drawSetting['menu.margin_top'] = 18
	_drawSetting['menu.margin_right'] = 4
	_drawSetting['menu.right'] = 0
	_drawSetting['menu.space'] = 6

	_drawSetting['title_start'] = 0
	_drawSetting['play_pause'] = Rect(0, 0, 0, 0)
	_drawSetting['home'] = Rect(0, 0, 0, 0)
	_drawSetting['ff'] = Rect(0, 0, 0, 0)
	_drawSetting['rew'] = Rect(0, 0, 0, 0)
	_drawSetting['stop'] = Rect(0, 0, 0, 0)
	_drawSetting['menu'] = Rect(0, 0, 0, 0)

	def __init__(self, helper, _ConfigDefault):
		self.helper = helper
		self._ConfigDefault = _ConfigDefault
		self._drawSetting['title_start'] = 0

	def setPygameScreen(self, pygame, screen, draw_default):
		self.pygame = pygame
		self.screen = screen
		self.draw_default = draw_default
		getattr(self, 'SetupDrawSetting'+self._ConfigDefault['display.resolution'])()

	def SetupDrawSetting320x240(self):
		#self._drawSetting['button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/48x48/hicontrast/button_play_320x240.png')
		#self._drawSetting['button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/48x48/hicontrast/button_pause_320x240.png')
		self._drawSetting['button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/48x48/play.png')
		self._drawSetting['button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/48x48/pause.png')

		#self._drawSetting['button.home'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/32x32/hicontrast/button_home_320x240.png')
		#self._drawSetting['button.rew'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/32x32/hicontrast/button_rew_320x240.png')
		#self._drawSetting['button.ff'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/32x32/hicontrast/button_ff_320x240.png')
		#self._drawSetting['button.stop'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/32x32/hicontrast/button_stop_320x240.png')
		#self._drawSetting['button.menu'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/32x32/hicontrast/button_menu_320x240.png')

		self._drawSetting['button.home'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/48x48/home.png')
		self._drawSetting['button.rew'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/48x48/rew.png')
		self._drawSetting['button.ff'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/48x48/fwd.png')
		self._drawSetting['button.stop'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/48x48/stop.png')
		self._drawSetting['button.menu'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/48x48/menu.png')

		self._drawSetting['menu.right'] = self.screen.get_width() - self._drawSetting['menu.margin_right']

	#def drawMenu(self) # menu bar, top right

	def break_text(self, text, max_chars):
		if max_chars == 0:
			max_chars = 14
		line1 = text[0:max_chars].strip()
		line2 = text[max_chars:].strip()
		brk=0
		for i in re.finditer(r'\s|_', line1):
			brk=i.end()
		if brk > 0 and (max_chars - brk) < 2:
			line1 = text[0:brk].strip()
			line2 = text[brk:].strip()

		return line1, line2

	def drawPopUp(self, text):
		popcolor = [0, 97, 181]
		textcolor = [255,198, 0]

		font = self.pygame.font.Font(self._ConfigDefault['basedirpath']+"fonts/MC360.ttf", 32)
		text_size = font.size(text)
		if text_size[0] > (self.screen.get_width() - 20):
			line_spacing = -10
			line1, line2 = self.break_text(text, 0)
			line1_surface = font.render(line1, True, textcolor)
			line2_surface = font.render(line2, True, textcolor)
			y = line1_surface.get_height() + line2_surface.get_height()
			line_width = line1_surface.get_width() if line1_surface.get_width() >= line2_surface.get_width() else line2_surface.get_width()
			pop = self.pygame.Surface((line_width+20, y+10))
			pop.fill(popcolor)
			pop.blit(line1_surface, (pop.get_width()/2 - line_width/2, pop.get_height() - y + line_spacing))
			pop.blit(line2_surface, (pop.get_width()/2 - line_width/2, pop.get_height() - line2_surface.get_height() + line_spacing))
		else:
			text_surface = font.render(text, True, textcolor)
			pop = self.pygame.Surface((text_size[0]+20, text_size[1]+10))
			pop.fill(popcolor)
			pop.blit(text_surface, (pop.get_width()/2 - text_size[0]/2, pop.get_height()/2 - text_size[1]/2))

		self.screen.blit(pop, (self.screen.get_width()/2 - pop.get_width()/2, self.screen.get_height()/2 - pop.get_height()/2))

	def drawProgressBar(self, play_time, play_time_done, margin_top=0):
		rect_bar = self.pygame.Rect((10, self._drawSetting['progressbar.margin_top']+margin_top), (self.screen.get_width()-20, self._drawSetting['progressbar.height']))

		if play_time_done > 0:
			percent_done = int(( 1. * rect_bar.width / play_time ) * play_time_done)
		else:
			percent_done = 0

		rect_done = self.pygame.Rect(rect_bar)
		rect_done.width = percent_done
		self.pygame.draw.rect(self.screen, self._ConfigDefault['color.green'], rect_bar)
		self.pygame.draw.rect(self.screen, self._ConfigDefault['color.orange'], rect_done)
		self.pygame.draw.rect(self.screen, self._ConfigDefault['color.white'], rect_bar, 1)

	def drawProperties(self, title, time_now, speed, media_time, media_timetotal):
		margin_top = 0
		title_fontsize = self._drawSetting['title.fontsize']
		### convert media_time and media_timetotal to seconds
		seconds_time = self.helper.get_sec(media_time)
		seconds_timetotal = self.helper.get_sec(media_timetotal)
		### configure for resolutions

		if self._ConfigDefault['display.resolution']=="320x240":
			title_fontsize = 40
			margin_top = -16
			second_title_height_margin = -38
			max_chars = 14
		### if we want two line display
		if self._ConfigDefault['config.musictitleformat']=="twoline":
			### if title is longer than max_chars, break into two lines
			if len(title) > max_chars:
				### break title
				line1, line2 = self.break_text(title, max_chars)
				self.draw_default.displaytext(line1, title_fontsize, 10, self.screen.get_height()-self._drawSetting['title.height_margin']+second_title_height_margin, 'left', (self._ConfigDefault['color.white']))
				self.draw_default.displaytext(line2, title_fontsize, 10, self.screen.get_height()-self._drawSetting['title.height_margin'], 'left', (self._ConfigDefault['color.white']))
			else:
				self.draw_default.displaytext(title, self._drawSetting['title.fontsize'], 10, self.screen.get_height()-self._drawSetting['title.height_margin'], 'left', (self._ConfigDefault['color.white']))
		### if we want single line display
		else:
			### scroll title if needed
			if len(title) > max_chars:
				at = title + " | "
				if self._drawSetting['title_start'] + max_chars <= len(at):
					buff = at[self._drawSetting['title_start']:self._drawSetting['title_start'] + max_chars]
				else:
					e = max_chars - (len(at)-self._drawSetting['title_start'] + 1)
					buff = at[self._drawSetting['title_start']:] + at[0:e+1]

				self._drawSetting['title_start'] += 1
				if self._drawSetting['title_start'] >= len(at):
					self._drawSetting['title_start'] = 0

				self.draw_default.displaytext(buff, self._drawSetting['title.fontsize'], 10, self.screen.get_height()-self._drawSetting['title.height_margin'], 'left', (self._ConfigDefault['color.white']))
			else: ### title is shorter than max_chars, show normally
				self.draw_default.displaytext(title, self._drawSetting['title.fontsize'], 10, self.screen.get_height()-self._drawSetting['title.height_margin'], 'left', (self._ConfigDefault['color.white']))
		### draw time
		self.draw_default.displaytext(str(time_now.strftime("%H:%M")), self._drawSetting['time_now.fontsize'], 10, self._drawSetting['time_now.height_margin'], 'left', (self._ConfigDefault['color.white']))
		### calculate progress bar
		margin_progressbar = self._drawSetting['progressbar.margin_top']+self._drawSetting['progressbar.height']+margin_top
		### pad media_time and media_timetotal with zeros
		mtime = self.helper.add_zeros(media_time)
		mtime_total = self.helper.add_zeros(media_timetotal)
		### position of separator
		x1 = 62 + self._drawSetting['time.margin_left']
		x2 = self.screen.get_width()-10
		x3 = x1 + self.draw_default.get_text_w(mtime,self._drawSetting['time.fontsize'])
		x4 = x2 - self.draw_default.get_text_w(mtime_total,self._drawSetting['time.fontsize'])
		x5 = self.draw_default.get_text_w('/',self._drawSetting['time.fontsize']) / 2
		xx = ((x4 - x3) / 2) + x3 - x5
		### time played
		self.draw_default.displaytext(mtime, self._drawSetting['time.fontsize'], x1, margin_progressbar+self._drawSetting['time.margin_top'], 'left', (self._ConfigDefault['color.white']))
		### / separator
		self.draw_default.displaytext("/", self._drawSetting['time.fontsize'], xx, margin_progressbar+self._drawSetting['time.margin_top'], 'left', (self._ConfigDefault['color.white']))
		### total time
		self.draw_default.displaytext(mtime_total, self._drawSetting['time.fontsize'], x2, margin_progressbar+self._drawSetting['time.margin_top'], 'right', (self._ConfigDefault['color.white']))
		### draw progress bar
		self.drawProgressBar(seconds_timetotal, seconds_time, margin_top)
		### draw play/pause button
		if speed == 1: ### play
			self.screen.blit(self._drawSetting['button.play'], (8, margin_progressbar+8))
		else: ### pause
			self.screen.blit(self._drawSetting['button.break'], (8, margin_progressbar+8))
		### draw menu buttons
		#self.screen.blit(self._drawSetting['button.menu'], (self._drawSetting['menu.right'] - 32, self._drawSetting['menu.margin_top']))
		#self.screen.blit(self._drawSetting['button.ff'], (self._drawSetting['menu.right'] - 64, self._drawSetting['menu.margin_top']))
		#self.screen.blit(self._drawSetting['button.rew'], (self._drawSetting['menu.right'] - 96, self._drawSetting['menu.margin_top']))
		#self.screen.blit(self._drawSetting['button.stop'], (self._drawSetting['menu.right'] - 128, self._drawSetting['menu.margin_top']))
		
		self.screen.blit(self._drawSetting['button.menu'], (self._drawSetting['menu.right']-48-self._drawSetting["menu.space"], self._drawSetting['menu.margin_top']))
		self.screen.blit(self._drawSetting['button.ff'], (self._drawSetting['menu.right']-96-2*self._drawSetting["menu.space"], self._drawSetting['menu.margin_top']))
		self.screen.blit(self._drawSetting['button.rew'], (self._drawSetting['menu.right']-144-3*self._drawSetting["menu.space"], self._drawSetting['menu.margin_top']))
		self.screen.blit(self._drawSetting['button.stop'], (self._drawSetting['menu.right']-192-4*self._drawSetting["menu.space"], self._drawSetting['menu.margin_top']))
		
		### put clickable area over buttons
		r_play_pause = self._drawSetting['button.play'].get_rect().inflate(-4, -4)
		self._drawSetting['play_pause'] = Rect((8, margin_progressbar+8), (r_play_pause[2], r_play_pause[3]))
		r_menu = self._drawSetting['button.menu'].get_rect().inflate(-8, -10)
		self._drawSetting['menu'] = Rect((self._drawSetting['menu.right'] - 32, self._drawSetting['menu.margin_top']), (r_menu[2], r_menu[3]))
		r_ff = self._drawSetting['button.ff'].get_rect().inflate(-6, -12)
		self._drawSetting['ff'] = Rect((self._drawSetting['menu.right'] - 64, self._drawSetting['menu.margin_top']), (r_ff[2], r_ff[3]))
		r_rew = self._drawSetting['button.rew'].get_rect().inflate(-6, -12)
		self._drawSetting['rew'] = Rect((self._drawSetting['menu.right'] - 96, self._drawSetting['menu.margin_top']), (r_rew[2], r_rew[3]))
		r_stop = self._drawSetting['button.stop'].get_rect().inflate(-8, -12)
		self._drawSetting['stop'] = Rect((self._drawSetting['menu.right'] - 128, self._drawSetting['menu.margin_top']), (r_stop[2], r_stop[3]))
