import pygame
import logging
from thread import start_new_thread, allocate_lock

from resources.resource_manager import ResourceWrapper

__author__ = 'Donhilion'

class PictureManager(object):
	""" The picture manager class.

	An instance of this class represents a picture manager.
	This manager loads pictures asynchronously.

	Attributes:
		_lock: A lock for controlling asynchronous access.
		_loaded: A dictionary containing every loaded picture.
	"""

	# An instance of this class.
	MANAGER = None

	def __init__(self):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.
		"""
		self._lock = allocate_lock()
		self._loaded = {}
		PictureManager.MANAGER = self

	def load_picture(self, name):
		""" Loads the picture.

		This method loads the picture with the given name.
		Calling this method starts a new thread which will load the picture.
		A wrapper is returned containing the progress information and when the picture is loaded the picture.

		Args:
			name: The name of the picture to load.

		Returns:
			A wrapper containing the progress information and when the picture is loaded the picture.
		"""
		resource_wrapper = ResourceWrapper(name = name)
		start_new_thread(self.load_picture_asynchronously, (resource_wrapper,))
		return resource_wrapper

	def load_picture_asynchronously(self, resource_wrapper):
		""" Loads the picture.

		This method loads the picture with the name included in the wrapper.

		Args:
			wrapper: The wrapper containing the name of the picture. The result will be stored in this wrapper.
		"""
		try:
			logging.debug("Begin loading picture " + resource_wrapper.name)
			self._lock.acquire()
			resource_wrapper.data = pygame.image.load("resources/pictures/" \
				+ resource_wrapper.name).convert_alpha()
			self._loaded[resource_wrapper.name] = resource_wrapper.data
			self._lock.release()
			logging.debug("End loading picture " + resource_wrapper.name)
			resource_wrapper.status = ResourceWrapper.LOADED
		except Exception as ex: 
			self._lock.release()
			logging.error("Error while loading picture " + \
				resource_wrapper.name)
			logging.error(ex)
			resource_wrapper.status = ResourceWrapper.FAILED

	def get_picture(self, name):
		""" Returns the picture.

		This method returns the picture with the given name.
		If no picture with this name was loaded, None is returned.

		Args:
			name: The name of the picture to return.

		Returns:
			The picture with the given name or None if this picture was not loaded.
		"""
		if name in self._loaded.keys():
			return self._loaded[name]
		return None
