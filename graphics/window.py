import pygame
from pygame.locals import *
import logging

from ressources.settings.settings_manager import SettingsManager
from menu import Menu

class Window(object):
	''' The main window.
	'''
	def __init__(self):
		self.settings_manager = SettingsManager.MANAGER
		if self.settings_manager is not None:
			try:
				self.width = \
					self.settings_manager.settings["graphics.xml"]["width"]
				self.height = \
					self.settings_manager.settings["graphics.xml"]["height"]
			except Exception, e:
				logging.error("Error while get window size")
				logging.error(e)
				self.width = 400
				self.height = 400
		else:
			logging.warn("No settings manager")
			self.width = 400
			self.height = 400
		self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
		self.menu = Menu(self.screen, self.width, self.height)

	def start(self):
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					exit() # TODO: check what else has to be done

			#self.screen.fill((0, 0, 0))
			self.menu.draw()

			pygame.display.update()
