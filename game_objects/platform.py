__author__ = 'Donhilion'

from pygame import Surface, Rect
import pygame

class Platform(object):

	def __init__(self, pos = [0, 0], size = [10,10]):
		self._pos = pos
		self.size = size
		self.surface = Surface(size)
		self.rect = Rect(pos, size)
		pygame.draw.rect(self.surface, (255,211,155), Rect((0,0), size))

	def draw(self, surface, tick):
		surface.blit(self.surface, self._pos)

	def collides(self, rect):
		return self.rect.colliderect(rect)