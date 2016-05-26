import urllib
import json

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

    def KODI_GetItem(self, playerid):
        try:
            parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title"], "playerid": '+str(playerid)+' }, "id": "VideoGetItem"}')
            try:
                video_title = parsed_json['result']['item']['title']
                if video_title=="":
                    video_title = parsed_json['result']['item']['label']
                return video_title
            except KeyError:
                return ""
            except IndexError:
                return ""
        except ValueError:
            self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
            print 'Decoding JSON has failed'
            return ""  

    def KODI_GetItemA(self, playerid):
        try:
            parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title"], "playerid": '+str(playerid)+' }, "id": "AudioGetItem"}')
            try:
                audio_title = parsed_json['result']['item']['title']
                if audio_title=="":
                    audio_title = parsed_json['result']['item']['label']
                return audio_title
            except KeyError:
                return ""
            except IndexError:
                return ""
        except ValueError:
            self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
            print 'Decoding JSON has failed'
            return ""

    def KODI_GetProperties(self, playerid):
        try:
            parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetProperties", "params": { "playerid": '+str(playerid)+', "properties": ["speed","time","totaltime"] }, "id": 1}')
            try:
                speed = parsed_json['result']['speed']
                minutes_time = self.__format_to_minute(parsed_json['result']['time']['hours'],parsed_json['result']['time']['minutes'])
                minutes_timetotal = self.__format_to_minute(parsed_json['result']['totaltime']['hours'], parsed_json['result']['totaltime']['minutes'])

                return speed, minutes_time, minutes_timetotal
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

    def KODI_GetPropertiesA(self, playerid):
        try:
            parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetProperties", "params": { "playerid": '+str(playerid)+', "properties": ["time","totaltime"] }, "id": 1}')
            try:
                speeda = parsed_json['result']['speed']
                seconds_time = self.__format_to_seconds(parsed_json['result']['time']['minutes'],parsed_json['result']['time']['seconds'])
                seconds_timetotal = self.__format_to_seconds(parsed_json['result']['totaltime']['minutes'], parsed_json['result']['totaltime']['seconds'])

                return speeda,seconds_time, seconds_timetotal
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