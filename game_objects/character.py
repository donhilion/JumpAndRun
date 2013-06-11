from graphics.drawables.animated import Animated
from ressources.animations.animation_manager import AnimationManager
from ressources.pictures.picture_manager import PictureManager
from pygame import Rect
import pygame

__author__ = 'donhilion'

class Character(object):

	STANDING, WALKING = range(2)
	SPEED = 1
	DEBUG = True
	MAX_FALLING = 2
	V_FALLING = 0.1

	def __init__(self, pos = [0, 0], state = STANDING, walk_animation = None, stand_animation = None):
		self._state = state
		self._is_falling = False
		self._dy = 0
		if walk_animation is None or stand_animation is None:
			animation_manager = AnimationManager.MANAGER
			animation = animation_manager.animations["animations.xml"]
			if walk_animation is None:
				walk_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["charMov"])
			if stand_animation is None:
				stand_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["charStill"])
		self._walk_animation = walk_animation
		self._stand_animation = stand_animation

		self._collision_rect = Rect(pos[0],pos[1],48,74)
		self._walking_line = Rect(pos[0],pos[1]+74,48,1)

	def draw(self, surface, tick):
		if self._state == Character.STANDING:
			self._stand_animation.draw(surface, self._collision_rect.x, self._collision_rect.y, tick)
		elif self._state == Character.WALKING:
			self._walk_animation.draw(surface, self._collision_rect.x, self._collision_rect.y, tick)
		if Character.DEBUG:
			pygame.draw.rect(surface, (255,255,255), self._collision_rect, 1)
			pygame.draw.rect(surface, (255,255,255), self._walking_line, 1)

	def tick(self, platforms):
		self._state = Character.STANDING
		if self._is_falling:
			if self._dy < Character.MAX_FALLING:
				self._dy += Character.V_FALLING
		else:
			self._dy = 0
		self._collision_rect = self._collision_rect.move(0, self._dy)
		self._walking_line = self._walking_line.move(0, self._dy)
		coliding = None
		for platform in platforms:
			if platform.collides(self._collision_rect):
				coliding = platform
				break
		if coliding is not None:
			while platform.collides(self._collision_rect):
				self._collision_rect = self._collision_rect.move(0, -self._dy*0.5)
				self._walking_line = self._walking_line.move(0, -self._dy*0.5)


	def move(self, dx, platforms):
		self._collision_rect = self._collision_rect.move(dx * Character.SPEED, 0)
		self._walking_line = self._walking_line.move(dx * Character.SPEED, 0)
		self._state = Character.WALKING
		for platform in platforms:
			if platform.collides(self._collision_rect):
				self._collision_rect = self._collision_rect.move(-dx * Character.SPEED, 0)
				self._walking_line = self._walking_line.move(-dx * Character.SPEED, 0)
				break

	def jump(self):
		self._is_falling = True
		self._dy = -5
