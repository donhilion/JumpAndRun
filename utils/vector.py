import math

__author__ = 'Donhilion'

class Vector2(object):
	""" The vector class.

	An instance of this class represents a two dimensional vector.

	Attributes:
		x: The x part of this vector.
		y: The y part of this vector.
	"""

	def __init__(self, point=None):
		""" Generates a new instance of this class.

		This method generates a new instance of this class and sets the fields.

		Args:
			point: The point corresponding to this vector. If not set it will be set to (0,0).
		"""
		if point is None:
			point = (0,0)
		self.x = point[0]
		self.y = point[1]

	def normal(self):
		""" Normalizes this vector.

		Returns this vector normalized.

		Returns:
			This vector normalized.
		"""
		l = len(self)
		if l > 0:
			return self / l
		else:
			return self

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __neg__(self):
		return Vector2([-self.x, -self.y])

	def __add__(self, other):
		return Vector2([self.x + other.x, self.y + other.y])

	def __sub__(self, other):
		return Vector2([self.x - other.x, self.y - other.y])

	def __mul__(self, other):
		return Vector2([self.x * other, self.y * other])

	def __div__(self, other):
		return Vector2([self.x / other, self.y / other])

	def __len__(self):
		return math.sqrt(self.x**2 + self.y**2)

	def __str__(self):
		return "(" +  str(self.x) + "," + str(self.y) + ")"
