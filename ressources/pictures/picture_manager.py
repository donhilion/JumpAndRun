import pygame
import logging
from thread import start_new_thread, allocate_lock

from ressources.ressource_manager import RessourceWrapper # TODO: check import

class PictureManager(object):
	''' A manager for picture ressources.

	This manager loads pictures asynchroniously.
	'''

	def __init__(self):
		self.lock = allocate_lock()
		self.loaded = {}

	def load_picture(self, name):
		ressource_wrapper = RessourceWrapper(name = name)
		start_new_thread(self.load_picture_asynchroniously, (ressource_wrapper,))
		return ressource_wrapper

	def load_picture_asynchroniously(self, ressource_wrapper):
		try:
			logging.debug("Begin loading picture " + ressource_wrapper.name)
			self.lock.acquire()
			ressource_wrapper.data = pygame.image.load("ressources/pictures/" \
				+ ressource_wrapper.name).convert()
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
