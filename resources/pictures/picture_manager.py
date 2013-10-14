import pygame
import logging
from thread import start_new_thread, allocate_lock

from resources.ressource_manager import RessourceWrapper

class PictureManager(object):
	''' A manager for picture resources.

	This manager loads pictures asynchroniously.
	'''

	MANAGER = None

	def __init__(self):
		self.lock = allocate_lock()
		self.loaded = {}
		PictureManager.MANAGER = self

	def load_picture(self, name):
		ressource_wrapper = RessourceWrapper(name = name)
		start_new_thread(self.load_picture_asynchroniously, (ressource_wrapper,))
		return ressource_wrapper

	def load_picture_asynchroniously(self, ressource_wrapper):
		try:
			logging.debug("Begin loading picture " + ressource_wrapper.name)
			self.lock.acquire()
			ressource_wrapper.data = pygame.image.load("resources/pictures/" \
				+ ressource_wrapper.name).convert_alpha()
			self.loaded[ressource_wrapper.name] = ressource_wrapper.data
			self.lock.release()
			logging.debug("End loading picture " + ressource_wrapper.name)
			ressource_wrapper.status = RessourceWrapper.LOADED
		except Exception as ex: 
			self.lock.release()
			logging.error("Error while loading picture " + \
				ressource_wrapper.name)
			logging.error(ex)
			ressource_wrapper.status = RessourceWrapper.FAILED
