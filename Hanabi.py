"""
Learned:
printing more than one line at a time (was printing one line at a time at first)
a bunch of stuff, you came up with the idea to write this here after you finished this all, so you'll have to remember

TODO
Fill out these lists
manual finale functionality
make it run better (it lags when my laptop isn't plugged in, or when too many fireworks.)
maybe different kind of fireworks
maybe make it so by default it just runs, but you can always add in whatever kind of fireworks you want or start finales
	so you could be the composer

"""


import time
import os
import random
import math
import msvcrt


def run():
	"""
	Runs the fireworks. First it has the user set up the size of the screen, then it makes fireworks for as long as the user asked
	"""
	screen_size = setup_screen() # Show the splash screen, and use it to set the size of the screen for fireworks
	run_screen = Screen(screen_size[0], screen_size[1]) # initialize the screen that will be used to show the fireworks on
	h = Composer(run_screen) # initialize the composer that will store all the fireworks

	run_time = input('How many minutes?  Minutes: ')
	run_time = round(float(run_time) * 60 * 20) # set how long to run the fireworks for. Not accurate, actually represents how long the console is paused for

	finale = False # is there currently a finale happening?
	finale_frame = 0 # used to  know when the last finale started, for clearing the screen of fireworks before, and timing the launch
	default_rate = 0.1 # Default rate of fireworks, basically the chance a firework will be created every 0.05 seconds
	firework_rate = default_rate
	for frame in range(run_time): # Main loop
		if random.random() < firework_rate: # firework_rate chance to add a randomized firework to the composer
			position = Coord(round(run_screen.width * 0.2 + random.random() * run_screen.width * 0.6), 0)
			v0 = random.random()*3+2
			angle = random.random()*90+45
			timer = random.random()*30+10
			h.add_firework(Firework(position, v0, angle, timer, '@', 'o'))

		if frame and frame % 300 == 0 and random.random() < 0.5: # checks to see if it should start a finale
			finale = True
			finale_frame = frame
			firework_rate = 0
		if finale and frame == finale_frame + 50: # waits for 50 frames to actually start the finale, so the screen will be clear by then
			firework_rate = do_finale(h, random.random()*4)
		if frame == finale_frame + 100: # resets FINALE and  FIREWORK_RATE now that the finale is finished
			finale = False
			firework_rate = default_rate

		if frame > run_time - 400: # last 400 frames will have a lot of fireworks
			firework_rate = 1

		h.write_fireworks() # write all the fireworks to the screen
		# clear_screen() # OLD PRINTING
		h.print_screen() # print the screen
		# print("frame: ", frame)
		# print("number of fireworks: ", len(h.fireworks))
		h.update_fireworks() # update all the fireworks, using basic physics
		wait_sec(0.05) # wait between every loop. not as updating X times per second, but it's close enough

	print('The fireworks are over! See ya ~')


