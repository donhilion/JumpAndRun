import pygame
import logging
from thread import start_new_thread, allocate_lock
from ressources.ressource_manager import RessourceWrapper

__author__ = 'Donhilion'

class SoundManager(object):
	''' A manager for sound ressources.

	This manager loads sounds asynchroniously.
	'''

	MANAGER = None

	def __init__(self):
		self.lock = allocate_lock()
		self.loaded = {}
		SoundManager.MANAGER = self

	def load_sound(self, name):
		ressource_wrapper = RessourceWrapper(name = name)
		start_new_thread(self.load_sound_asynchroniously, (ressource_wrapper,))
		return ressource_wrapper

	def load_sound_asynchroniously(self, ressource_wrapper):
		try:
			logging.debug("Begin loading sound " + ressource_wrapper.name)
			self.lock.acquire()
			ressource_wrapper.data = pygame.mixer.Sound("ressources/sounds/" \
				+ ressource_wrapper.name)
			self.loaded[ressource_wrapper.name] = ressource_wrapper.data
			self.lock.release()
			logging.debug("End loading sound " + ressource_wrapper.name)
			ressource_wrapper.status = RessourceWrapper.LOADED
		except Exception as ex:
			self.lock.release()
			logging.error("Error while loading sound " + \
				ressource_wrapper.name)
			logging.error(ex)
			ressource_wrapper.status = RessourceWrapper.FAILED

