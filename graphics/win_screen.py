import pygame
from pygame.constants import K_ESCAPE
from graphics.screen import Screen
import window

__author__ = 'Donhilion'


class WinScreen(Screen):
	""" The win screen class.

	A instance of this class represents a win screen.

	Attributes:
		_screen: The screen to draw on.
		_width: The width of the window.
		_height: The height of the window.
		_window: The surrounding window.
		_font: The font to use.
		_font_height: The height of the used font.
		_points: The number of points to show.
	"""

	# The win text to show.
	WIN_TEXT = "Win!"

	def __init__(self, screen, width, height, window, points=0):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.

		Args:
			screen: The screen to draw on.
			width: The width of the window.
			height: The height of the window.
			window: The surrounding window.
			points: The number of points to show.
		"""
		self._screen = screen
		self._width = width
		self._height = height
		self._window = window
		self._font = pygame.font.SysFont("arial", 40)
		self._font_height = self._font.get_linesize()
		self._points = points

	def draw(self):
		""" Draws the win screen.

		Draws the win screen on the screen.
		This shows the win text and the achieved points.
		"""
		self._screen.fill((0, 0, 0))
		text = self._font.render(WinScreen.WIN_TEXT, True, (0, 0, 255))
		self._screen.blit(text, ((self._width - text.get_width()) / 2, (self._height - self._font_height) / 2))
		points = self._font.render(str(self._points) + " Points", True, (0, 0, 255))
		self._screen.blit(points, ((self._width - text.get_width()) / 2, (self._height - self._font_height) / 2 + 50))

	def key_down(self, key):
		""" Handles key down events.

		This method handles key down events.
		The pressing of the escape button results in the changing to the menu screen.

		Args:
			key: The key event information provided by pygame.
		"""
		if key == K_ESCAPE:
			self._window.switch(window.Window.MENU)

	def set_points(self, points):
		""" Sets the points.

		This method sets the value of the _points field.
		"""
		self._points = points
