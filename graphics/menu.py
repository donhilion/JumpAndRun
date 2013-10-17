import pygame
from pygame.locals import *
import sys
from resources.pictures.picture_manager import PictureManager
import window

__author__ = 'Donhilion'


class MenuEntry(object):
	""" The menu entry class.

	An instance of this class represents a menu entry.

	Attributes:
		text: The text of the entry.
		action: The action to perform when the entry is selected.
	"""

	def __init__(self, text, action):
		self.text = text
		self.action = action


class Menu(object):
	""" The menu class.

	An instance of this class represents the menu screen.

	Attributes:
		_screen: The screen to draw on.
		_width: The width of the window.
		_height: The height of the window.
		_window: The surrounding window.
		_bg: The background picture.
		_font: The font to use.
		_font_height: The height of the used font.
		_selected: The index of the selected menu entry.
	"""

	# The menu entries to show.
	ENTRIES = (MenuEntry("Start", None), MenuEntry("Options", None),
			   MenuEntry("Ende", sys.exit))

	def __init__(self, screen, width, height, window):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.

		Args:
			screen: The screen to draw on.
			width: The width of the window.
			height: The height of the window.
			window: The surrounding window.
		"""
		self._screen = screen
		self._width = width
		self._height = height
		self._window = window
		self._bg = PictureManager.MANAGER.get_picture("menuBackground.png")
		self._bg = pygame.transform.scale(self._bg, (width, height))
		self._font = pygame.font.SysFont("arial", 24)
		self._font_height = self._font.get_linesize()
		self._selected = 0

		Menu.ENTRIES[0].action = self.to_game

	def draw(self):
		""" Draws the menu.

		This method draws the menu on the screen.
		"""
		self._screen.blit(self._bg, (0, 0))
		y = 0.5 * (self._height - len(Menu.ENTRIES) * (self._font_height + 5))
		i = 0
		for entry in Menu.ENTRIES:
			if self._selected == i:
				text = self._font.render(entry.text, True, (255, 255, 0))
			else:
				text = self._font.render(entry.text, True, (150, 150, 0))
			self._screen.blit(text, ((self._width - text.get_width()) / 2, y))
			y += self._font_height + 5
			i += 1

	def key_down(self, key):
		""" Handles key down events.

		This method handles key down events.
		The pressing of the up or down key changes the selected menu entry.
		The pressing of the return key performs the action corresponding to the selected menu entry.

		Args:
			key: The key event information provided by pygame.
		"""
		if key == K_DOWN and self._selected < len(Menu.ENTRIES) - 1:
			self._selected += 1
		elif key == K_UP and self._selected > 0:
			self._selected -= 1
		elif key == K_RETURN:
			entry = Menu.ENTRIES[self._selected]
			if entry.action is not None:
				entry.action()


	def key_up(self, key):
		""" Handles key up events.

		This method handles key up events.
		These events will be ignored.

		Args:
			key: The key event information provided by pygame.
		"""
		pass

	def to_game(self):
		""" Changes to the game.

		This method changes to the game surface.
		"""
		self._window.switch(window.Window.GAME)
		