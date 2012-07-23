import pygame
from pygame.locals import *
import logging

from ressources.pictures.picture_manager import PictureManager

class MenuEntry(object):

	def __init__(self, text, action):
		self.text = text
		self.action = action

class Menu(object):
	'''
	'''

	ENTRYS = (MenuEntry("Start", None), MenuEntry("Options", None),
		MenuEntry("Ende", exit))

	def __init__(self, screen, width, height):
		self.screen = screen
		self.width = width
		self.height = height
		self.bg = PictureManager.MANAGER.loaded["menuBackground.png"]
		self.bg = pygame.transform.scale(self.bg, (width, height))
		self.font = pygame.font.SysFont("arial", 24)
		self.font_height = self.font.get_linesize()
		self.selected = 0

	def draw(self):
		self.screen.blit(self.bg, (0,0))
		y = 0.5 * (self.height - len(Menu.ENTRYS) * (self.font_height + 5))
		i = 0
		for entry in Menu.ENTRYS:
			if self.selected == i:
				text = self.font.render(entry.text, True, (255, 255, 0))
			else:
				text = self.font.render(entry.text, True, (150, 150, 0))
			self.screen.blit(text, (8, y)) # TODO center text
			y += self.font_height + 5
			i += 1

	def key_down(self, key):
		if key == K_DOWN and self.selected < len(Menu.ENTRYS) - 1:
			self.selected += 1
		elif key == K_UP and self.selected > 0:
			self.selected -= 1
		elif key == K_RETURN:
			entry = Menu.ENTRYS[self.selected]
			if entry.action is not None:
				(entry.action)()


	def key_up(self, key):
		pass
		