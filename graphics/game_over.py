import pygame
from pygame.constants import K_ESCAPE
import window

__author__ = 'Donhilion'


class GameOver(object):
	""" The game over class.

	An object of this class represents a game over screen.

	Attributes:
		_screen: The surface to draw on.
		_width: The width of the window.
		_height: The height of the window.
		_window: The surrounding window.
	"""

	# The text which will be shown.
	GAME_OVER_TEXT = "Game Over!"

	def __init__(self, screen, width, height, window):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.

		Args:
			screen: The surface of the window.
			width: The width of the window.
			height: The height of the window.
			window: The surrounding window.
		"""
		self._screen = screen
		self._width = width
		self._height = height
		self._window = window
		self._font = pygame.font.SysFont("arial", 40)
		self._font_height = self._font.get_linesize()

	def draw(self):
		""" Draws on the screen.

		This method draws on the screen.
		"""
		self._screen.fill((0, 0, 0))
		text = self._font.render(GameOver.GAME_OVER_TEXT, True, (255, 0, 0))
		self._screen.blit(text, ((self._width - text.get_width()) / 2, (self._height - self._font_height) / 2))

	def key_down(self, key):
		""" Handles key down events.

		This method handles key down events.
		The pressing of the escape button results in the changing to the menu screen.

		Args:
			key: The key event information provided by pygame.
		"""
		if key == K_ESCAPE:
			self._window.switch(window.Window.MENU)

	def key_up(self, key):
		""" Handles key up events.

		This method handles key up events.
		These events will be ignored.

		Args:
			key: The key event information provided by pygame.
		"""
		pass