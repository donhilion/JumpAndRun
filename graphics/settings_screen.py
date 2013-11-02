import pygame
from pygame.locals import *
from settings.settings import Settings
import window
from resources.pictures.picture_manager import PictureManager

__author__ = 'Donhilion'


class SettingsEntry(object):
	""" The settings entry class.

	An instance of this class represents a settings entry-

	Attributes:
		name: The name of the setting.
		text: The text to display.
		type: The type of the setting.
		value: The value of the setting.
	"""

	# possible value for type
	SCALE10 = range(1)

	def __init__(self, name, text, type, value):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.
		"""
		self.name = name
		self.text = text
		self.type = type
		self.value = value

	def inc(self):
		""" Increases the setting's value.

		This method increases the value of the entry.
		"""
		if self.type == SettingsEntry.SCALE10:
			if self.value < 10:
				self.value += 1

	def dec(self):
		""" Decreases the setting's value.

		This method decreases the value of the entry.
		"""
		if self.type == SettingsEntry.SCALE10:
			if self.value > 0:
				self.value -= 1


class SettingsScreen(object):
	""" The settings screen class.

	An instance of this class represents a settings screen.

	Attributes:
		_settings: The game settings.
		_entries: The settings entries.
		_screen: The screen to draw on.
		_width: The width of the window.
		_height: The height of the window.
		_window: The surrounding window.
		_bg: The background picture.
		_font: The font to use.
		_font_height: The height of the used font.
		_selected: The index of the selected settings entry.
	"""

	def __init__(self, screen, width, height, window, settings):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.
		"""
		self._settings = settings

		sound_entry = SettingsEntry(Settings.SOUND_VOLUME, "Sound", SettingsEntry.SCALE10,
									self._settings.get_value(Settings.SOUND_VOLUME))
		music_entry = SettingsEntry(Settings.MUSIC_VOLUME, "Music", SettingsEntry.SCALE10,
									self._settings.get_value(Settings.MUSIC_VOLUME))
		fx_entry = SettingsEntry(Settings.FX_VOLUME, "Effects", SettingsEntry.SCALE10,
								 self._settings.get_value(Settings.FX_VOLUME))

		self._entries = (sound_entry, music_entry, fx_entry)

		self._screen = screen
		self._width = width
		self._height = height
		self._window = window
		self._bg = PictureManager.MANAGER.get_picture("menuBackground.png")
		self._bg = pygame.transform.scale(self._bg, (width, height))
		self._font = pygame.font.SysFont("arial", 24)
		self._font_height = self._font.get_linesize()
		self._selected = 0

	def draw(self):
		""" Draws the settings.

		This method draws the settings on the screen.
		"""
		self._screen.blit(self._bg, (0, 0))
		y = 0.5 * (self._height - len(self._entries) * (self._font_height + 5))
		i = 0
		for entry in self._entries:
			if self._selected == i:
				text = self._font.render(entry.text, True, (255, 255, 0))
			else:
				text = self._font.render(entry.text, True, (150, 150, 0))
			value = self._font.render(str(entry.value), True, (150, 150, 0))

			self._screen.blit(text, (100, y))
			self._screen.blit(value, (self._width - 100 - value.get_width(), y))
			y += self._font_height + 5
			i += 1

	def key_down(self, key):
		""" Handles key down events.

		This method handles key down events.
		The pressing of the up or down key changes the selected settings entry.
		The pressing of the left or right key changes the value of the selected entry.

		Args:
			key: The key event information provided by pygame.
		"""
		if key == K_DOWN:
			if self._selected < len(self._entries) - 1:
				self._selected += 1
		elif key == K_UP:
			if self._selected > 0:
				self._selected -= 1
		elif key == K_RIGHT:
			self._entries[self._selected].inc()
		elif key == K_LEFT:
			self._entries[self._selected].dec()
		elif key == K_ESCAPE:
			# save settings
			for entry in self._entries:
				self._settings.set_value(entry.name, entry.value)
			self._window.switch(window.Window.MENU)


	def key_up(self, key):
		""" Handles key up events.

		This method handles key up events.
		These events will be ignored.

		Args:
			key: The key event information provided by pygame.
		"""
		pass
