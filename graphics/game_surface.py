import pygame
from pygame.locals import *
import logging

from ressources.pictures.picture_manager import PictureManager
from graphics.drawables.animated import Animated
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
		
		# begin test
		from ressources.animations.animation_manager import AnimationManager
		animation_manager = AnimationManager.MANAGER
		animation = animation_manager.animations["animations.xml"]
		self.animated = Animated(PictureManager.MANAGER, animation[0], animation[1]["testAnim"])
		# end test

	def draw(self):
		x = 0
		while x < self.width:
			self.screen.blit(self.bg, (x,0))
			x += self.height

		tick = self.tick / 10

		# begin test
		self.animated.draw(self.screen, 150, 50, tick)
		# end test

		# calculate the ticks
		current_ticks = pygame.time.get_ticks()
		delta = (current_ticks - self.last_ticks)
		self.tick += delta
		self.last_ticks = current_ticks

	def key_down(self, key):
		if key == K_ESCAPE:
			self.window.switch(window.Window.MENU)

	def key_up(self, key):
		pass
