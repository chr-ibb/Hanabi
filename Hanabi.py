import random
import math
import msvcrt

"""
set up a blank screen, x by y of ' '
randomly pick a spot on the bottom,
shoot a firework up
it explodes
firework and the explosions are represented by characters
for starters the firework can be an 'O'
and the explosions can be '~'

should i use parabolas?
probably
probably everything should be a parabola
so really i just need to write something that can draw a parabola from one end to the other
each firework will be a firework object, that draws to the screen,
so there can be more than one at a time
and you can set the amount of them
and maybe it fluctuates

lets use ARGS and command line options
--size small/medium/big
--height 
--width
eventually

actually scratch that
I want there to be a calibration at the start
you can cycle through different rectangles
and when it fits your screen you press enter
and it starts
so there will be a splash screen that says Hanabi with a rectangle around edges
and instructions "A: smaller" "D: bigger" "Press Enter"

I'll find a nice rate of fireworks for non-finale time
and after X updates it rolls to see if it goes into another non-finale stretch or into a finale
and repeat
so itll go in and out of finalle mode randomly
"""

class Screen:
	"""
	A screen of characters WIDTH wide and HEIGHT high. Characters stored in 2d list CONTENT. Can change individual characters based on coordinates, and print the screen
	"""

	def __init__(width, height):
		self.width = width
		self.height = height
		self.content = [[' ' for _ in range(width)] for _ in ranage(height)]

	def set_char(coord, char):
		"""
		sets the character at coordinate COORD to be character CHAR
		"""
		self.content[coord.y][coord.x] = char

	def get_char(coord):
		"""
		returns the character at coordintate COORD
		"""
		return self.content[coord.y][coord.x]\

	def print():
		for row in self.content:
			line = ''
			for char in row:
				line += char
			print(line)




class Coord:
	"""
	simple coordinate with an X and Y value
	"""

	def __init__(x,y):
		self.x = x
		self.y = y