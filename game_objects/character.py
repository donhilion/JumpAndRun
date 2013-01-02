from graphics.drawables.animated import Animated
from ressources.animations.animation_manager import AnimationManager
from ressources.pictures.picture_manager import PictureManager

__author__ = 'donhilion'

class Character(object):

	STANDING, WALKING = range(2)
	SPEED = 1

	def __init__(self, pos = [0, 0], state = STANDING, walk_animation = None, stand_animation = None):
		self._pos = pos
		self._state = state
		if walk_animation is None or stand_animation is None:
			animation_manager = AnimationManager.MANAGER
			animation = animation_manager.animations["animations.xml"]
			if walk_animation is None:
				walk_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["charMov"])
			if stand_animation is None:
				stand_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["charStill"])
		self._walk_animation = walk_animation
		self._stand_animation = stand_animation

	def draw(self, surface, tick):
		if self._state == Character.STANDING:
			self._stand_animation.draw(surface, self._pos[0], self._pos[1], tick)
		elif self._state == Character.WALKING:
			self._walk_animation.draw(surface, self._pos[0], self._pos[1], tick)

	def tick(self):
		self._state = Character.STANDING

	def move(self, dx):
		self._pos[0] += dx * Character.SPEED
		self._state = Character.WALKING