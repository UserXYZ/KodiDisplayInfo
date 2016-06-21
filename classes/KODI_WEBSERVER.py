import json
import urllib2

class KODI_WEBSERVER:

	ip_port = ""

	def __init__(self, helper, _ConfigDefault, draw_default):
		self.helper = helper
		self._ConfigDefault = _ConfigDefault
		self.draw_default = draw_default

		self.ip_port = 'http://'
		if self._ConfigDefault['KODI.webserver.user']!="" and self._ConfigDefault['KODI.webserver.pass']!="":
			self.ip_port = self.ip_port+self._ConfigDefault['KODI.webserver.user']+':'+self._ConfigDefault['KODI.webserver.pass']+'@'
		self.ip_port = self.ip_port+self._ConfigDefault['KODI.webserver.host']+':'+self._ConfigDefault['KODI.webserver.port']+'/jsonrpc'

	def __format_to_seconds(self, minutes, seconds):
		if minutes > 0:
			minutes = minutes * 60
		return int(minutes + seconds)

	def getJSON(self, jsondata):
		headers = {'content-type': 'application/json'}
		self.draw_default.setInfoText("", self._ConfigDefault['color.white'])
		json_data = json.dumps(json.loads(jsondata))
		post_data = json_data.encode('utf-8')
		request = urllib2.Request(self.ip_port + '?request=', post_data, headers)
		try:
			result = urllib2.urlopen(request).read()
			result = json.loads(result.decode("utf-8"))
			return result
		except IOError:
			self.draw_default.setInfoText("NO KODI ACCESS!", self._ConfigDefault['color.red'])
			return json.loads('{"id":1,"jsonrpc":"2.0","result":[]}')

	def KODI_Cmd(self, playerid, cmd, params):
		headers = {'content-type': 'application/json'}
		if params == "":
			payload = '{"jsonrpc": "2.0", "method": "' + str(cmd) + '", "params": { "playerid": ' + str(playerid) + ' }, "id": 1}'
		else:
			payload = '{"jsonrpc": "2.0", "method": "' + str(cmd) + '", "params": { "playerid": ' + str(playerid) +', ' + str(params) + '}, "id": 1}'
		#print "cmd: " + payload
		json_data = json.dumps(json.loads(payload))
		post_data = json_data.encode('utf-8')
		request = urllib2.Request(self.ip_port, post_data, headers)
		try:
			result = urllib2.urlopen(request).read()
			result = json.loads(result.decode("utf-8"))
			return result
		except ValueError:
			self.draw_default.setInfoText("No response!", self._ConfigDefault['color.red'])
			return json.loads('{"id":1,"jsonrpc":"2.0","result":[]}')

	def KODI_GetActivePlayers(self):
		try:
			parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}')
			try:
				return parsed_json['result'][0]['playerid'], parsed_json['result'][0]['type']
			except KeyError:
				return 0, ""
			except IndexError:
				return 0, ""
		except ValueError:
			self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
			print 'Decoding JSON has failed'
			return ""

	def KODI_GetItem(self, playerid, mtype):
		if mtype == "video":
			try:
				parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title"], "playerid": '+str(playerid)+' }, "id": "VideoGetItem"}')
			except ValueError:
				self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
				print 'Decoding JSON has failed'
				return ""
		elif mtype == "audio":
			try:
				parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title", "album", "artist"], "playerid": '+str(playerid)+' }, "id": "AudioGetItem"}')
			except ValueError:
				self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
				print 'Decoding JSON has failed'
				return ""
		else:
			return ""

		try:
			title = parsed_json['result']['item']['title']
			if title == "":
				title = parsed_json['result']['item']['label']
			if mtype == "audio":
				album = parsed_json['result']['item']['album']
				artist = parsed_json['result']['item']['artist']
				return (title, album, artist)
			elif mtype == "video":
					return (title, '', '')
		except KeyError:
			return ""
		except IndexError:
			return ""

	def KODI_GetProperties(self, playerid):
		try:
			parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetProperties", "params": { "playerid": '+str(playerid)+', "properties": ["speed","time","totaltime"] }, "id": 1}')
			try:
				speed = parsed_json['result']['speed']
				media_time = str(parsed_json['result']['time']['hours'])+":"+str(parsed_json['result']['time']['minutes'])+":"+str(parsed_json['result']['time']['seconds'])
				media_timetotal = str(parsed_json['result']['totaltime']['hours'])+":"+str(parsed_json['result']['totaltime']['minutes'])+":"+str(parsed_json['result']['totaltime']['seconds'])
				return speed, media_time, media_timetotal
			except KeyError, e:
				print "KeyError: " + str(e)
				return 0,0,0
			except IndexError, e:
				print "IndexError: " + str(e)
				return 0,0,0
		except ValueError:
			self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
			print 'Decoding JSON has failed'
			return 0,0,0

	def KODI_Get_PL_Properties(self, playerid): # playlist properties
		try:
			parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetProperties", "params": { "playerid": '+str(playerid)+', "properties": ["playlistid","position"] }, "id": 1}')
			try:
				playlistid = parsed_json['result']['playlistid']
				position = parsed_json['result']['position']
			except KeyError, e:
				print "KeyError: " + str(e)
				return 0,0,0
			except IndexError, e:
				print "IndexError: " + str(e)
				return 0,0,0

			parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Playlist.GetProperties", "params": { "playlistid": '+str(playlistid)+', "properties": ["size"] }, "id": 1}')
			try:
				size = parsed_json['result']['size']
				return playlistid, position, size
			except KeyError, e:
				print "KeyError: " + str(e)
				return 0,0,0
			except IndexError, e:
				print "IndexError: " + str(e)
				return 0,0,0
		except ValueError:
			self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
			print 'Decoding JSON has failed'
			return 0,0,0

	def KODI_Get_Version(self):
		# retrieve current installed version
		try:
			parsed_json = self.getJSON('{ "jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["version", "name"]}, "id": 1 }')
			version_installed = []
			if parsed_json.has_key('result') and parsed_json['result'].has_key('version'):
				version_installed  = parsed_json['result']['version']
			return version_installed
		except KeyError:
			return ""
		except IndexError:
			return ""


