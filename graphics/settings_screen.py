import math
import pygame
from pygame.locals import *
from pygame.surface import Surface
from graphics.screen import Screen
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
		minus: The rectangle for decreasing the value.
		plus: The rectangle for increasing the value.
		action: The action to perform.
	"""

	# possible value for type
	SCALE10, ACTION, BOOL = range(3)

	def __init__(self, name, text, type, value, button_size=0, action=None):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.

		Args:
			name: The name of the setting.
			text: The text to display.
			type: The type of the setting.
			value: The value of the setting.
			button_size: The size of the buttons. The value is used for the rectangles.
			action: The action to perform.
		"""
		self.name = name
		self.text = text
		self.type = type
		self.value = value
		self.minus = Rect(0, 0, button_size, button_size)
		self.plus = Rect(0, 0, button_size, button_size)
		self.action = action

	def inc(self):
		""" Increases the setting's value.

		This method increases the value of the entry.
		"""
		if self.type == SettingsEntry.SCALE10:
			if self.value < 10:
				self.value += 1
		elif self.type == SettingsEntry.BOOL:
			self.value = not self.value

	def dec(self):
		""" Decreases the setting's value.

		This method decreases the value of the entry.
		"""
		if self.type == SettingsEntry.SCALE10:
			if self.value > 0:
				self.value -= 1
		elif self.type == SettingsEntry.BOOL:
			self.inc()

	def act(self):
		""" Performs the action.

		This method performs the defined action.
		"""
		if self.type == SettingsEntry.ACTION and self.action is not None:
			self.action()
		elif self.type == SettingsEntry.BOOL:
			self.inc()


