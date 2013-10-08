import pygame
from pygame.rect import Rect
from pygame.surface import Surface

__author__ = 'Donhilion'


class Collectable(object):
	""" The collectable class.

	An instance of this class represents a collectable, like a coin.

	Attributes:
		_pos: The position of the collectable.
		_value: The value of this collectable.
		_pic: The picture to display this collectable.
		_collision_rect: The rectangle used for checking for collision.
	"""

	def __init__(self, pos=None, size=None, value=5, pic=None):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the fields.
		If no picture is given a the rectangle determined by position and size will be filled.

		Args:
			pos: The position of the collectable.
			size: The size of the collectable.
			value: The value of the collectable.
			pic: The picture to display the collectable.
		"""
		if pos is None:
			pos = [0, 0]
		if size is None:
			size = [0, 0]
		self._pos = pos
		self._value = value
		if pic is None:
			self._pic = Surface(size)
			pygame.draw.rect(self._pic, (0, 255, 0), Rect((0, 0), size))
			self._collision_rect = Rect(pos, size())
		else:
			self._pic = pic
			self._collision_rect = Rect(pos, pic.get_size())

	def draw(self, surface, tick, camera, size):
		""" Draws the collectable.

		Draws this collectable on the given surface if it is in the horizontal range to be visible.

		Args:
			surface: The surface to draw on.
			tick: The current tick of the game. This argument is not used at the moment.
			camera: The position of the camera.
			size: The size of the window.
		"""
		if self._collision_rect.midright > camera[0] or self._pos[0] < camera[0] + size[0]:
			surface.blit(self._pic, (self._pos[0] - camera[0], self._pos[1] - camera[1]))

	def collides(self, rect):
		""" Checks if the collectable collides.

		This method checks if the collectable collides with the given rectangle.

		Args:
			rect: The rectangle to check with.

		Returns:
			True if the collectable collides with the given rectangle. False otherwise.
		"""
		return self._collision_rect.colliderect(rect)

	def get_value(self):
		""" Returns the value.

		This method returns the value of this collectable.

		Returns:
			The value of this collectable.
		"""
		return self._value

