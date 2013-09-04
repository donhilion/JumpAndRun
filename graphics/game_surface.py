import pygame
from pygame.locals import *
from game_objects.character import Character
from game_objects.platform import Platform
from game_objects.collectable import Collectable

from ressources.pictures.picture_manager import PictureManager
import window

class GameSurface(object):
	'''
	'''

	def __init__(self, screen, width, height, window):
		self.screen = screen
		self.width = width
		self.height = height
		self.window = window
		self.camera = [0,0]
		self.bg = PictureManager.MANAGER.loaded["background.png"]
		#self.bg = PictureManager.MANAGER.loaded["bg2.png"]
		self.bg = pygame.transform.scale(self.bg, (height, height))
		self.tick = 0
		self.last_ticks = pygame.time.get_ticks()
		self.dx = 0
		self.jumping = False
		self.font = pygame.font.SysFont("arial", 24)

		self.character = Character()
		self.platforms = []
		self.platforms.append(Platform((0, 200), (500, 50)))

		self.collectables = []
		self.collectables.append(Collectable((50,150), (10,10)))
		self.collectables.append(Collectable((150,150), (10,10)))
		self.collectables.append(Collectable((200,150), (10,10)))
		self.collectables.append(Collectable((250,150), (10,10)))

		self.deadzone = Rect((-1000, self.height), (300000, 1))

	def reset_tick(self):
		self.last_ticks = pygame.time.get_ticks()

	def draw(self):
		x = -(self.camera[0] % self.height)
		while x < self.width:
			self.screen.blit(self.bg, (x,0))
			x += self.height

		tick = self.tick / 10

		# calculate the ticks
		current_ticks = pygame.time.get_ticks()
		delta = (current_ticks - self.last_ticks)
		self.tick += delta
		self.last_ticks = current_ticks

		# handle the ticks
		for i in range(self.tick/10 - tick):
			# check walking collision
			standing = False
			for platform in self.platforms:
				if platform.collides(self.character._walking_line):
					standing = True
					break
			self.character._is_falling = not standing
			if standing and self.jumping:
				self.character.jump()
			self.character.tick(self.platforms, self.collectables)
			if self.dx != 0:
				self.character.move(self.dx, self.platforms)

			if self.character.is_colliding(self.deadzone):
				self.window.switch(window.Window.GAME_OVER)

		# center camera around player
		self.camera[0] = self.character.get_x() - self.width / 2

		# draw the platforms
		for platform in self.platforms:
			platform.draw(self.screen, tick, self.camera, (self.width, self.height))

		# draw collectables
		for collectable in self.collectables:
			collectable.draw(self.screen, tick, self.camera, (self.width, self.height))


		# draw the character
		self.character.draw(self.screen, tick, self.camera, (self.width, self.height))

		# draw points
		text = self.font.render(str(self.character.get_points()), True, (255, 255, 255))
		self.screen.blit(text, (self.width - text.get_width() - 10, 10))



	def key_down(self, key):
		if key == K_ESCAPE:
			self.window.switch(window.Window.MENU)
		elif key == K_RIGHT:
			self.dx += 1
		elif key == K_LEFT:
			self.dx -= 1
		elif key == K_UP:
			self.jumping = True

	def key_up(self, key):
		if key == K_RIGHT:
			self.dx -= 1
		elif key == K_LEFT:
			self.dx += 1
		elif key == K_UP:
			self.jumping = False
