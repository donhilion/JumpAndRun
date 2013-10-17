import logging
from thread import start_new_thread, allocate_lock

from resources.ressource_manager import RessourceWrapper
from game_objects.level import Level

__author__ = 'Donhilion'


class LevelManager(object):
	""" The level manager class.

	An instance of this class represents a level manager.

	Attributes:
		_lock: A lock for controlling asynchronous access.
		_levels: A dictionary containing every loaded level.
	"""

	# An instance of this class.
	MANAGER = None

	def __init__(self):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.
		"""
		self._lock = allocate_lock()
		self._levels = {}
		LevelManager.MANAGER = self

	def load_level(self, name):
		""" Loads the level.

		This method loads the level with the given name.
		Calling this method starts a new thread which will load the level.
		A wrapper is returned containing the progress information and when the level is loaded the level.

		Args:
			name: The name of the level to load.

		Returns:
			A wrapper containing the progress information and when the level is loaded the level.
		"""
		wrapper = RessourceWrapper(name=name)
		start_new_thread(self.load_level_asynchronously, (wrapper,))
		return wrapper

	def load_level_asynchronously(self, wrapper):
		""" Loads the level.

		This method loads the level with the name included in the wrapper.

		Args:
			wrapper: The wrapper containing the name of the level. The result will be stored in this wrapper.
		"""
		try:
			logging.debug("Begin loading level " + wrapper.name)
			with open('resources/levels/' + wrapper.name + '.json', 'r') as f:
				s = f.read()
			level = Level(json_string=s)

			self._lock.acquire()
			self._levels[wrapper.name] = level
			self._lock.release()
			logging.debug("End loading level " + wrapper.name)
			wrapper.status = RessourceWrapper.LOADED

		except Exception as ex:
			logging.error("Error while loading level " + \
						  wrapper.name)
			logging.error(ex)
			wrapper.status = RessourceWrapper.FAILED
			try:
				self._lock.release()
			except Exception as ex:
				logging.error(ex)

	def get_level(self, name):
		""" Returns the animation.

		This method returns the animation with the given name.
		If no animation with this name was loaded, None is returned.

		Args:
			name: The name of the animation to return.

		Returns:
			The animation with the given name or None if this animation was not loaded.
		"""
		if name in self._levels.keys():
			return self._levels[name]
		return None
