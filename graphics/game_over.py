import pygame
from pygame.constants import K_ESCAPE
import window

__author__ = 'donhilion'

class GameOver(object):

	GAME_OVER_TEXT = "Game Over!"

	def __init__(self, screen, width, height, window):
		self.screen = screen
		self.width = width
		self.height = height
		self.window = window
		self.font = pygame.font.SysFont("arial", 40)
		self.font_height = self.font.get_linesize()

	def draw(self):
		self.screen.fill((0,0,0))
		text = self.font.render(GameOver.GAME_OVER_TEXT, True, (255, 0, 0))
		self.screen.blit(text, ((self.width - text.get_width()) / 2, (self.height - self.font_height) / 2))

	def key_down(self, key):
		if key == K_ESCAPE:
			self.window.switch(window.Window.MENU)

	def key_up(self, key):
		pass