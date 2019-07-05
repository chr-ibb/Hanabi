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

	def __init__(self, width, height):
		self.width = width
		self.x_max = self.width - 1
		self.height = height
		self.y_max = height - 1
		self.content = [[' ' for _ in range(width)] for _ in range(height)]

	def set_char(self, coord, char):
		"""
		sets the character at coordinate COORD to be character CHAR
		"""
		assert coord.x > 0 and coord.x <= self.x_max, "X Coordinate out of range"
		assert coord.y > 0 and coord.y <= self.y_max, "Y Coordinate out of range"
		self.content[self.y_max - coord.y][coord.x] = char

	def get_char(self, coord):
		"""
		returns the character at coordintate COORD
		"""
		assert coord.x > 0 and coord.x <= self.x_max, "X Coordinate out of range"
		assert coord.y > 0 and coord.y <= self.y_max, "Y Coordinate out of range"
		return self.content[self.y_max - coord.y][coord.x]

	def print(self):
		for row in self.content:
			line = ''
			for char in row:
				line += char
			print(line)


class Firework:
	"""
	A firework that goes across the screen and either explodes into more fireworks, or terminates after reaching it's length or the end of the screen
	OR maybe just give them all lengths, and only have them update the screen if they would be ON the screen
	I like that more because then they can pop off screen but you'd see the result
	Will have a attribute that tells it how many more recursive calls are left,
	so you launch a firework, which splits into a bunch of other fireworks, and so on
	maybe each recursive call the LENGTH is halved

	can have 3 different kind of fireworks
	a standard that only recursively calls once
	a double that calls twice
	and a rando, where everything is random. can go nuts with this one. like maybe even only some of the offspring will have offspring, etc, and lengths can be rando

	a FIREWORK has:
	 a starting coordinate START
	 a list of it's flame trails FLAME
	 a LENGTH, telling how far it will travel before popping
	 an ANGLE, which is really the a value for ax^2 + bx + c
	 a LEFT_OR_RIGHT, which tells whether it launches towards the left or right (using parabolas, so have to know which direction we are going)
	 an attribute that tells it whether or not ot make more, MORE

	a FIREWORK can:
	fly through the air
	Pop
	"""

	def __init__(self, start, length, angle, left_or_right = 'right', more = 1):
		self.start = start
		self.flame = []
		self.length = length
		self.angle = angle
		self.left_or_right = left_or_right
		self.more = more 

	def fly(self):
		"""
		use y = a(x-h)^2 + k where a is the 'slope' more or less, h is the x-value of vertex, and k is y-value of vertex
		"""
		if left_or_right = 'right':
			#you have the left x-intercept and the 'skew', so solve for the equation
			# i need paper

	def pop(self):




class Coord:
	"""
	simple coordinate with an X and Y value
	"""

	def __init__(self, x,y):
		self.x = x
		self.y = y