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

	def draw(self, surface, tick, camera, size):
		if self._pos[0] + self.size[0] > camera[0] or self._pos[0] < camera[0] + size[0]:
			surface.blit(self.surface, (self._pos[0] - camera[0], self._pos[1] - camera[1]))

	def collides(self, rect):
		return self.rect.colliderect(rect)