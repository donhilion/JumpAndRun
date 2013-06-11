import pygame
from pygame.locals import *
import logging
from game_objects.character import Character
from game_objects.platform import Platform

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
		self.bg = PictureManager.MANAGER.loaded["background.png"]
		self.bg = pygame.transform.scale(self.bg, (height, height))
		self.tick = 0
		self.last_ticks = pygame.time.get_ticks()
		self.dx = 0
		self.jumping = False

		self.character = Character()
		self.platforms = []
		self.platforms.append(Platform((0, 200), (500, 50)))

	def reset_tick(self):
		self.last_ticks = pygame.time.get_ticks()

	def draw(self):
		x = 0
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
			self.character.tick(self.platforms)
			if self.dx != 0:
				self.character.move(self.dx, self.platforms)

		# draw the platforms
		for platform in self.platforms:
			platform.draw(self.screen, tick)


		# draw the character
		self.character.draw(self.screen, tick)



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
