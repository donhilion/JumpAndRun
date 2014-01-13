__author__ = 'Donhilion'


class Settings(object):
	""" The settings class.

	This class contains the current settings of the game.

	Attributes:
		_settings: A dictionary containing every setting.
	"""

	# The overall volume
	SOUND_VOLUME = "SOUND_VOLUME"
	# The volume of the music
	MUSIC_VOLUME = "MUSIC_VOLUME"
	# The volume of the sound effects
	FX_VOLUME = "FX_VOLUME"
	# Determines if the joystick is enabled
	JOYSTICK = "JOYSTICK"

	def __init__(self):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.
		The available settings will be preset with standard values.
		"""
		self._settings = {Settings.SOUND_VOLUME: 5, Settings.MUSIC_VOLUME: 5, Settings.FX_VOLUME: 10, Settings.JOYSTICK: True}

	def get_value(self, key):
		""" Returns the settings value.

		This method returns the value of the setting with the given name.

		Args:
			key: The name of the setting.

		Returns:
			The value of the setting.
		"""
		if key in self._settings.keys():
			return self._settings[key]
		return None

	def set_value(self, key, value):
		""" Set the setting's value.

		This method sets the value of the given setting.

		Args:
			key: The name of the setting.
			value: The new value of the setting.
		"""
		self._settings[key] = value
