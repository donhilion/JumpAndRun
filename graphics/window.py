import pygame
from pygame.locals import *
import logging
from graphics.game_over import GameOver

from ressources.settings.settings_manager import SettingsManager
from menu import Menu
from game_surface import GameSurface

class Window(object):
	''' The main window.
	'''

	MENU, GAME, GAME_OVER = range(3)

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
		self.menu = Menu(self.screen, self.width, self.height, self)
		self.game = GameSurface(self.screen, self.width, self.height, self)
		self.game_over = GameOver(self.screen, self.width, self.height, self)
		self.current_display = self.menu

	def start(self):
		last_update = pygame.time.get_ticks()
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

			current_update = pygame.time.get_ticks()
			delta = current_update - last_update
			last_update = current_update

			if delta < 16: # 16 for 60 fps
				pygame.time.wait(16-delta)


	def switch(self, type):
		if type == Window.MENU:
			self.current_display = self.menu
		elif type == Window.GAME:
			self.current_display = self.game
			self.game.reset_tick()
		elif type == Window.GAME_OVER:
			self.current_display = self.game_over
			self.game = GameSurface(self.screen, self.width, self.height, self) # reset game
