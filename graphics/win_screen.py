import pygame
from pygame.constants import K_ESCAPE
import window

__author__ = 'donhilion'

class WinScreen(object):

	WIN_TEXT = "Win!"

	def __init__(self, screen, width, height, window, points=0):
		self.screen = screen
		self.width = width
		self.height = height
		self.window = window
		self.font = pygame.font.SysFont("arial", 40)
		self.font_height = self.font.get_linesize()
		self._points = points

	def draw(self):
		self.screen.fill((0,0,0))
		text = self.font.render(WinScreen.WIN_TEXT, True, (0, 0, 255))
		self.screen.blit(text, ((self.width - text.get_width()) / 2, (self.height - self.font_height) / 2))
		points = self.font.render(str(self._points) + " Points", True, (0, 0, 255))
		self.screen.blit(points, ((self.width - text.get_width()) / 2, (self.height - self.font_height) / 2 + 50))

	def key_down(self, key):
		if key == K_ESCAPE:
			self.window.switch(window.Window.MENU)

	def set_points(self, points):
		self._points = points

	def key_up(self, key):
		pass
