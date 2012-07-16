'''
Created on 10.07.2012

@author: Donhilion
'''

class Camera(object):
	''' The camera.

	This class contains informations about the view of a camera.

	Attributes:
		x: The x coordinate of the camera. This is a number.
		y: The y coordinate of the camera. This is a number.
		width: The width of the camera. This is a number.
		height: The height of the camera. This is a number.
	'''
	
	def __init__(self, x=0, y=0, width=0, height=0):
		self.x = x
		self.y = y
		self.width = width
		self.height = height