from ressources.pictures.picture_manager import PictureManager

__author__ = 'Donhilion'

from pygame import Surface, Rect

class Platform(object):
	""" The platform class.

	An instance of this class represents a platform of a level.

	Attributes:
		_pos: The position of the platform.
		_size: The size of the platform.
		_surface: The visual representation of the platform.
		_rect: The rectangle for collision detection.
	"""

	def __init__(self, pos = (0, 0), size = (10,10), picture = None):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.

		Args:
			pos: The position of the platform.
			size: The size of the platform.
			picture: The picture for drawing the platform.
		"""
		self._pos = pos
		self._size = size
		self._surface = Surface(size)
		self._rect = Rect(pos, size)
		if picture is None:
			picture = PictureManager.MANAGER.loaded["grass.png"]
		x = 0
		y = 0
		pic_w = picture.get_width()
		pic_h = picture.get_height()
		while x < size[0]:
			while y < size[1]:
				self._surface.blit(picture, (x,y))
				y += pic_h
			y = 0
			x += pic_w


	def draw(self, surface, tick, camera, size):
		""" Draws the platform.

		This method draws the platform on the give surface if it is in the horizontal range to be visible.

		Args:
			surface: The surface to draw on.
			tick: The current tick of the game. This argument is not used at the moment.
			camera: The position of the camera.
			size: The size of the window.
		"""
		if self._pos[0] + self._size[0] > camera[0] or self._pos[0] < camera[0] + size[0]:
			surface.blit(self._surface, (self._pos[0] - camera[0], self._pos[1] - camera[1]))

	def collides(self, rect):
		""" Checks for collision.

		This method checks if the platform collides with the given rectangle.

		Args:
			rect: The rectangle to check with.

		Returns:
			True if the platform collides with the given rectangle. False otherwise.
		"""
		return self._rect.colliderect(rect)