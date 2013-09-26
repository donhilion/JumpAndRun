import json
from platform import Platform
from collectable import Collectable

__author__ = 'Donhilion'

class Level(object):

	def __init__(self, jsonString=None, platforms=None, collectables=None, start = (0,0), deadzone = (0,0,0,0), goal=(0,0)):
		if jsonString is not None:
			jsonMap = json.loads(jsonString)
			start = jsonMap["start"]
			deadzone = jsonMap["deadzone"]
			goal = jsonMap["goal"]
			platforms = []
			for platform in jsonMap["platforms"]:
				x = platform["x"]
				y = platform["y"]
				w = platform["w"]
				h = platform["h"]
				platforms.append(Platform((x,y), (w,h)))
			collectables = []
			for collectable in jsonMap["collectables"]:
				x = collectable["x"]
				y = collectable["y"]
				collectables.append(Collectable((x,y), (10,10)))
		if platforms is None:
			platforms = []
		if collectables is None:
			collectables = []
		self._start = start
		self._deadzone = deadzone
		self._platforms = platforms
		self._collectables = collectables
		self._goal = goal

	def get_platforms(self):
		return self._platforms

	def get_collectables(self):
		return self._collectables

	def get_start(self):
		return self._start

	def get_deadzone(self):
		return self._deadzone

	def get_goal(self):
		return self._goal