class Composer:
	"""
	Stores all the fireworks, adds them, removes them, puts them on a screen, and prints that screen
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

	# def print(self): # OLD PRINT METHOD that printed one line at a time. new one prints out the whole screen at once
	# 	for row in self.content:
	# 		line = ''
	# 		for char in row:
	# 			line += char
	# 		print(line)

	def print(self):
		to_print = ''
		for row in self.content:
			line = ''
			for char in row:
				line += char
			to_print = to_print + line + '\n'
		clear_screen()
		print(to_print)

	def in_screen(self, coord):
		"""
		return whether coord is within screen
		"""
		return coord.x >= 0 and coord.x < self.width and coord.y >= 0 and coord.y < self.height 


class Firework:
	"""
	
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
		firework pops, making new fireworks from it's position if split > 0
		firework removes itself from composer
		"""
		if self.split > 1:
			for firework in range(round(random.random()*75+75)):
				composer.add_firework(Firework(self.position.copy(), random.random()*5, random.random()*360, 20, '#', '~', 10, self.split - 1))
		elif self.split > 0:
			for firework in range(round(random.random()*50+50)):
				composer.add_firework(Firework(self.position.copy(), random.random()*5, random.random()*360, random.random()*15, '*', '.', 3, self.split - 1))
		composer.remove_firework(self)


class Coord:
	"""
	simple coordinate with an X and Y value
	"""

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def copy(self):
		return Coord(self.x, self.y)

	def int_copy(self):
		return Coord(round(self.x), round(self.y))

	def __str__(self):
		return '(' + str(self.x) + ', ' + str(self.y) +')'


# To spell out Hanabi in large letters:
title_char = '#'
p = title_char
hanabi_letters = []
hanabi_letters.append(list(' '*3 + p + ' '*3 + p + ' '*22 + p + ' '*7))
hanabi_letters.append(list(' '*3 + p + ' '*3 + p + ' '*22 + p + ' '*7))
hanabi_letters.append(list(' '*3 + p + ' '*3 + p + ' '*22 + p + ' '*7))
hanabi_letters.append(list(' '*2 + p + ' '*3 + p + ' '*22 + p + ' '*6 + p + ' '))
hanabi_letters.append(list(' '*2 + p*5 + ' '*3 + p*2 + ' '*4 + p + ' '*6 + p*2 + ' '*4 + p + ' '*8))
hanabi_letters.append(list(' '*2 + p + ' '*3 + p + ' '*2 + p + ' '*2 + p + ' '*3 + p*4 + ' '*2 + p + ' '*2 + p + ' '*3 + p*4 + ' '*2 + p + ' '*2))
hanabi_letters.append(list(' ' + p + ' '*3 + p + ' '*2 + p + ' '*3 + p + ' '*3 + p + ' '*2 + p + ' ' + p + ' '*3 + p + ' '*2 + p + ' '*3 + p + ' '*2 + p + ' '*2))
hanabi_letters.append(list(' ' + p + ' '*3 + p + ' '*2 + p + ' '*2 + p + ' ' + p + ' ' + p + ' '*2 + p + ' '*2 + p + ' '*2  + p + ' ' + p + ' ' + p + ' '*2 + p + ' '*2 + p + ' '*3))
hanabi_letters.append(list(' ' + p + ' '*3 + p + ' '*3 + p*2 + ' '*2 + p + ' ' + p + ' '*2 + p + ' '*3 + p*2 + ' '*2 + p + ' ' + p*4 + ' '*2 + p + ' '*3))


def make_splash(width, height): # makes a splash screen with WIDTH and HEIGHT dimensions. says Hanabi in the center of the screen
	splash = Screen(width, height)

	border_char = '#'
	hanabi_width = 38
	hanabi_height = 9
	for x in range(splash.width):
		splash.set_char(Coord(x, 0), border_char)
		splash.set_char(Coord(x, splash.height - 1), border_char)
	for y in range(splash.height):
		splash.set_char(Coord(0, y), border_char)
		splash.set_char(Coord(splash.width - 1, y), border_char)

	#bottom left corner of where letters should start
	letters_start = Coord((splash.width - hanabi_width) / 2, (splash.height - hanabi_height) / 2)
	letters_start = letters_start.int_copy()

	for x in range(hanabi_width):
		for y in range(hanabi_height):
			# print("x, y = ", x, ", ", y)
			splash.set_char(Coord(letters_start.x + x, letters_start.y + y), hanabi_letters[hanabi_height - 1 - y][x])

	return splash


def setup_screen(): # Setup the size of the screen that will show the fireworks
	size_setter = make_splash(80, 20) # Makes a splash screen of sorts, which is used to set the screen size
	# size_setter = make_splash(315, 80) # this is the size that fits the monitor I was using to write the code, actually a television
	done = False
	while not done: # loop until they finish setting the screen size
		clear_screen()
		size_setter.print()
		print('Use WASD to change size of the rectangle to fit your screen, then press Enter.')
		print('Try maximizing the window and setting the font to 12. Size:', size_setter.width, 'x', size_setter.height, ' (aim for 300x70)')
		print('Make sure you can still see the top edge of the rectangle.')
		# print('Size: ', size_setter.width, ' x ', size_setter.height, ' (aim for 300 x 70)')
		user_input = msvcrt.getwch()
		if user_input == 'w' or user_input == 'W':
			size_setter = make_splash(size_setter.width, size_setter.height - 5)
						
		if user_input == 'a' or user_input == 'A':
			size_setter = make_splash(size_setter.width - 5, size_setter.height)

		if user_input == 's' or user_input == 'S':
			size_setter = make_splash(size_setter.width, size_setter.height + 5)
			
		if user_input == 'd' or user_input == 'D':
			size_setter = make_splash(size_setter.width + 5, size_setter.height)
			
		if user_input == '\r' or user_input == 'e' or input == 'E':
			done = True
	return size_setter.width, size_setter.height


def do_finale(composer, choose):
	"""
	Does a finale, by adding a bunch of fireworks to the COMPOSER, or just changing the firework_rate to 1
	Currently there are 4 finales. By default, one of them is randomly picked
	finale 1 (CHOOSE between 0 and 1):
		shoots between 10 and 50 fireworks from one point in the center, bottom of the screen, all srpead out but in the same general direction
	finale 2 (CHOOSE between 1 and 2):
		shoots between 5 and 25 fireworks from each side,bottom of the screen, towards the center
	finale 3 (CHOOSE between 2 and 3):
		shoots one special firework with different ASCII characters, which splits into a bunch of fireworks when it pops, which all split again
	finale 4 (Choose between 3 and 4):
		makes the firework_rate 1, meaning a firework spawns every frame for the duration of the finale
	"""
	screen = composer.screen

	if choose < 1:
		position = Coord(screen.width*0.45 + random.random()*screen.width*0.1, 0)
		timer = random.random()*30+10
		f_angle = random.random()*60+60
		number_of_fireworks = round(10 + random.random()*40)
		for _ in range(number_of_fireworks):
			v0 = random.random()*3+2
			angle = f_angle - 45 + random.random()*90
			composer.add_firework(Firework(position.copy(), v0, angle, timer, '@', 'o'))
		return 0

	elif choose < 2:
		number_of_fireworks = round(5 + random.random()*20)
		timer = random.random()*20+20

		position = Coord(screen.width * 0.15, 0)
		f_angle = 45
		for _ in range(number_of_fireworks):
			v0 = random.random()*3+3
			angle = f_angle - 25 + random.random()*50
			composer.add_firework(Firework(position.copy(), v0, angle, timer, '@', 'o'))

		position = Coord(screen.width * 0.85, 0)
		f_angle = 135
		for _ in range(number_of_fireworks):
			v0 = random.random()*3+3
			angle = f_angle - 25 + random.random()*50
			composer.add_firework(Firework(position.copy(), v0, angle, timer, '@', 'o'))
		return 0

	elif choose < 3:
		position = Coord((screen.width * 0.4) + random.random()*screen.width * 0.2, 0)
		timer = random.random()*20+20
		angle = random.random()*90+45
		v0 = random.random()*2+2
		composer.add_firework(Firework(position.copy(), v0, angle, timer, '+', '-', round(timer / 2), 2))
		return 0

	else:
		return 1	


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