class SettingsScreen(Screen):
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
		_first_y: The y coordinate of the first entry.
		_delta_y: The difference in the y axis between the entries.
		_plus_button: The pre-rendered plus button.
		_minus_button: The pre-rendered minus button.
	"""
	# color of an entry
	SELECTED_COLOR = (255, 255, 0)
	# color of the selected entry
	COLOR = (150, 150, 0)

	def __init__(self, screen, width, height, window, settings):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.

		Args:
			screen: The screen to draw on.
			width: The width of the screen.
			height: The height of the screen.
			window: The surrounding window.
			settings: The game settings.
		"""
		self._settings = settings

		self._screen = screen
		self._width = width
		self._height = height
		self._window = window
		self._bg = PictureManager.MANAGER.get_picture("menuBackground.png")
		self._bg = pygame.transform.scale(self._bg, (width, height))
		self._font = pygame.font.SysFont("arial", 24)
		self._font_height = self._font.get_linesize()
		self._selected = 0

		sound_entry = SettingsEntry(Settings.SOUND_VOLUME, "Sound", SettingsEntry.SCALE10,
									self._settings.get_value(Settings.SOUND_VOLUME), button_size=self._font_height)
		music_entry = SettingsEntry(Settings.MUSIC_VOLUME, "Music", SettingsEntry.SCALE10,
									self._settings.get_value(Settings.MUSIC_VOLUME), button_size=self._font_height)
		fx_entry = SettingsEntry(Settings.FX_VOLUME, "Effects", SettingsEntry.SCALE10,
								 self._settings.get_value(Settings.FX_VOLUME), button_size=self._font_height)
		joystick_entry = SettingsEntry(Settings.JOYSTICK, "Controller", SettingsEntry.BOOL,
								 self._settings.get_value(Settings.JOYSTICK), button_size=self._font_height)
		back_entry = SettingsEntry(None, "back", SettingsEntry.ACTION,
								 None, action=self.back)

		self._entries = (sound_entry, music_entry, fx_entry, joystick_entry, back_entry)

		self._first_y = 0.5 * (self._height - len(self._entries) * (self._font_height + 5))
		self._delta_y = self._font_height + 5

		self._plus_button = None
		self._minus_button = None

		self._unchecked_bool = None
		self._checked_bool = None

		self._prepare_buttons()

	def _prepare_buttons(self):
		""" Prepares the buttons.

		This method pre-renders the plus and minus buttons.
		"""
		# draw plus button
		self._plus_button = Surface((self._font_height, self._font_height), pygame.SRCALPHA, 32)
		self._plus_button.convert_alpha()
		pygame.draw.rect(self._plus_button, SettingsScreen.COLOR, Rect(0, self._font_height/3, self._font_height, self._font_height/3))
		pygame.draw.rect(self._plus_button, SettingsScreen.COLOR, Rect(self._font_height/3, 0, self._font_height/3, self._font_height))

		# draw minus button
		self._minus_button = Surface((self._font_height, self._font_height), pygame.SRCALPHA, 32)
		self._minus_button.convert_alpha()
		pygame.draw.rect(self._minus_button, SettingsScreen.COLOR, Rect(0, self._font_height/3, self._font_height, self._font_height/3))

		# draw unchecked bool button
		self._unchecked_bool = Surface((self._font_height, self._font_height), pygame.SRCALPHA, 32)
		self._unchecked_bool.convert_alpha()
		pygame.draw.rect(self._unchecked_bool, SettingsScreen.COLOR, Rect(0, 0, self._font_height, self._font_height), 3)

		# draw checked bool button
		self._checked_bool = Surface((self._font_height, self._font_height), pygame.SRCALPHA, 32)
		self._checked_bool.convert_alpha()
		pygame.draw.rect(self._checked_bool, SettingsScreen.COLOR, Rect(0, 0, self._font_height, self._font_height), 3)
		pygame.draw.line(self._checked_bool, SettingsScreen.COLOR, (0, 0), (self._font_height, self._font_height), 3)
		pygame.draw.line(self._checked_bool, SettingsScreen.COLOR, (0, self._font_height), (self._font_height, 0), 3)

	def draw(self):
		""" Draws the settings.

		This method draws the settings on the screen.
		"""
		self._screen.blit(self._bg, (0, 0))
		y = self._first_y
		i = 0
		for entry in self._entries:
			if self._selected == i:
				text = self._font.render(entry.text, True, SettingsScreen.SELECTED_COLOR)
			else:
				text = self._font.render(entry.text, True, SettingsScreen.COLOR)
			self._screen.blit(text, (100, y))

			if entry.type == SettingsEntry.SCALE10:
				value = self._font.render(str(entry.value), True, SettingsScreen.COLOR)
				self._screen.blit(value, (self._width - 100 - value.get_width(), y))

				entry.plus.topleft = (self._width - 95, y)
				self._screen.blit(self._plus_button, entry.plus.topleft)
				entry.minus.topleft = (self._width - 105 - value.get_width() - self._font_height, y)
				self._screen.blit(self._minus_button, entry.minus.topleft)
			elif entry.type == SettingsEntry.BOOL:
				entry.plus.topleft = (self._width - 100 - self._font_height, y)
				if entry.value:
					self._screen.blit(self._checked_bool, entry.plus.topleft)
				else:
					self._screen.blit(self._unchecked_bool, entry.plus.topleft)
			y += self._delta_y
			i += 1

	def back(self):
		""" Returns to the main menu.

		This method saves the settings and return to the main menu.
		"""
		for entry in self._entries:
			if entry.name is not None:
				self._settings.set_value(entry.name, entry.value)
		self._window.switch(window.Window.MENU)

	def key_down(self, key):
		""" Handles key down events.

		This method handles key down events.
		The pressing of the up or down key changes the selected settings entry.
		The pressing of the left or right key changes the value of the selected entry.
		The pressing of the return key performs the action of the entry.
		The pressing of the escape key returns to the main menu.

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
			self.back()
		elif key == K_RETURN or key == K_SPACE:
			self._entries[self._selected].act()

	def mouse_click(self, pos, button):
		""" Handles mouse click events.

		This method is handles mouse click events.

		Args:
			pos: The position of the mouse.
			button: The button pressed.
		"""
		if button == 1:
			entry = self._entries[self._selected]
			if entry.plus.collidepoint(pos):
				entry.inc()
			elif entry.minus.collidepoint(pos):
				entry.dec()
			else:
				entry.act()

	def mouse_move(self, pos):
		""" Handles mouse move events.

		This method handles mouse movement events.

		Args:
			pos: The position of the mouse.
		"""
		if pos[1] < self._first_y:
			self._selected = 0
		else:
			dy = math.trunc((pos[1] - self._first_y) / self._delta_y)
			if dy >= len(self._entries):
				dy = len(self._entries)-1
			self._selected = dy