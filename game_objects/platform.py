from ressources.pictures.picture_manager import PictureManager

__author__ = 'Donhilion'

from pygame import Surface, Rect

class Platform(object):

	def __init__(self, pos = [0, 0], size = [10,10], picture = None):
		self._pos = pos
		self.size = size
		self.surface = Surface(size)
		self.rect = Rect(pos, size)
		if picture is None:
			picture = PictureManager.MANAGER.loaded["grass.png"]
		x = 0
		y = 0
		pic_w = picture.get_width()
		pic_h = picture.get_height()
		while x < size[0]:
			while y < size[1]:
				self.surface.blit(picture, (x,y))
				y += pic_h
			y = 0
			x += pic_w


	def draw(self, surface, tick, camera, size):
		if self._pos[0] + self.size[0] > camera[0] or self._pos[0] < camera[0] + size[0]:
			surface.blit(self.surface, (self._pos[0] - camera[0], self._pos[1] - camera[1]))

	def collides(self, rect):
		return self.rect.colliderect(rect)