__author__ = 'Donhilion'

import logging
from thread import start_new_thread, allocate_lock

from ressources.ressource_manager import RessourceWrapper
from game_objects.level import Level

class LevelManager(object):

	MANAGER  = None

	def __init__(self):
		self.lock = allocate_lock()
		self.levels = {}
		LevelManager.MANAGER = self

	def load_level(self, name):
		wrapper = RessourceWrapper(name = name)
		start_new_thread(self.load_level_asynchroniously, (wrapper,))
		return wrapper

	def load_level_asynchroniously(self, wrapper):
		try:
			logging.debug("Begin loading level " + wrapper.name)
			with open('ressources/levels/' + wrapper.name + '.json', 'r') as f:
				s = f.read()
			level = Level(jsonString=s)

			self.lock.acquire()
			self.levels[wrapper.name] = level
			self.lock.release()
			logging.debug("End loading level " + wrapper.name)
			wrapper.status = RessourceWrapper.LOADED

		except Exception as ex:
			logging.error("Error while loading level " + \
				wrapper.name)
			logging.error(ex)
			wrapper.status = RessourceWrapper.FAILED
			try:
				self.lock.release()
			except Exception as ex:
				logging.error(ex)
