from graphics.drawables.animated import Animated
from ressources.animations.animation_manager import AnimationManager
from ressources.pictures.picture_manager import PictureManager
from pygame import Rect
import pygame

__author__ = 'donhilion'

class Character(object):

	STANDING, WALKING, JUMPING = range(3)
	SPEED = 1
	DEBUG = False
	MAX_FALLING = 2
	V_FALLING = 0.1

	def __init__(self, pos = [0, 0], state = STANDING, points = 0, walk_animation = None, stand_animation = None, jump_animation = None):
		self._state = state
		self._points = points
		self._is_falling = False
		self._dy = 0
		self._left = False
		if walk_animation is None or stand_animation is None or jump_animation is None:
			animation_manager = AnimationManager.MANAGER
			animation = animation_manager.animations["animations.xml"]
			if walk_animation is None:
				walk_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["dudeMov"], True)
			if stand_animation is None:
				stand_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["dudeStill"], True)
			if jump_animation is None:
				jump_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["dudeJump"], True)
		self._walk_animation = walk_animation
		self._stand_animation = stand_animation
		self._jump_animation = jump_animation

		self._collision_rect = Rect(pos[0],pos[1],28,49)
		self._walking_line = Rect(pos[0],pos[1]+49,28,1)

	def draw(self, surface, tick, camera, size):
		if self._state == Character.STANDING:
			self._stand_animation.draw(surface, self._collision_rect.x - camera[0], self._collision_rect.y - camera[1], tick, self._left)
		elif self._state == Character.WALKING:
			self._walk_animation.draw(surface, self._collision_rect.x - camera[0], self._collision_rect.y - camera[1], tick, self._left)
		elif self._state == Character.JUMPING:
			self._jump_animation.draw(surface, self._collision_rect.x - camera[0], self._collision_rect.y - camera[1], tick, self._left)
		if Character.DEBUG:
			pygame.draw.rect(surface, (255,255,255), self._collision_rect, 1)
			pygame.draw.rect(surface, (255,255,255), self._walking_line, 1)

	def tick(self, platforms, collectables):
		self._state = Character.STANDING
		if self._is_falling:
			if self._dy < Character.MAX_FALLING:
				self._dy += Character.V_FALLING
			self._state = Character.JUMPING
		else:
			self._dy = 0
		self._collision_rect = self._collision_rect.move(0, self._dy)
		self._walking_line = self._walking_line.move(0, self._dy)
		colliding = None
		for platform in platforms:
			if platform.collides(self._collision_rect):
				colliding = platform
				break
		if colliding is not None:
			while platform.collides(self._collision_rect):
				self._collision_rect = self._collision_rect.move(0, -self._dy*0.5)
				self._walking_line = self._walking_line.move(0, -self._dy*0.5)

		for collectable in collectables:
			if collectable.collides(self._collision_rect):
				self._points += collectable.get_value()
				collectables.remove(collectable)


	def move(self, dx, platforms):
		if dx < 0:
			self._left = True
		elif dx > 0:
			self._left = False
		self._collision_rect = self._collision_rect.move(dx * Character.SPEED, 0)
		self._walking_line = self._walking_line.move(dx * Character.SPEED, 0)
		if self._state is not Character.JUMPING:
			self._state = Character.WALKING
		for platform in platforms:
			if platform.collides(self._collision_rect):
				self._collision_rect = self._collision_rect.move(-dx * Character.SPEED, 0)
				self._walking_line = self._walking_line.move(-dx * Character.SPEED, 0)
				break

	def jump(self):
		self._is_falling = True
		self._dy = -5

	def get_points(self):
		return self._points

	def is_colliding(self, rect):
		return rect.colliderect(self._collision_rect)

	def get_x(self):
		return self._collision_rect.x + 14
