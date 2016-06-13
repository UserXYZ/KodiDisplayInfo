from datetime import timedelta
import re
from pygame import Rect

class DrawToDisplay_AudioTime:

	# default for 320x240
	_drawSetting = {}
	_drawSetting['audioinfo.progressbar.margin_top'] = 85
	_drawSetting['audioinfo.progressbar.height'] = 25

	_drawSetting['audioinfo.button.play'] = ""
	_drawSetting['audioinfo.button.break'] = ""
	_drawSetting['audioinfo.button.home'] = ""
	_drawSetting['audioinfo.button.rew'] = ""
	_drawSetting['audioinfo.button.ff'] = ""
	_drawSetting['audioinfo.button.stop'] = ""

	_drawSetting['audioinfo.title.fontsize'] = 40
	_drawSetting['audioinfo.title.height_margin'] = 4

	_drawSetting['audioinfo.time_now.fontsize'] = 60
	_drawSetting['audioinfo.time_now.height_margin'] = 68

	_drawSetting['audioinfo.time.fontsize'] = 38
	_drawSetting['audioinfo.time.margin_left'] = 0
	_drawSetting['audioinfo.time.margin_top'] = 54

	_drawSetting['audioinfo.menu.margin_top'] = 18
	_drawSetting['audioinfo.menu.margin_right'] = 4
	_drawSetting['audioinfo.menu.right'] = 0

	_drawSetting['title_start'] = 0
	_drawSetting['play_pause'] = Rect(0, 0, 0, 0)
	_drawSetting['home'] = Rect(0, 0, 0, 0)
	_drawSetting['ff'] = Rect(0, 0, 0, 0)
	_drawSetting['rew'] = Rect(0, 0, 0, 0)
	_drawSetting['stop'] = Rect(0, 0, 0, 0)

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
		self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_320x240.png')

		self._drawSetting['audioinfo.button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/48x48/button_play_320x240.png')
		self._drawSetting['audioinfo.button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/48x48/button_pause_320x240.png')
		self._drawSetting['audioinfo.button.home'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/32x32/button_home_320x240.png')
		self._drawSetting['audioinfo.button.rew'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/32x32/button_rew_320x240.png')
		self._drawSetting['audioinfo.button.ff'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/32x32/button_ff_320x240.png')
		self._drawSetting['audioinfo.button.stop'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/32x32/button_stop_320x240.png')
		self._drawSetting['audioinfo.button.menu'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/32x32/button_menu_320x240.png')

		self._drawSetting['audioinfo.menu.right'] = self.screen.get_width() - self._drawSetting['audioinfo.menu.margin_right']

	"""
	def SetupDrawSetting480x272(self):
		self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_480x272.png')
		self._drawSetting['startscreen.clock.fontsize'] = 64
		self._drawSetting['startscreen.clock.height_margin'] = 102

		self._drawSetting['audioinfo.progressbar.margin_top'] = 92
		self._drawSetting['audioinfo.progressbar.height'] = 34

		self._drawSetting['audioinfo.button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_play_480x320.png')
		self._drawSetting['audioinfo.button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_break_480x320.png')

		self._drawSetting['audioinfo.title.fontsize'] = 60
		self._drawSetting['audioinfo.title.height_margin'] = 5

		self._drawSetting['audioinfo.time_now.fontsize'] = 80
		self._drawSetting['audioinfo.time_now.height_margin'] = 86

		self._drawSetting['audioinfo.time.fontsize'] = 81
		self._drawSetting['audioinfo.time.margin_left'] = 14
		self._drawSetting['audioinfo.time.margin_top'] = 83

	def SetupDrawSetting480x320(self):
		self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_480x320.png')
		self._drawSetting['startscreen.clock.fontsize'] = 75
		self._drawSetting['startscreen.clock.height_margin'] = 118

		self._drawSetting['audioinfo.progressbar.margin_top'] = 120
		self._drawSetting['audioinfo.progressbar.height'] = 34

		self._drawSetting['audioinfo.button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_play_480x320.png')
		self._drawSetting['audioinfo.button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_break_480x320.png')

		self._drawSetting['audioinfo.title.fontsize'] = 60
		self._drawSetting['audioinfo.title.height_margin'] = 5

		self._drawSetting['audioinfo.time_now.fontsize'] = 80
		self._drawSetting['audioinfo.time_now.height_margin'] = 86

		self._drawSetting['audioinfo.time.fontsize'] = 81
		self._drawSetting['audioinfo.time.margin_left'] = 14
		self._drawSetting['audioinfo.time.margin_top'] = 83
	"""
	#def drawMenu(self) # menu bar, top right


	def drawProgressBar(self, play_time, play_time_done, margin_top=0):
		rect_bar = self.pygame.Rect((10,self._drawSetting['audioinfo.progressbar.margin_top']+margin_top), (self.screen.get_width()-20,self._drawSetting['audioinfo.progressbar.height']))

		if play_time_done > 0:
			percent_done = int(( 1. * rect_bar.width / play_time ) * play_time_done)
		else:
			percent_done = 0

		rect_done = self.pygame.Rect(rect_bar)
		rect_done.width = percent_done
		self.pygame.draw.rect(self.screen, self._ConfigDefault['color.green'], rect_bar)
		self.pygame.draw.rect(self.screen, self._ConfigDefault['color.orange'], rect_done)
		self.pygame.draw.rect(self.screen, self._ConfigDefault['color.white'], rect_bar, 1)

	def drawProperties(self, audio_title, time_now, speed, media_time, media_timetotal):
		margin_top = 0
		audioinfo_title_fontsize = self._drawSetting['audioinfo.title.fontsize']
		### convert media_time and media_timetotal to seconds
		seconds_time = self.helper.get_sec(media_time)
		seconds_timetotal = self.helper.get_sec(media_timetotal)
		### configure for resolutions
		"""
		if self._ConfigDefault['display.resolution']=="480x320":
			audioinfo_title_fontsize = 49
			margin_top = -18
			second_title_height_margin = -46
			max_chars = 17
		if self._ConfigDefault['display.resolution']=="480x272":
			audioinfo_title_fontsize = 42
			margin_top = -11
			second_title_height_margin = -40
			max_chars = 17
		"""
		if self._ConfigDefault['display.resolution']=="320x240":
			audioinfo_title_fontsize = 40
			margin_top = -16
			second_title_height_margin = -38
			max_chars = 14
		### if we want two line display
		if self._ConfigDefault['config.musictitleformat']=="twoline":
			### if title is longer than max_chars, break into two lines
			if len(audio_title) > max_chars:
				### break title
				line1 = audio_title[0:max_chars].strip()
				line2 = audio_title[max_chars:].strip()
				brk=0
				for i in re.finditer(r'\s|_',line1):
					brk=i.end()
				if brk > 0 and (max_chars - brk) < 2:
					line1 = audio_title[0:brk].strip()
					line2 = audio_title[brk:].strip()
				self.draw_default.displaytext(line1, audioinfo_title_fontsize, 10, self.screen.get_height()-self._drawSetting['audioinfo.title.height_margin']+second_title_height_margin, 'left', (self._ConfigDefault['color.white']))
				self.draw_default.displaytext(line2, audioinfo_title_fontsize, 10, self.screen.get_height()-self._drawSetting['audioinfo.title.height_margin'], 'left', (self._ConfigDefault['color.white']))
			else:
				self.draw_default.displaytext(audio_title, self._drawSetting['audioinfo.title.fontsize'], 10, self.screen.get_height()-self._drawSetting['audioinfo.title.height_margin'], 'left', (self._ConfigDefault['color.white']))
		### if we want single line display
		else:
			### scroll title if needed
			if len(audio_title) > max_chars:
				at = audio_title + " | "
				if self._drawSetting['title_start'] + max_chars <= len(at):
					buff = at[self._drawSetting['title_start']:self._drawSetting['title_start'] + max_chars]
				else:
					e = max_chars - (len(at)-self._drawSetting['title_start'] + 1)
					buff = at[self._drawSetting['title_start']:] + at[0:e+1]

				self._drawSetting['title_start'] += 1
				if self._drawSetting['title_start'] >= len(at):
					self._drawSetting['title_start'] = 0

				self.draw_default.displaytext(buff, self._drawSetting['audioinfo.title.fontsize'], 10, self.screen.get_height()-self._drawSetting['audioinfo.title.height_margin'], 'left', (self._ConfigDefault['color.white']))
			else: ### title is shorter than max_chars, show normally
				self.draw_default.displaytext(audio_title, self._drawSetting['audioinfo.title.fontsize'], 10, self.screen.get_height()-self._drawSetting['audioinfo.title.height_margin'], 'left', (self._ConfigDefault['color.white']))
		### draw time
		self.draw_default.displaytext(str(time_now.strftime("%H:%M")), self._drawSetting['audioinfo.time_now.fontsize'], 10, self._drawSetting['audioinfo.time_now.height_margin'], 'left', (self._ConfigDefault['color.white']))
		### calculate progress bar
		margin_progressbar = self._drawSetting['audioinfo.progressbar.margin_top']+self._drawSetting['audioinfo.progressbar.height']+margin_top
		### pad media_time and media_timetotal with zeros
		mtime = self.helper.add_zeros(media_time)
		mtime_total = self.helper.add_zeros(media_timetotal)
		### position of separator
		x1 = 62 + self._drawSetting['audioinfo.time.margin_left']
		x2 = self.screen.get_width()-10
		x3 = x1 + self.draw_default.get_text_w(mtime,self._drawSetting['audioinfo.time.fontsize'])
		x4 = x2 - self.draw_default.get_text_w(mtime_total,self._drawSetting['audioinfo.time.fontsize'])
		x5 = self.draw_default.get_text_w('/',self._drawSetting['audioinfo.time.fontsize']) / 2
		xx = ((x4 - x3) / 2) + x3 - x5
		### time played
		self.draw_default.displaytext(mtime, self._drawSetting['audioinfo.time.fontsize'], x1, margin_progressbar+self._drawSetting['audioinfo.time.margin_top'], 'left', (self._ConfigDefault['color.white']))
		### / separator
		self.draw_default.displaytext("/", self._drawSetting['audioinfo.time.fontsize'], xx, margin_progressbar+self._drawSetting['audioinfo.time.margin_top'], 'left', (self._ConfigDefault['color.white']))
		### total time
		self.draw_default.displaytext(mtime_total, self._drawSetting['audioinfo.time.fontsize'], x2, margin_progressbar+self._drawSetting['audioinfo.time.margin_top'], 'right', (self._ConfigDefault['color.white']))
		### draw progress bar
		self.drawProgressBar(seconds_timetotal, seconds_time, margin_top)
		### draw play/pause button
		if speed == 1: ### play
			self.screen.blit(self._drawSetting['audioinfo.button.play'], (8, margin_progressbar+8))
		else: ### pause
			self.screen.blit(self._drawSetting['audioinfo.button.break'], (8, margin_progressbar+8))
		### draw menu buttons
		self.screen.blit(self._drawSetting['audioinfo.button.menu'], (self._drawSetting['audioinfo.menu.right'] - 32, self._drawSetting['audioinfo.menu.margin_top']))
		self.screen.blit(self._drawSetting['audioinfo.button.ff'], (self._drawSetting['audioinfo.menu.right'] - 64, self._drawSetting['audioinfo.menu.margin_top']))
		self.screen.blit(self._drawSetting['audioinfo.button.rew'], (self._drawSetting['audioinfo.menu.right'] - 96, self._drawSetting['audioinfo.menu.margin_top']))
		self.screen.blit(self._drawSetting['audioinfo.button.stop'], (self._drawSetting['audioinfo.menu.right'] - 128, self._drawSetting['audioinfo.menu.margin_top']))

		### put clickable area over buttons
		r_play_pause = self._drawSetting['audioinfo.button.play'].get_rect().inflate(-4, -4)
		self._drawSetting['play_pause'] = Rect((8, margin_progressbar+8), (r_play_pause[2], r_play_pause[3]))

		r_home = self._drawSetting['audioinfo.button.menu'].get_rect().inflate(-8, -10)
		self._drawSetting['menu'] = Rect((self._drawSetting['audioinfo.menu.right'] - 32, self._drawSetting['audioinfo.menu.margin_top']), (r_home[2], r_home[3]))
		r_ff = self._drawSetting['audioinfo.button.ff'].get_rect().inflate(-6, -12)
		self._drawSetting['ff'] = Rect((self._drawSetting['audioinfo.menu.right'] - 64, self._drawSetting['audioinfo.menu.margin_top']), (r_ff[2], r_ff[3]))
		r_rew = self._drawSetting['audioinfo.button.rew'].get_rect().inflate(-6, -12)
		self._drawSetting['rew'] = Rect((self._drawSetting['audioinfo.menu.right'] - 96, self._drawSetting['audioinfo.menu.margin_top']), (r_rew[2], r_rew[3]))
		r_stop = self._drawSetting['audioinfo.button.stop'].get_rect().inflate(-8, -12)
		self._drawSetting['stop'] = Rect((self._drawSetting['audioinfo.menu.right'] - 128, self._drawSetting['audioinfo.menu.margin_top']), (r_stop[2], r_stop[3]))
