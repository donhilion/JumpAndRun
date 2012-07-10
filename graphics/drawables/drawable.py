'''
Created on 10.07.2012

@author: Donhilion
'''

class Drawable(object):
	''' Interface for drawable objects.

	This Interface defines all methods a drawable object must implement.
	'''
	def __init__(self):
		pass

	def draw(self):
		''' Draws this object.

		This method has to be implemented.
		'''
		# TODO: use logger
		print("Not implemented draw")

class Drawable2D(object):
	''' Abstract class for 2D objects.

	This class provides some handy functions for drawable 2D objects.

	Attributes:
		x: The x coordinate of the left side of the object. This is a number.
		x: The y coordinate of the bottom side of the object. This is a number.
		width: The width of the object. This is a number.
		height: The height of the object.  This is a number.
	'''
	def __init__(self, x=0, y=0, width=0, height=0):
		# TODO: check input
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def is_visible(self):
		''' Checks if the object is visible.

		Checks if the object is inside the area the camera sees.

		Returns: True if the object is visible, False otherwise.
		'''
		# TODO: get camera position
		# temp {
		camX = 0
		camY = 0
		camWidth = 500
		camHeight = 500
		# }
		return self.x < (camX + camWidth) and \
				(self.x + self.width) > camX and \
				self.y < (camY + camHeight) and \
				(self.y + self.height) > camY

	def draw(self):
		''' Draws this object if it is visible.

		Checks if this object is visible and if so, draws it.
		'''
		if self.is_visible():
			self.draw2D()

	def draw2D(self):
		''' Draws this object.

		This method has to be implemented.
		'''
		# TODO: use logger
		print("Not implemented draw2D")
