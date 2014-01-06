import pygame
from pygame.locals import *
import logging
import sys
from graphics.game_over import GameOver
from graphics.settings_screen import SettingsScreen
from graphics.win_screen import WinScreen

from resources.settings.settings_manager import SettingsManager
from menu import Menu
from game_surface import GameSurface
from settings.settings import Settings

__author__ = 'Donhilion'


class Window(object):
	""" The window class.

	An instance of this class represents the main window.

	Attributes:
		_settings_manager: The settings manager.
		_width: The width of the window.
		_height: The height of the window.
		_screen: The screen to draw on.
		_menu: An instance of the menu class.
		_game: An instance of the game surface class.
		_game_over: An instance of the game over class.
		_current_display: The current display. This could be the menu, game surface, game over or win screen.
	"""

	# Values for the switch method.
	MENU, GAME, GAME_OVER, WIN_SCREEN, SETTINGS = range(5)
	# The name of the config file.
	GRAPHICS_CONFIG = "graphics.json"
	# The key for the window width.
	WIDTH_KEY = "width"
	# The key for the window height.
	HEIGHT_KEY = "height"

	def __init__(self):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.
		"""
		self._settings_manager = SettingsManager.MANAGER
		if self._settings_manager is not None:
			try:
				self._width = \
					self._settings_manager.get_setting(Window.GRAPHICS_CONFIG)[Window.WIDTH_KEY]
				self._height = \
					self._settings_manager.get_setting(Window.GRAPHICS_CONFIG)[Window.HEIGHT_KEY]
			except Exception, e:
				logging.error("Error while get window size")
				logging.error(e)
				self._width = 400
				self._height = 400
		else:
			logging.warn("No settings manager")
			self._width = 400
			self._height = 400
		self._settings = Settings()
		self._screen = pygame.display.set_mode((self._width, self._height), 0, 32)
		self._menu = Menu(self._screen, self._width, self._height, self)
		self._game = GameSurface(self._screen, self._width, self._height, self)
		self._game_over = GameOver(self._screen, self._width, self._height, self)
		self._win_screen = WinScreen(self._screen, self._width, self._height, self)
		self._settings_screen = SettingsScreen(self._screen, self._width, self._height, self, self._settings)
		self._current_display = self._menu

	def start(self):
		""" Starts the event handling.

		This method starts the event handling.
		"""
		last_update = pygame.time.get_ticks()
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit() # TODO: check what else has to be done
				elif event.type == KEYDOWN:
					self._current_display.key_down(event.key)
				elif event.type == KEYUP:
					self._current_display.key_up(event.key)
				elif event.type == MOUSEBUTTONUP:
					self._current_display.mouse_click(event.pos, event.button)
				elif event.type == MOUSEMOTION:
					self._current_display.mouse_move(event.pos)

			self._current_display.draw()
			pygame.display.update()

			current_update = pygame.time.get_ticks()
			delta = current_update - last_update
			last_update = current_update

			if delta < 16: # 16 for 60 fps
				pygame.time.wait(16 - delta)


	def switch(self, type, params=None):
		""" Switches the current display.

		Switches the current display according to the value in type.

		Args:
			type: Determines which display should be switched to. Valid values are MENU, GAME, GAME_OVER, WIN_SCREEN, SETTINGS.
			params: An optional list of parameters. This list will be forwarded to the new display.
					Currently only the win screen has parameters.
		"""
		if type == Window.MENU:
			self._current_display = self._menu
		elif type == Window.GAME:
			self._current_display = self._game
			self._game.get_settings(self._settings)
			self._game.reset_tick()
			self._game.start_music()
		elif type == Window.GAME_OVER:
			self._current_display = self._game_over
			self._game = GameSurface(self._screen, self._width, self._height, self) # reset game
		elif type == Window.WIN_SCREEN:
			self._win_screen.set_points(params)
			self._current_display = self._win_screen
			self._game = GameSurface(self._screen, self._width, self._height, self) # reset game
		elif type == Window.SETTINGS:
			self._current_display = self._settings_screen
