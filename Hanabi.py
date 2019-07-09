import time
import os
import random
import math
import msvcrt

"""
I'll find a nice rate of fireworks for non-finale time
and after X updates it rolls to see if it goes into another non-finale stretch or into a finale
and repeat
so itll go in and out of finale mode randomly
"""

def run():
	size_setter = make_splash(80, 20)
	# size_setter = make_splash(315, 80)
	done = False
	while not done:
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


	run_screen = Screen(size_setter.width, size_setter.height)
	h = Composer(run_screen)

	run_time = input('How many minutes?  Minutes: ')
	run_time = round(float(run_time) * 60 * 20)

	finale = False
	finale_frame = 0
	default_rate = 0.1
	firework_rate = default_rate
	for frame in range(run_time):
		# Randomly shoot fireworks, firework_rate chance every frame
		if random.random() < firework_rate:
			position = Coord(round(run_screen.width * 0.2 + random.random() * run_screen.width * 0.6), 0)
			v0 = random.random()*3+2
			angle = random.random()*90+45
			timer = random.random()*30+10
			h.add_firework(Firework(position, v0, angle, timer, '@', 'o'))

		if frame and frame % 300 == 0 and random.random() < 0.5:
			finale = True
			finale_frame = frame
			firework_rate = 0
		if finale and frame == finale_frame + 50:
			firework_rate = do_finale(h)
		if frame == finale_frame + 100:
			finale = False
			firework_rate = default_rate


		if frame > run_time - 400:
			firework_rate = 1

		h.write_fireworks()
		# clear_screen() #OLD PRINTING
		h.print_screen()
		# print("frame: ", frame)
		# print("number of fireworks: ", len(h.fireworks))
		h.update_fireworks()
		wait_sec(0.05)

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

	# def print(self):
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


# To spell out Hanabi:
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

def make_splash(width, height):
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


def do_finale(composer):
	"""
	make it so it randomly desides what KIND of finale. maybe it just returns 1 and thats it, so the rate goes up to 1 and it goes nuts,
	maybe it does whats below,
	maybe it shoots half from each side towards the middle
	those could be the three for now.
	"""
	screen = composer.screen

	choose = random.random()*4
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
		v0 = random.random()*1+3
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


# if random.random() < 0.1:
		# 	position = Coord(round(random.random() * run_screen.width), 0)
		# 	v0 = random.random()*3+2
		# 	angle = random.random()*90+45
		# 	timer = random.random()*30+10
		# 	firework = Firework(position, v0, angle, timer, '@', 'o')
		# 	h.add_firework(firework)