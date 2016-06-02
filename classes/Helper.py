import sys

class Helper(object):

	def __init__(self, _ConfigDefault):
	    self._ConfigDefault = _ConfigDefault
	### convert time to seconds
	def get_sec(self, s):
	    try:
		t = s.split(':')
		return int(t[0]) * 3600 + int(t[1]) * 60 + int(t[2])
	    except ValueError:
        	self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
        	print 'Converting time to seconds has failed'
        	return 0
	### pad media time with zeros
	def add_zeros(self,s):
	    try:
	    	t = s.split(':')
		return str(t[0]+':'+t[1].zfill(2)+':'+t[2].zfill(2))
	    except ValueError:
        	self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
        	print 'Padding time with zeroes has failed'
        	return 0

	#following from http://code.activestate.com/recipes/475186/
	def has_colours(self, stream):
	    if not hasattr(stream, "isatty"):
		return False
	    if not stream.isatty():
		return False # auto color only on TTYs
	    try:
		import curses
		curses.setupterm()
		return curses.tigetnum("colors") > 2
	    except:
		# guess false in case of error
		return False
	
	def printout(self, text, colour):
	    if not colour:
		colour=self._ConfigDefault['mesg.white']
	    if self.has_colours(sys.stdout):
		seq = "\x1b[1;%dm" % (colour) + text + "\x1b[0m"
		sys.stdout.write(seq)
	    else:
		sys.stdout.write(text)

	#following from http://code.activestate.com/recipes/266466/
	def HTMLColorToRGB(self, colorstring):
	    try:
	    # convert #RRGGBB to an (R, G, B) tuple
		colorstring = colorstring.strip()
		if colorstring[0] == '#':
		    colorstring = colorstring[1:]
		if len(colorstring) != 6:
		    raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
		r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
		r, g, b = [int(n, 16) for n in (r, g, b)]
		return (r, g, b)
	    except ValueError as text:
		self.printout("[error]   ", self._ConfigDefault['mesg.red'])
		print "Color Error RGB! " + str(text)
		exit()
