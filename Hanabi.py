import time
import os
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

originally was thinking parabolas, and that was getting copmlicated
and then DUH, i should just use classical physics, its so simple. 
have a starting velocity and angle, get the Vx and Vy from that, and just solve for new position each call
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
or dude just do WASD so you can do height and width also, for different dimension screens

I'll find a nice rate of fireworks for non-finale time
and after X updates it rolls to see if it goes into another non-finale stretch or into a finale
and repeat
so itll go in and out of finalle mode randomly
"""

class Composer:
	"""
	stores all the fireworks, adds them, removes them, puts them on a screen, and prints that screen

	has:
	list of fireworks
	a screen

	can:
	update fireworks
	add fireworks
	remove fireworks
	write firework content to screen
	print screen
	"""

	def __init__(self, screen):
		self.screen = screen
		self.fireworks = []

	def add_firework(self, firework):
		self.fireworks.append(firework)
	def remove_firework(self, firework):
		for smoke in firework.trail:
			self.screen.set_char(smoke.int_copy(), ' ')
		self.fireworks.remove(firework)
	def update_fireworks(self):
		for firework in self.fireworks:
			firework.fly(self)
	def write_fireworks(self):
		for firework in self.fireworks:
			self.screen.set_char(firework.position.int_copy(), firework.flame_char)
			if firework.dim:
				self.screen.set_char(firework.dim.int_copy(), firework.dim_char)

	def print_screen(self):
		self.screen.print()


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
		assert coord.x >= 0 and coord.x < self.width, "X Coordinate out of range"
		assert coord.y >= 0 and coord.y < self.height, "Y Coordinate out of range"
		self.content[self.y_max - coord.y][coord.x] = char

	def get_char(self, coord):
		"""
		returns the character at coordintate COORD
		"""
		assert coord.x >= 0 and coord.x < self.width, "X Coordinate out of range"
		assert coord.y >= 0 and coord.y < self.height, "Y Coordinate out of range"
		return self.content[self.y_max - coord.y][coord.x]

	def print(self):
		for row in self.content:
			line = ''
			for char in row:
				line += char
			print(line)

	def in_screen(self, coord):
		"""
		return whether coord is within screen
		"""
		return coord.x >= 0 and coord.x < self.width and coord.y >= 0 and coord.y < self.height 


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
	 a POSITION coordinate
	 a list of it's flame trails FLAME. stores 3 values and overwrites as adds more. can do self.time % 3
	 a TIMER, telling how long it will travel before popping
	 a V0, initial velocity
	 an ANGLE, degrees or radians?
	 a character to display flame, FLAME_CHAR
	 a character to display dim streak, DIM_CHAR
	 a FLAME_LENGTH which is length of flame trail, before turning dim
	 an attribute that tells it whether or not to split, SPLIT

	a FIREWORK can:
	fly through the air
	Pop

	*** eventually add a dead trail, like as it fades. so maybe flame is '*' or 'O' but then dead is 'o' or '.'
	this will replace flames that are X old with dead flames, 
	ALSO make it so when the time runs out it doesn't remove itself yet, instead it stops updating position but keeps
	making things dead, and then after that it removes itself. so there's a lag. for now skip this.
	you can just compare FADE to TIME to see what you should fade, and then write that, etc.
	"""
	grav = -0.1

	def __init__(self, position, v0, angle, timer, flame_char, dim_char, flame_length = 5, split = 1):
		self.position = position
		self.v0 = v0
		self.angle = math.radians(angle) #converts to radians, but i will write code using degrees
		self.timer = timer
		self.flame_char = flame_char
		self.dim_char = dim_char
		self.flame_length = flame_length
		self.split = split

		self.trail = [self.position.copy()]
		self.dim = None
		self.time = 0
		self.vx = math.cos(self.angle) * self.v0
		self.vy = math.sin(self.angle) * self.v0

	def fly(self, composer):
		"""
		using projectile motion, update position and add it to FLAME
		"""
		if self.time < self.timer:
			# print('position: ', self.position)
			# print('vx: ', self.vx)
			# print('vy: ', self.vy)
			self.position.x = self.position.x + self.vx
			self.position.y = self.position.y + self.vy
			
			self.trail.append(self.position.copy())

			self.vy = self.vy + self.grav
			self.time += 1

			if self.time >= self.flame_length:
				self.dim = self.trail[self.time - self.flame_length]

		else:
			self.pop(composer)

	def pop(self, composer):
		"""
		make more fireworks if split > 0, and delete self from wherever the list of all fireworks is stored

		consider saving the streaks later, but for now lets try without.
		"""
		if self.split > 0:
			print('pop')
		composer.remove_firework(self)




class Coord:
	"""
	simple coordinate with an X and Y value
	"""

	def __init__(self, x,y):
		self.x = x
		self.y = y

	def copy(self):
		return Coord(self.x, self.y)

	def int_copy(self):
		return Coord(round(self.x), round(self.y))

	def __str__(self):
		return '(' + str(self.x) + ', ' + str(self.y) +')'


def wait_sec(s):
	"""
	pauses command line for S seconds
	"""
	time.sleep(s)

def clear_screen():
	"""
	clears the command line screen
	"""
	os.system('cls')

sc = Screen(200, 50)
h = Composer(sc)
f = Firework(Coord(20,0), 3, 65, 35, 'O', '.')
h.add_firework(f)

while h.fireworks:
	h.write_fireworks()
	clear_screen()
	h.print_screen()
	h.update_fireworks()
	wait_sec(0.1)