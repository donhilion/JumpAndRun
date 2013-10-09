__author__ = 'Donhilion'


class Camera(object):
	""" The camera.

	This class contains information about the view of a camera.

	Attributes:
		x: The x coordinate of the camera. This is a number.
		y: The y coordinate of the camera. This is a number.
		width: The width of the camera. This is a number.
		height: The height of the camera. This is a number.
	"""

	def __init__(self, x=0, y=0, width=0, height=0):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.

		Args:
			x: The x coordinate of the camera.
			y: The y coordinate of the camera.
			width: The width of the camera.
			height: The height of the camera.
		"""
		self.x = x
		self.y = y
		self.width = width
		self.height = height