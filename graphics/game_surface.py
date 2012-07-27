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
		# begin test
		self.animated.draw(self.screen, 50, 50, self.tick)
		# end test
		self.tick += 1

	def key_down(self, key):
		if key == K_ESCAPE:
			self.window.switch(window.Window.MENU)

	def key_up(self, key):
		pass
