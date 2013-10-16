import pygame
from pygame.locals import *
from resources.levels.level_manager import LevelManager

from resources.pictures.picture_manager import PictureManager
from resources.settings.settings_manager import SettingsManager
from resources.animations.animation_manager import AnimationManager
from resources.ressource_manager import RessourceWrapper
from resources.sounds.sound_manager import SoundManager

__author__ = 'Donhilion'


class LoadingWindow(object):
	""" The loading window class.

	An object of this class represents a loading window.
	This window will load files and shows the progress of this loading.

	Attributes:
		_screen: The screen surface to draw on.
		_font: The font used for displaying the information.
		_font_height: The height of the font.
	"""

	# Name of the file containing the picture information.
	PICTURES_FILE = "pictures.json"
	# Name of the file containing the sound information.
	SOUNDS_FILE = "sounds.json"
	# List of setting files to load.
	SETTINGS_FILES = ("graphics.json", PICTURES_FILE, SOUNDS_FILE)
	# List of animation files to load.
	ANIMATIONS_FILES = ("animations",)
	# List of level files to load.
	LEVELS_FILES = ("level0",)
	# String used for indentation.
	INDENT = "    "
	# The dimensions of the window.
	SIZE = (WIDTH, HEIGHT) = (400, 400)

	def __init__(self):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.
		"""
		self._screen = pygame.display.set_mode(LoadingWindow.SIZE, 0, 32)
		self._font = pygame.font.SysFont("arial", 16)
		self._font_height = self._font.get_linesize()

	@staticmethod
	def load_pictures(pictures, info, results):
		""" Loads the pictures.

		This method loads the pictures using the picture manager.

		Args:
			pictures: The list of picture file names to load.
			info: The showed list of information.
			results: The list of result elements.
		"""
		info.append("Start loading pictures")
		manager = PictureManager()
		for name in pictures:
			info.append(LoadingWindow.INDENT + "Start loading " + \
						name["value"])
			results.append(manager.load_picture(name["value"]))

	@staticmethod
	def load_sounds(sounds, info, results):
		""" Loads the sounds.

		This method loads the sounds using the sound manager.

		Args:
			sounds: The list of sound file names to load.
			info: The showed list of information.
			results: The list of result elements.
		"""
		info.append("Start loading sounds")
		manager = SoundManager()
		for name in sounds:
			info.append(LoadingWindow.INDENT + "Start loading " + \
						name)
			results.append(manager.load_sound(name))


	def load(self):
		""" Loads the files.

		This method loads the setting and resource files and shows the progress on the screen.
		"""
		running = True
		infos = []
		results = []
		level_loaded = False

		infos.append("Start loading graphics settings")
		settings_manager = SettingsManager()
		for file_name in LoadingWindow.SETTINGS_FILES:
			infos.append(LoadingWindow.INDENT + "Start loading " + file_name)
			results.append(settings_manager.load_setting(file_name))

		infos.append("Start loading animations")
		animation_manager = AnimationManager()
		for file_name in LoadingWindow.ANIMATIONS_FILES:
			infos.append(LoadingWindow.INDENT + "Start loading " + file_name)
			results.append(animation_manager.load_animation(file_name))

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
					if result.name == LoadingWindow.SOUNDS_FILE:
						self.load_sounds(result.data, infos, results)
				if result.status == RessourceWrapper.FAILED:
					infos.append("Error during loading " + result.name)
					results.remove(result)

			self._screen.fill((0, 0, 0))

			line = LoadingWindow.HEIGHT - len(infos) * self._font_height
			for info in infos:
				text = self._font.render(info, True, (0, 255, 0))
				self._screen.blit(text, (8, line))
				line += self._font_height

			pygame.display.update()

			if len(results) == 0:
				if level_loaded:
					running = False
				else:
					infos.append("Start loading levels")
					level_manager = LevelManager()
					for file_name in LoadingWindow.LEVELS_FILES:
						infos.append(LoadingWindow.INDENT + "Start loading " + file_name)
						results.append(level_manager.load_level(file_name))
					level_loaded = True
