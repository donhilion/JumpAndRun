import logging

__author__ = 'Donhilion'


class Drawable(object):
	""" Abstract class for drawable objects.

	This class defines all methods a drawable object must implement.

	Attributes:
		environment: The environment this drawable belongs to.
	"""

	def __init__(self, environment=None):
		""" Generates a new instance of this class.
		
		Generates a new instance of this class and sets the field information.
		
		Args:
			environment: The environment of this drawable.
		"""
		self.environment = environment

	def draw(self):
		""" Draws this object.

		This method has to be implemented.
		"""
		logging.warn("Not implemented draw")


class Drawable2D(Drawable):
	""" Abstract class for 2D objects.

	This class provides some handy functions for drawable 2D objects.

	Attributes:
		x: The x coordinate of the left side of the object. This is a number.
		y: The y coordinate of the bottom side of the object. This is a number.
		width: The width of the object. This is a number.
		height: The height of the object.  This is a number.
	"""

	def __init__(self, environment=None, x=0, y=0, width=0, height=0):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.

		Args:
			environment: The environment of this drawable.
			x: The x coordinate of this drawable.
			y: The y coordinate of this drawable.
			width: The width of this drawable.
			height: The height of this drawable.
		"""
		super(Drawable2D, self).__init__(environment)
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def is_visible(self):
		""" Checks if the object is visible.

		Checks if the object is inside the area the camera sees.

		Returns:
			True if the object is visible, False otherwise.
		"""
		if self.environment is None:
			logging.warn("No environment")
			return
		camera = self.environment.camera
		return self.x < (camera.x + camera.width) and \
			   (self.x + self.width) > camera.x and \
			   self.y < (camera.y + camera.height) and \
			   (self.y + self.height) > camera.y

	def draw(self):
		""" Draws this object if it is visible.

		Checks if this object is visible and if so, draws it.
		"""
		if self.is_visible():
			self.draw2D()

	def draw2D(self):
		""" Draws this object.

		This method has to be implemented.
		"""
		logging.warn("Not implemented draw2D")
		
