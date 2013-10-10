from camera import Camera

__author__ = 'Donhilion'


class GraphicsEnvironment(object):
	""" The graphics environment.

	This class contains information about the current graphics environment.

	Attributes:
		camera: The current camera of the environment. This is a Camera.
	"""

	def __init__(self, camera=None):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.

		Args:
			camera: The camera of this environment.
		"""
		if camera is None:
			camera = Camera()
		self.camera = camera
