from graphics.drawables.animated import Animated
from ressources.animations.animation_manager import AnimationManager
from ressources.pictures.picture_manager import PictureManager
from pygame import Rect
import pygame

__author__ = 'donhilion'

class Character(object):

	STANDING, WALKING, JUMPING = range(3)
	LEFT, RIGHT, NONE = range(3)
	SPEED = 1
	DEBUG = False
	MAX_FALLING = 2
	V_FALLING = 0.1

	def __init__(self, pos = [0, 0], state = STANDING, lives = 3, points = 0, walk_animation = None, stand_animation = None, jump_animation = None, jump_right_animation = None):
		self._state = state
		self._lives = lives
		self._points = points
		self._is_falling = False
		self._dy = 0
		self._direction = Character.NONE
		self._invincible = 0
		if walk_animation is None or stand_animation is None or jump_animation is None or jump_right_animation is None:
			animation_manager = AnimationManager.MANAGER
			animation = animation_manager.animations["animations.xml"]
			if walk_animation is None:
				#walk_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["dudeMov"], True)
				walk_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["HeroWalk"], True)
			if stand_animation is None:
				#stand_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["dudeStill"], True)
				stand_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["HeroStand"], True)
			if jump_animation is None:
				#jump_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["dudeJump"], True)
				jump_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["HeroJump"], True)
			if jump_right_animation is None:
				jump_right_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["HeroJumpRight"], True)
		self._walk_animation = walk_animation
		self._stand_animation = stand_animation
		self._jump_animation = jump_animation
		self._jump_right_animation = jump_right_animation

		self._collision_rect = Rect(pos[0],pos[1],27,48)
		self._walking_line = Rect(pos[0],pos[1]+48,27,1)
		self._head_line = Rect(pos[0], pos[1]-1, 27, 1)

	def draw(self, surface, tick, camera, size):
		if self._state == Character.STANDING:
			self._stand_animation.draw(surface, self._collision_rect.x - camera[0], self._collision_rect.y - camera[1], tick, self._direction == Character.LEFT)
		elif self._state == Character.WALKING:
			self._walk_animation.draw(surface, self._collision_rect.x - camera[0], self._collision_rect.y - camera[1], tick, self._direction == Character.LEFT)
		elif self._state == Character.JUMPING:
			if self._direction == Character.NONE:
				self._jump_animation.draw(surface, self._collision_rect.x - camera[0], self._collision_rect.y - camera[1], tick, self._direction == Character.LEFT)
			else:
				self._jump_right_animation.draw(surface, self._collision_rect.x - camera[0], self._collision_rect.y - camera[1], tick, self._direction == Character.LEFT)
		if Character.DEBUG:
			pygame.draw.rect(surface, (255,255,255), self._collision_rect, 1)
			pygame.draw.rect(surface, (255,255,255), self._walking_line, 1)
			pygame.draw.rect(surface, (255,255,255), self._head_line, 1)

	def tick(self, platforms, collectables):
		self._direction = Character.NONE
		if self._invincible > 0:
			self._invincible -= 1
		self._state = Character.STANDING
		if self._is_falling:
			if self._dy < Character.MAX_FALLING:
				self._dy += Character.V_FALLING
			self._state = Character.JUMPING
		else:
			self._dy = 0
		self._collision_rect = self._collision_rect.move(0, self._dy)
		self._walking_line = self._walking_line.move(0, self._dy)
		self._head_line = self._head_line.move(0, self._dy)
		colliding = None
		for platform in platforms:
			if platform.collides(self._collision_rect):
				colliding = platform
				break
		if colliding is not None:
			while platform.collides(self._collision_rect):
				if platform.collides(self._walking_line):
					direction = -1.0
				else:
					direction = 1.0
				self._dy *= 0.5
				self._collision_rect = self._collision_rect.move(0, direction)
				self._walking_line = self._walking_line.move(0, direction)
				self._head_line = self._head_line.move(0, direction)

		for collectable in collectables:
			if collectable.collides(self._collision_rect):
				self._points += collectable.get_value()
				collectables.remove(collectable)


	def move(self, dx, platforms):
		if dx < 0:
			self._direction = Character.LEFT
		elif dx > 0:
			self._direction = Character.RIGHT

		self._collision_rect = self._collision_rect.move(dx * Character.SPEED, 0)
		self._walking_line = self._walking_line.move(dx * Character.SPEED, 0)
		self._head_line = self._head_line.move(dx * Character.SPEED, 0)
		if self._state is not Character.JUMPING:
			self._state = Character.WALKING
		for platform in platforms:
			if platform.collides(self._collision_rect):
				self._collision_rect = self._collision_rect.move(-dx * Character.SPEED, 0)
				self._walking_line = self._walking_line.move(-dx * Character.SPEED, 0)
				self._head_line = self._head_line.move(-dx * Character.SPEED, 0)
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

	def get_y(self):
		return self._collision_rect.y + 25

	def get_lives(self):
		return self._lives

	def change_lives(self, dl):
		self._lives += dl
		if dl < 0:
			self._invincible = 100
			self.jump()

	def change_points(self, dp):
		self._points += dp

	def is_invincible(self):
		return self._invincible
