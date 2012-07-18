import pygame
from pygame.locals import *

from ressources.pictures.picture_manager import PictureManager
from ressources.ressource_manager import RessourceWrapper

class LoadingWindow(object):
	'''
	'''
	def __init__(self):
		self.screen = pygame.display.set_mode((400, 400), 0, 32)
		self.font = pygame.font.SysFont("arial", 16)
		self.font_height = self.font.get_linesize()


	def load(self):
		running = True
		infos = []
		results = []

		# TODO load settings

		infos.append("Start loading pictures")
		manager = PictureManager()
		wrapper = manager.load_picture("background.png") # TODO use list
		results.append(wrapper)

		while running:
			for event in pygame.event.get():
				if event.type == QUIT:
					exit() # TODO: check what else has to be done

			for result in results:
				if result.status == RessourceWrapper.LOADED:
					infos.append("Done loading " + result.name)
					results.remove(result)
				if result.status == RessourceWrapper.FAILED:
					infos.append("Error during loading " + result.name)
					results.remove(result)
		
			self.screen.fill((255, 255, 255))

			line = 0
			for info in infos:
				text = self.font.render(info, True, (0, 0, 0))
				self.screen.blit(text, (8, line))
				line += self.font_height

			pygame.display.update()

