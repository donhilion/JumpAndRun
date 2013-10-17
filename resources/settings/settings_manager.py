import json
import logging
from thread import start_new_thread, allocate_lock

from resources.ressource_manager import RessourceWrapper

__author__ = 'Donhilion'


class SettingsManager(object):
	""" The settings manager class.

	An instance of this class represents a settings manager.

	Attributes:
		_lock: A lock for controlling asynchronous access.
		_settings: A dictionary containing every loaded setting.
	"""

	# An instance of this class.
	MANAGER = None

	def __init__(self):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.
		"""
		self._lock = allocate_lock()
		self._settings = {}
		SettingsManager.MANAGER = self


	def load_setting(self, name):
		""" Loads the setting.

		This method loads the setting with the given name.
		Calling this method starts a new thread which will load the setting.
		A wrapper is returned containing the progress information and when the setting is loaded the setting.

		Args:
			name: The name of the setting to load.

		Returns:
			A wrapper containing the progress information and when the setting is loaded the setting.
		"""
		resource_wrapper = RessourceWrapper(name=name)
		start_new_thread(self.load_setting_asynchronously, (resource_wrapper,))
		return resource_wrapper

	def load_setting_asynchronously(self, wrapper):
		""" Loads the setting.

		This method loads the setting with the name included in the wrapper.

		Args:
			wrapper: The wrapper containing the name of the setting. The result will be stored in this wrapper.
		"""
		try:
			with open('resources/settings/' + wrapper.name, 'r') as f:
				json_string = f.read()
			json_object = json.loads(json_string)
			self._lock.acquire()
			self._settings[wrapper.name] = json_object
			self._lock.release()
			wrapper.data = json_object
			wrapper.status = RessourceWrapper.LOADED
		except Exception as ex:
			logging.error("Error while loading picture " + wrapper.name)
			logging.error(ex)
			wrapper.status = RessourceWrapper.FAILED

	def get_setting(self, name):
		""" Returns the setting.

		This method returns the setting with the given name.
		If no setting with this name was loaded, None is returned.

		Args:
			name: The name of the setting to return.

		Returns:
			The setting with the given name or None if this setting was not loaded.
		"""
		if name in self._settings.keys():
			return self._settings[name]
		return None