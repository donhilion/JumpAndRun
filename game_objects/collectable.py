import pygame
from pygame.rect import Rect
from pygame.surface import Surface

__author__ = 'donhilion'

class Collectable(object):

	def __init__(self, pos = [0, 0], size = [0, 0], value = 5, pic = None):
		self._pos = pos
		self._value = value
		if pic is None:
			self._pic = Surface(size)
			pygame.draw.rect(self._pic, (0,255,0), Rect((0,0), size))
			self._collision_rect = Rect(pos, size())
		else:
			self._pic = pic
			self._collision_rect = Rect(pos, pic.get_size())

	def draw(self, surface, tick, camera, size):
		if self._collision_rect.midright > camera[0] or self._pos[0] < camera[0] + size[0]:
			surface.blit(self._pic, (self._pos[0] - camera[0], self._pos[1] - camera[1]))

	def collides(self, rect):
		return self._collision_rect.colliderect(rect)

	def get_value(self):
		return self._value

