import pygame
import logging
from thread import start_new_thread, allocate_lock
from resources.ressource_manager import RessourceWrapper

__author__ = 'Donhilion'


class SoundManager(object):
	""" The sound manager class.

	An instance of this class represents a sound manager.

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
		SoundManager.MANAGER = self

	def load_sound(self, name):
		""" Loads the sound.

		This method loads the sound with the given name.
		Calling this method starts a new thread which will load the sound.
		A wrapper is returned containing the progress information and when the sound is loaded the sound.

		Args:
			name: The name of the sound to load.

		Returns:
			A wrapper containing the progress information and when the sound is loaded the sound.
		"""
		resource_wrapper = RessourceWrapper(name=name)
		start_new_thread(self.load_sound_asynchronously, (resource_wrapper,))
		return resource_wrapper

	def load_sound_asynchronously(self, resource_wrapper):
		""" Loads the sound.

		This method loads the sound with the name included in the wrapper.

		Args:
			wrapper: The wrapper containing the name of the sound. The result will be stored in this wrapper.
		"""
		try:
			logging.debug("Begin loading sound " + resource_wrapper.name)
			self._lock.acquire()
			resource_wrapper.data = pygame.mixer.Sound("resources/sounds/" \
													   + resource_wrapper.name)
			self._loaded[resource_wrapper.name] = resource_wrapper.data
			self._lock.release()
			logging.debug("End loading sound " + resource_wrapper.name)
			resource_wrapper.status = RessourceWrapper.LOADED
		except Exception as ex:
			self._lock.release()
			logging.error("Error while loading sound " + \
						  resource_wrapper.name)
			logging.error(ex)
			resource_wrapper.status = RessourceWrapper.FAILED

	def get_sound(self, name):
		""" Returns the sound.

		This method returns the sound with the given name.
		If no sound with this name was loaded, None is returned.

		Args:
			name: The name of the sound to return.

		Returns:
			The sound with the given name or None if this setting was not loaded.
		"""
		if name in self._loaded.keys():
			return self._loaded[name]
		return None
