import json
import logging
from thread import start_new_thread

from ressources.ressource_manager import RessourceWrapper

class SettingsManager(object):
	'''
	'''

	MANAGER = None

	def __init__(self):
		self.settings = {}
		SettingsManager.MANAGER = self


	def load_setting(self, name):
		ressource_wrapper = RessourceWrapper(name = name)
		start_new_thread(self.load_setting_asynchroniously, (ressource_wrapper,))
		return ressource_wrapper
	
	def load_setting_asynchroniously(self, wrapper):
		try:
			with open('ressources/settings/' + wrapper.name, 'r') as f:
				json_string = f.read()
			json_object = json.loads(json_string)
			self.settings[wrapper.name] = json_object
			wrapper.data = json_object
			wrapper.status = RessourceWrapper.LOADED
		except Exception as ex:
			logging.error("Error while loading picture " + wrapper.name)
			logging.error(ex)
			wrapper.status = RessourceWrapper.FAILED