import json
import logging
from thread import start_new_thread, allocate_lock

from resources.ressource_manager import RessourceWrapper

__author__ = 'Donhilion'


class AnimationManager(object):
	""" The animation manager class.

	An instance of this class represents an animation manager.

	Attributes:
		_lock: A lock for controlling asynchronous access.
		_animation: A dictionary containing every loaded animation.
	"""

	# An instance of this class.
	MANAGER = None

	def __init__(self):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.
		"""
		self._lock = allocate_lock()
		self._animations = {}
		AnimationManager.MANAGER = self

	def load_animation(self, name):
		""" Loads the animation.

		This method loads the animation with the given name.
		Calling this method starts a new thread which will load the animation.
		A wrapper is returned containing the progress information and when the animation is loaded the animation.

		Args:
			name: The name of the animation to load.

		Returns:
			A wrapper containing the progress information and when the animation is loaded the animation.
		"""
		wrapper = RessourceWrapper(name=name)
		start_new_thread(self.load_animation_asynchronously, (wrapper,))
		return wrapper

	def load_animation_asynchronously(self, wrapper):
		""" Loads the animation.

		This method loads the animation with the name included in the wrapper.

		Args:
			wrapper: The wrapper containing the name of the animation. The result will be stored in this wrapper.
		"""
		try:
			logging.debug("Begin loading animation " + wrapper.name)
			with open('resources/animations/' + wrapper.name + ".json", 'r') as f:
				json_string = f.read()
			json_object = json.loads(json_string)
			frames = json_object["frames"]
			animations = json_object["animations"]

			self._lock.acquire()
			self._animations[wrapper.name] = (frames, animations)
			self._lock.release()
			logging.debug("End loading picture " + wrapper.name)
			wrapper.status = RessourceWrapper.LOADED
		except Exception as ex:
			logging.error("Error while loading animation " + \
						  wrapper.name)
			logging.error(ex)
			wrapper.status = RessourceWrapper.FAILED
			try:
				self._lock.release()
			except Exception as ex:
				logging.error(ex)

	def get_animation(self, name):
		""" Returns the animation.

		This method returns the animation with the given name.
		If no animation with this name was loaded, None is returned.

		Args:
			name: The name of the animation to return.

		Returns:
			The animation with the given name or None if this animation was not loaded.
		"""
		if name in self._animations.keys():
			return self._animations[name]
		return None