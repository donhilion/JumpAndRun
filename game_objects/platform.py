from pygame import Surface, Rect

from resources.pictures.picture_manager import PictureManager
from utils.vector import Vector2


__author__ = 'Donhilion'


class Platform(object):
	""" The platform class.

	An instance of this class represents a platform of a level.

	Attributes:
		_pos: The position of the platform.
		_size: The size of the platform.
		_surface: The visual representation of the platform.
		_rect: The rectangle for collision detection.
	"""

	def __init__(self, pos=(0, 0), size=(10, 10), picture=None):
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
			picture = PictureManager.MANAGER.get_picture("platform.png")
		x = 0
		y = 0
		pic_w = picture.get_width()
		pic_h = picture.get_height()
		while x < size[0]:
			while y < size[1]:
				self._surface.blit(picture, (x, y))
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

class MovingPlatform(Platform):
	""" The moving platform class.

	An instance of this class represents a moving platform of a level.

	Attributes:
		_route: The rout of this moving platform.
		_flying_type: The flying type of the moving platform.
		_forward: This optional flag, used for the LINE type, determines if the moving platform moves forward or backward in the route.
		_next_point: The index of the next point the moving platform flies to.
		_vector: The vector determining the direction of the moving platform.
	"""

	# Values for the _flying_type attributes.
	LINE, CIRCLE = range(2)

	# Speed of the flying platform.
	SPEED = 0.75

	def __init__(self, size=(10, 10), route=([0, 0], (50, 0)), flying_type=CIRCLE):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.

		Args:
			size: The size of the moving platform.
			route: The route the moving platform.
			flying_type: The flying type of the moving platform.
		"""
		Platform.__init__(self, pos=route[0][:], size=size)
		self._route = route
		self._flying_type = flying_type
		if flying_type == MovingPlatform.LINE:
			self._forward = True
		self._next_point = 1
		self._vector = (Vector2(route[1]) - Vector2(route[0])).normal()

	def tick(self):
		""" Method for handling the game ticks.

		This method should be called every tick to calculate the moving platform changes.
		"""
		vector = self._vector * MovingPlatform.SPEED

		self._pos[0] += vector.x
		self._pos[1] += vector.y
		self._rect.x = self._pos[0]
		self._rect.y = self._pos[1]

		if not self._vector == (Vector2(self._route[self._next_point]) - Vector2(self._pos)).normal():
			if self._flying_type == MovingPlatform.CIRCLE:
				next_point = (self._next_point + 1) % len(self._route)
			elif self._forward:
				next_point = self._next_point + 1
				if next_point >= len(self._route):
					self._forward = False
					next_point -= 2
			else:
				next_point = self._next_point - 1
				if next_point < 0:
					self._forward = True
					next_point += 2
			self._vector = (Vector2(self._route[next_point]) - Vector2(self._route[self._next_point])).normal()
			self._next_point = next_point