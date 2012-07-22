import pygame
from pygame.locals import *
import logging

from ressources.pictures.picture_manager import PictureManager

class Menu(object):
	'''
	'''

	def __init__(self, screen, width, height):
		self.screen = screen
		self.width = width
		self.height = height
		self.bg = PictureManager.MANAGER.loaded["menuBackground.png"]
		self.bg = pygame.transform.scale(self.bg, (width, height))

	def draw(self):
		self.screen.blit(self.bg, (0,0))
		