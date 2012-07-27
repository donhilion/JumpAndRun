import pygame
from pygame.locals import *

from ressources.pictures.picture_manager import PictureManager
from ressources.settings.settings_manager import SettingsManager
from ressources.animations.animation_manager import AnimationManager
from ressources.ressource_manager import RessourceWrapper

class LoadingWindow(object):
	'''
	'''

	PICTURES_FILE = "pictures.xml"
	SETTINGS_FILES = ("graphics.xml", PICTURES_FILE)
	ANIMATIONS_FILES = ("animations.xml",)

	INTEND = "    "

	SIZE = (WIDTH, HEIGHT) = (400, 400)

	def __init__(self):
		self.screen = pygame.display.set_mode(LoadingWindow.SIZE, 0, 32)
		self.font = pygame.font.SysFont("arial", 16)
		self.font_height = self.font.get_linesize()

	def load_pictures(self, pictures, infos, results):
		infos.append("Start loading pictures")
		manager = PictureManager()
		for key in pictures:
			for name in pictures[key]:
				infos.append(LoadingWindow.INTEND + "Start loading " + \
					pictures[key][name])
				results.append(manager.load_picture(pictures[key][name]))


	def load(self):
		running = True
		infos = []
		results = []
		ok = True

		infos.append("Start loading graphics settings")
		self.settings_manager = SettingsManager()
		for file_name in LoadingWindow.SETTINGS_FILES:
			infos.append(LoadingWindow.INTEND + "Start loading " + file_name)
			results.append(self.settings_manager.load_setting(file_name))

		infos.append("Star loading animations")
		self.animation_manager = AnimationManager()
		for file_name in LoadingWindow.ANIMATIONS_FILES:
			infos.append(LoadingWindow.INTEND + "Start loading " + file_name)
			results.append(self.animation_manager.load_animation(file_name))

		while running:
			for event in pygame.event.get():
				if event.type == QUIT:
					exit() # TODO: check what else has to be done

			for result in results:
				if result.status == RessourceWrapper.LOADED:
					infos.append("Done loading " + result.name)
					results.remove(result)
					# load images
					if result.name == LoadingWindow.PICTURES_FILE:
						self.load_pictures(result.data, infos, results)
				if result.status == RessourceWrapper.FAILED:
					ok = False
					infos.append("Error during loading " + result.name)
					results.remove(result)
		
			self.screen.fill((0, 0, 0))

			line = LoadingWindow.HEIGHT - len(infos) * self.font_height
			for info in infos:
				text = self.font.render(info, True, (0, 255, 0))
				self.screen.blit(text, (8, line))
				line += self.font_height

			pygame.display.update()

			if len(results) == 0:
				running = False
