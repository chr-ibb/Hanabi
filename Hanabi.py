import time
import os
import random
import math
import msvcrt

"""
so there will be a splash screen that says Hanabi with a rectangle around edges
and instructions "A: smaller" "D: bigger" "Press Enter"
or dude just do WASD so you can do height and width also, for different dimension screens

I'll find a nice rate of fireworks for non-finale time
and after X updates it rolls to see if it goes into another non-finale stretch or into a finale
and repeat
so itll go in and out of finalle mode randomly
"""

def run():
	size_setter = Screen(50, 20, '#')

	done = False
	while not done:
		clear_screen()
		size_setter.print()
		print('Hanabi')
		print('use WASD to change size of rectangle to fit your screen, then press Enter')
		user_input = msvcrt.getwch()
		if user_input == 'w' or input == 'W':
			size_setter = Screen(size_setter.width, size_setter.height - 5, size_setter.background)
						
		if user_input == 'a' or input == 'A':
			size_setter = Screen(size_setter.width - 5, size_setter.height, size_setter.background)

		if user_input == 's' or input == 'S':
			size_setter = Screen(size_setter.width, size_setter.height + 5, size_setter.background)
			
		if user_input == 'd' or input == 'D':
			size_setter = Screen(size_setter.width + 5, size_setter.height, size_setter.background)
			
		if user_input == '\r' or input == 'e' or input == 'E':
			done = True


	run_screen = Screen(size_setter.width, size_setter.height)
	h = Composer(run_screen)

	run_time = input('How many hours?  Hours: ')
	run_time = int(run_time)  * 60 * 60 * 20

	for _ in range(run_time):
		if random.random() < 0.1:
			firework = Firework(Coord(round(random.random() * 300 + 25), 0), random.random()*3+2, random.random()*90+45, random.random()*30+10, '@', 'o')
			h.add_firework(firework)
		h.write_fireworks()
		clear_screen()
		h.print_screen()
		h.update_fireworks()
		wait_sec(0.05)


	clear_screen()
	print('See ya next year!')

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
		for spot in firework.trail:
			int_spot = spot.int_copy()
			if self.screen.in_screen(int_spot):
				self.screen.set_char(int_spot, self.screen.background)
		self.fireworks.remove(firework)
	def update_fireworks(self):
		for firework in self.fireworks:
			firework.fly(self)
	def write_fireworks(self):
		for firework in self.fireworks:
			int_position = firework.position.int_copy()
			if self.screen.in_screen(int_position):
				self.screen.set_char(int_position, firework.flame_char)
			if firework.dim:
				int_dim = firework.dim.int_copy()
				if self.screen.in_screen(int_dim):
					self.screen.set_char(int_dim, firework.dim_char)

	def print_screen(self):
		self.screen.print()


class Screen:
	"""
	A screen of characters WIDTH wide and HEIGHT high. Characters stored in 2d list CONTENT. Can change individual characters based on coordinates, and print the screen
	"""

	def __init__(self, width, height, background = ' '):
		self.width = width
		self.x_max = self.width - 1
		self.height = height
		self.y_max = height - 1
		self.background = background
		self.content = [[self.background for _ in range(width)] for _ in range(height)]

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
	can have 3 different kind of fireworks
	a standard that only recursively calls once
	a double that calls twice
	and a rando, where everything is random. can go nuts with this one. like maybe even only some of the offspring will have offspring, etc, and lengths can be rando

	MAYBE make it so when the time runs out it doesn't remove itself yet, instead it stops updating position but keeps
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
		using projectile motion, update position and add it to TRAIL
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
		firework pops, making new fireworks from it's position if spliy > 0
		firework removes itself from composer
		"""
		if self.split > 0:
			for firework in range(round(random.random()*50+50)):
				composer.add_firework(Firework(self.position.copy(), random.random()*5, random.random()*360, random.random()*15, '*', '.', 3, self.split - 1))
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

run()