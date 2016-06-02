import urllib
import json
from string import split

class KODI_WEBSERVER:

    ip_port = ""

    def __init__(self, helper, _ConfigDefault, draw_default):
        self.helper = helper
        self._ConfigDefault = _ConfigDefault
        self.draw_default = draw_default

        self.ip_port = 'http://'
        if self._ConfigDefault['KODI.webserver.user']!="" and self._ConfigDefault['KODI.webserver.pass']!="":
            self.ip_port = self.ip_port+self._ConfigDefault['KODI.webserver.user']+':'+self._ConfigDefault['KODI.webserver.pass']+'@'
        self.ip_port = self.ip_port+self._ConfigDefault['KODI.webserver.host']+':'+self._ConfigDefault['KODI.webserver.port']+'/jsonrpc?request='

    def __format_to_minute(self, hours,minutes):
        if hours > 0:
            hours = hours * 60
        return int(hours + minutes)

    def __format_to_seconds(self, minutes, seconds):
        if minutes > 0:
            minutes = minutes * 60
        return int(minutes + seconds)

    def getJSON(self, jsonconfig):
        try:
            self.draw_default.setInfoText("", self._ConfigDefault['color.white'])
            f = urllib.urlopen(self.ip_port+jsonconfig)
            json_string = f.read()
            return json.loads(json_string)
        except IOError:
            self.draw_default.setInfoText("NO KODI ACCESS!", self._ConfigDefault['color.red'])
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
        	parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title"], "playerid": '+str(playerid)+' }, "id": "AudioGetItem"}')
    	    except ValueError:
        	self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
        	print 'Decoding JSON has failed'
        	return ""
	else:
	    return ""

	try:
    	    title = parsed_json['result']['item']['title']
	    if title=="":
        	title = parsed_json['result']['item']['label']
            return title
	except KeyError:
    	    return ""
    	except IndexError:
    	    return ""

    def KODI_GetProperties(self, playerid):
        try:
            parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetProperties", "params": { "playerid": '+str(playerid)+', "properties": ["speed","time","totaltime"] }, "id": 1}')
            try:
		### print("Vprop=",parsed_json)
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
