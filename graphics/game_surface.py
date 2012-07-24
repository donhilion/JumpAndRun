import pygame
from pygame.locals import *
import logging

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

	def draw(self):
		x = 0
		while x < self.width:
			self.screen.blit(self.bg, (x,0))
			x += self.height

	def key_down(self, key):
		if key == K_ESCAPE:
			self.window.switch(window.Window.MENU)

	def key_up(self, key):
		pass
