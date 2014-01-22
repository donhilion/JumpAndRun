import json
from game_objects.enemy import Enemy, FlyingEnemy
from platform import Platform, MovingPlatform

__author__ = 'Donhilion'


class Level(object):
	""" The level class.

	An instance of this class represents a level for the game.

	Attributes:
		_start: The start position for the character.
		_deadzone: The area the character dies in.
		_platforms: The platforms of this level.
		_moving_platforms: The moving platforms of this level.
		_collectables: The collectables of this level.
		_enemies: The enemies of this level.
		_goal: The goal position of this level.
	"""

	def __init__(self, json_string=None, platforms=None, moving_platforms=None, collectables=None, enemies=None, start=(0, 0),
				 deadzone=(0, 0, 0, 0), goal=(0, 0)):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.
		If the jsonString is set, it is used to set these information. Otherwise the other parameters will be used.

		Args:
			json_string: The json string containing the level information.
			platforms: A list of platforms for this level.
			collectables: A list of collectables for this level.
			enemies: A list of enemies for this level.
			start: The start position for this level.
			deadzone: The dead zone area for this level.
			goal: The goal position for this level.
		"""
		if json_string is not None:
			json_map = json.loads(json_string)
			start = json_map["start"]
			deadzone = json_map["deadzone"]
			goal = json_map["goal"]
			platforms = []
			for platform in json_map["platforms"]:
				x = platform["x"]
				y = platform["y"]
				w = platform["w"]
				h = platform["h"]
				platforms.append(Platform((x, y), (w, h)))
			if "moving_platforms" in json_map.keys():
				moving_platforms = []
				for moving_platform in json_map["moving_platforms"]:
					moving_platforms.append(MovingPlatform(size=moving_platform["size"], route=moving_platform["route"]))
			collectables = []
			for collectable in json_map["collectables"]:
				x = collectable["x"]
				y = collectable["y"]
				collectables.append((x, y))
			enemies = []
			for enemy in json_map["enemies"]:
				x = enemy["x"]
				y = enemy["y"]
				enemies.append(Enemy([x, y]))
			for enemy in json_map["flying"]:
				enemies.append(FlyingEnemy(enemy))
		if platforms is None:
			platforms = []
		if moving_platforms is None:
			moving_platforms = []
		if collectables is None:
			collectables = []
		if enemies is None:
			enemies = []
		self._start = start
		self._deadzone = deadzone
		self._platforms = platforms
		self._moving_platforms = moving_platforms
		self._collectables = collectables
		self._enemies = enemies
		self._goal = goal

	def get_platforms(self):
		""" Returns the platforms.

		This method returns the list of platforms of this level.

		Returns:
			The list of platforms.
		"""
		return self._platforms[:]

	def get_moving_platforms(self):
		""" Returns the moving platforms.

		This method returns the list of moving platforms of this level.

		Returns:
			The list of moving platforms.
		"""
		return self._moving_platforms[:]

	def get_collectables(self):
		""" Returns the collectables.

		This method returns the list of collectables of this level.

		Returns:
			The list of collectables.
		"""
		return self._collectables[:]

	def get_enemies(self):
		""" Returns the enemies.

		This method returns the list of enemies of this level.

		Returns:
			The list of enemies.
		"""
		return self._enemies[:]

	def get_start(self):
		""" Returns the start.

		This method returns the start position of this level.

		Returns:
			The start position.
		"""
		return self._start

	def get_deadzone(self):
		""" Returns the dead zone.

		This method returns the dead zone area of this level.

		Returns:
			The dead zone area.
		"""
		return self._deadzone

	def get_goal(self):
		""" Returns the goal.

		This methods returns the goal position of this level.

		Returns:
			The goal position.
		"""
		return self._goal
