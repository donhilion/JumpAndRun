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
		self.current_display = self.menu

	def start(self):
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					exit() # TODO: check what else has to be done
				elif event.type == KEYDOWN:
					self.current_display.key_down(event.key)
				elif event.type == KEYUP:
					self.current_display.key_up(event.key)

			self.current_display.draw()

			pygame.display.update()
