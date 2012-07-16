'''
Created on 10.07.2012

@author: Donhilion
'''

from camera import Camera

class GraphicsEnvironment(object):
	''' The graphics environment.

	This class contains informations about the current graphics environment.

	Attributes:
		camera: The current camera of the environment. This is a Camera.
	'''
	
	def __init__(self, camera=None):
		if camera == None:
			camera = Camera()
		self.camera = camera
