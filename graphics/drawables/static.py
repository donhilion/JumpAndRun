import pygame

__author__ = 'Donhilion'


class Static(object):
	""" The static class.

	Class for static object to draw.

	Attributes:
		_image: The image to draw.
	"""

	def __init__(self, picture_manager, frame):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.

		Args:
			picture_manager: The picture_manager to use.
			frame: The frame information to use.
		"""
		picture = picture_manager.loaded[frame[0]]
		rect = pygame.Rect(float(frame[1]), float(frame[2]),
						   float(frame[3]) - float(frame[1]),
						   float(frame[4]) - float(frame[2]))
		self._image = picture.subsurface(rect)


	def draw(self, surface, x, y):
		""" Draws this static.

		This method draws this static object on the given surface.

		Args:
			surface: The surface to draw on.
			x: The x coordinate.
			y: The y coordinate.
		"""
		surface.blit(self._image, x, y)