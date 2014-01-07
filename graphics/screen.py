__author__ = 'Donhilion'

class Screen(object):
	""" The screen class.

	This class provides an interface for screen which could be displayed in the Window class.
	"""

	def __init__(self):
		""" Generates a new instance of this class.

		Generates a new instance of this class.
		"""
		pass

	def draw(self):
		""" Draws the screen.

		This method is a stub for drawing on the screen.
		"""
		pass

	def key_down(self, key):
		""" Handles key down events.

		This method is a stub for handling key down events.

		Args:
			key: The key event information provided by pygame.
		"""
		pass

	def key_up(self, key):
		""" Handles key up events.

		This method is a stub for handling key up events.

		Args:
			key: The key event information provided by pygame.
		"""
		pass

	def mouse_click(self, pos, button):
		""" Handles mouse click events.

		This method is a stub for handling mouse click events.

		Args:
			pos: The position of the mouse.
			button: The button pressed.
		"""
		pass

	def mouse_move(self, pos):
		""" Handles mouse move events.

		This method is a stub for handling mouse movement events.

		Args:
			pos: The position of the mouse.
		"""
		pass
