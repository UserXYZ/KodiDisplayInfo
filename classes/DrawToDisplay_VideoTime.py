from datetime import timedelta
import re

class DrawToDisplay_VideoTime:

	# default for 320x240
	_drawSetting = {}
	_drawSetting['videoinfo.progressbar.margin_top'] = 85
	_drawSetting['videoinfo.progressbar.height'] = 25

	_drawSetting['videoinfo.button.play'] = ""
	_drawSetting['videoinfo.button.break'] = ""

	_drawSetting['videoinfo.title.fontsize'] = 40
	_drawSetting['videoinfo.title.height_margin'] = 4

	_drawSetting['videoinfo.time_now.fontsize'] = 60
	_drawSetting['videoinfo.time_now.height_margin'] = 68
	_drawSetting['videoinfo.time_end.fontsize'] = 60
	_drawSetting['videoinfo.time_end.height_margin'] = 68

	_drawSetting['videoinfo.time.fontsize'] = 38
	_drawSetting['videoinfo.time.margin_left'] = 0
	_drawSetting['videoinfo.time.margin_top'] = 54

	_drawSetting['title_start'] = 0

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

		self._drawSetting['videoinfo.button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_play_320x240.png')
		self._drawSetting['videoinfo.button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_break_320x240.png')
	"""
	def SetupDrawSetting480x272(self):
		self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_480x272.png')
		self._drawSetting['startscreen.clock.fontsize'] = 64
		self._drawSetting['startscreen.clock.height_margin'] = 102

		self._drawSetting['videoinfo.progressbar.margin_top'] = 92
		self._drawSetting['videoinfo.progressbar.height'] = 34

		self._drawSetting['videoinfo.button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_play_480x320.png')
		self._drawSetting['videoinfo.button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_break_480x320.png')

		self._drawSetting['videoinfo.title.fontsize'] = 60
		self._drawSetting['videoinfo.title.height_margin'] = 5

		self._drawSetting['videoinfo.time_now.fontsize'] = 80
		self._drawSetting['videoinfo.time_now.height_margin'] = 86
		self._drawSetting['videoinfo.time_end.fontsize'] = 80
		self._drawSetting['videoinfo.time_end.height_margin'] = 86

		self._drawSetting['videoinfo.time.fontsize'] = 81
		self._drawSetting['videoinfo.time.margin_left'] = 14
		self._drawSetting['videoinfo.time.margin_top'] = 83

	def SetupDrawSetting480x320(self):
		self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_480x320.png')
		self._drawSetting['startscreen.clock.fontsize'] = 75
		self._drawSetting['startscreen.clock.height_margin'] = 118

		self._drawSetting['videoinfo.progressbar.margin_top'] = 120
		self._drawSetting['videoinfo.progressbar.height'] = 34

		self._drawSetting['videoinfo.button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_play_480x320.png')
		self._drawSetting['videoinfo.button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_break_480x320.png')

		self._drawSetting['videoinfo.title.fontsize'] = 60
		self._drawSetting['videoinfo.title.height_margin'] = 5

		self._drawSetting['videoinfo.time_now.fontsize'] = 80
		self._drawSetting['videoinfo.time_now.height_margin'] = 86
		self._drawSetting['videoinfo.time_end.fontsize'] = 80
		self._drawSetting['videoinfo.time_end.height_margin'] = 86

		self._drawSetting['videoinfo.time.fontsize'] = 81
		self._drawSetting['videoinfo.time.margin_left'] = 14
		self._drawSetting['videoinfo.time.margin_top'] = 83
	"""
	def drawProgressBar(self, play_time, play_time_done, margin_top=0):
		rect_bar = self.pygame.Rect((10,self._drawSetting['videoinfo.progressbar.margin_top']+margin_top), (self.screen.get_width()-20,self._drawSetting['videoinfo.progressbar.height']))

		if play_time_done > 0:
			percent_done = int(( 1. * rect_bar.width / play_time ) * play_time_done)
		else:
			percent_done = 0

		rect_done = self.pygame.Rect(rect_bar)
		rect_done.width = percent_done
		self.pygame.draw.rect(self.screen, self._ConfigDefault['color.green'], rect_bar)
		self.pygame.draw.rect(self.screen, self._ConfigDefault['color.orange'], rect_done)
		self.pygame.draw.rect(self.screen, self._ConfigDefault['color.white'], rect_bar, 1)

	def drawProperties(self, video_title, time_now, speed, media_time, media_timetotal):
		margin_top = 0
		videoinfo_title_fontsize = self._drawSetting['videoinfo.title.fontsize']
		### convert media_time and media_timetotal to seconds
		seconds_time = self.helper.get_sec(media_time)
		seconds_timetotal = self.helper.get_sec(media_timetotal)
		### configure for resolutions
		"""
		if self._ConfigDefault['display.resolution']=="480x320":
			videoinfo_title_fontsize = 49
			margin_top = -18
			second_title_height_margin = -46
			max_chars = 17
		if self._ConfigDefault['display.resolution']=="480x272":
			videoinfo_title_fontsize = 42
			margin_top = -11
			second_title_height_margin = -40
			max_chars = 17
		"""
		if self._ConfigDefault['display.resolution']=="320x240":
			videoinfo_title_fontsize = 40
			margin_top = -16
			second_title_height_margin = -38
			max_chars = 14
		### if we want two line display
		if self._ConfigDefault['config.movietitleformat']=="twoline":
			### if title is longer than max_chars, break into two lines
			if len(video_title) > max_chars:
				### break title
				line1 = video_title[0:max_chars].strip()
				line2 = video_title[max_chars:].strip()
				brk=0
				for i in re.finditer(r'\s|_',line1):
					brk=i.end()
				if brk > 0 and (max_chars - brk) < 2:
					line1 = video_title[0:brk].strip()
					line2 = video_title[brk:].strip()
				self.draw_default.displaytext(line1, videoinfo_title_fontsize, 10, self.screen.get_height()-self._drawSetting['videoinfo.title.height_margin']+second_title_height_margin, 'left', (self._ConfigDefault['color.white']))
				self.draw_default.displaytext(line2, videoinfo_title_fontsize, 10, self.screen.get_height()-self._drawSetting['videoinfo.title.height_margin'], 'left', (self._ConfigDefault['color.white']))
			else:
				self.draw_default.displaytext(video_title, self._drawSetting['videoinfo.title.fontsize'], 10, self.screen.get_height()-self._drawSetting['videoinfo.title.height_margin'], 'left', (self._ConfigDefault['color.white']))
		### if we want single line display
		else:
			### scroll title if needed
			"""
			if len(video_title) > max_chars:
				### make buffer based on start position in the title
				buff = video_title[self._drawSetting['title_start']:self._drawSetting['title_start'] + max_chars]
				if (self._drawSetting['title_start'] + max_chars) < len(video_title):
					self._drawSetting['title_start'] += 1
				else:
					self._drawSetting['title_start'] = 0
			"""
			if len(video_title) > max_chars:
				vt = video_title + " | "
				if self._drawSetting['title_start'] + max_chars <= len(vt):
					buff = vt[self._drawSetting['title_start']:self._drawSetting['title_start'] + max_chars]
				else:
					e = max_chars - (len(vt)-self._drawSetting['title_start'] + 1)
					buff = vt[self._drawSetting['title_start']:] + vt[0:e+1]

				self._drawSetting['title_start'] += 1
				if self._drawSetting['title_start'] >= len(vt):
					self._drawSetting['title_start'] = 0

				self.draw_default.displaytext(buff, self._drawSetting['videoinfo.title.fontsize'], 10, self.screen.get_height()-self._drawSetting['videoinfo.title.height_margin'], 'left', (self._ConfigDefault['color.white']))
			else: ### title is shorter than max_chars, show normally
				self.draw_default.displaytext(video_title, self._drawSetting['videoinfo.title.fontsize'], 10, self.screen.get_height()-self._drawSetting['videoinfo.title.height_margin'], 'left', (self._ConfigDefault['color.white']))

		### draw time
		self.draw_default.displaytext(str(time_now.strftime("%H:%M")), self._drawSetting['videoinfo.time_now.fontsize'], 10, self._drawSetting['videoinfo.time_now.height_margin'], 'left', (self._ConfigDefault['color.white']))
		### calculate progress bar
		margin_progressbar = self._drawSetting['videoinfo.progressbar.margin_top']+self._drawSetting['videoinfo.progressbar.height']+margin_top

		### pad media_time and media_timetotal with zeros
		mtime = self.helper.add_zeros(media_time)
		mtime_total = self.helper.add_zeros(media_timetotal)
		### position of separator
		x1 = 62 + self._drawSetting['videoinfo.time.margin_left']
		x2 = self.screen.get_width()-10
		x3 = x1 + self.draw_default.get_text_w(mtime,self._drawSetting['videoinfo.time.fontsize'])
		x4 = x2 - self.draw_default.get_text_w(mtime_total,self._drawSetting['videoinfo.time.fontsize'])
		x5 = self.draw_default.get_text_w('/',self._drawSetting['videoinfo.time.fontsize']) / 2
		xx = ((x4 - x3) / 2) + x3 - x5
		### time played
		self.draw_default.displaytext(mtime, self._drawSetting['videoinfo.time.fontsize'], x1, margin_progressbar+self._drawSetting['videoinfo.time.margin_top'], 'left', (self._ConfigDefault['color.white']))
		### / separator
		self.draw_default.displaytext("/", self._drawSetting['videoinfo.time.fontsize'], xx, margin_progressbar+self._drawSetting['videoinfo.time.margin_top'], 'left', (self._ConfigDefault['color.white']))
		### total time
		self.draw_default.displaytext(mtime_total, self._drawSetting['videoinfo.time.fontsize'], x2, margin_progressbar+self._drawSetting['videoinfo.time.margin_top'], 'right', (self._ConfigDefault['color.white']))
		### draw progress bar
		self.drawProgressBar(seconds_timetotal, seconds_time, margin_top)
		### draw play/pause button
		if speed == 1: ### play
			self.screen.blit(self._drawSetting['videoinfo.button.play'], (8, margin_progressbar+8))
		else: ### pause
			self.screen.blit(self._drawSetting['videoinfo.button.break'], (8, margin_progressbar+8))

		### put rectangular areas over clickable buttons
		r = self._drawSetting['audioinfo.button.play'].get_rect().inflate(-4, -4)
		self._drawSetting['play_pause'] = Rect((8, margin_progressbar+8), (r[2], r[3]))

