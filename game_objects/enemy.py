import pygame
from pygame.rect import Rect
from graphics.drawables.animated import Animated
from graphics.drawables.animation import Animation
from ressources.animations.animation_manager import AnimationManager
from ressources.pictures.picture_manager import PictureManager
from ressources.sounds.sound_manager import SoundManager

__author__ = 'donhilion'

class Enemy(object):

	SPEED = 1
	LEFT, RIGHT = range(2)
	MAX_FALLING = 2
	V_FALLING = 0.1

	def __init__(self, pos = None, direction = LEFT, pic = None, death_animation = None):
		if pos is None:
			pos = [0,0]
		if pic is None or death_animation is None:
			animation_manager = AnimationManager.MANAGER
			animation = animation_manager.animations["animations.xml"]
			if pic is None:
				pic = Animated(PictureManager.MANAGER, animation[0], animation[1]["Monster"])
			if death_animation is None:
				death_animation = (PictureManager.MANAGER, animation[0], animation[1]["MonsterExplode"])
		self._pos = pos
		self._direction = direction
		self._collision_rect = Rect(pos, (31,31))
		self._head_rect = Rect((pos[0], pos[1]-4), (31,4))
		self._walking_line = Rect((pos[0], pos[1]+31), (31,1))
		self._left_rect = Rect((pos[0]-1, pos[1]+31), (1,1))
		self._right_rect = Rect((pos[0]+30, pos[1]+31), (1,1))
		self._dy = 0
		self._pic = pic
		self._death_animation = death_animation

		self._hit_sound = SoundManager.MANAGER.loaded["hit.wav"]
		self._death_sound = SoundManager.MANAGER.loaded["coin.wav"]

	def draw(self, surface, tick, camera, size):
		self._pic.draw(surface, self._collision_rect.x - camera[0], self._collision_rect.y - camera[1], tick, False)

	def tick(self, platforms):
		if self._direction == Enemy.LEFT:
			dx = -Enemy.SPEED
		else:
			dx = Enemy.SPEED
		if self._dy < Enemy.MAX_FALLING:
			self._dy += Enemy.V_FALLING
		colliding = None
		for platform in platforms:
			if platform.collides(self._walking_line):
				colliding = platform
				break
		if colliding is not None:
			self._dy = 0
			if not colliding.collides(self._left_rect):
				self._direction = Enemy.RIGHT
			elif not colliding.collides(self._right_rect):
				self._direction = Enemy.LEFT
		self._collision_rect = self._collision_rect.move(dx, self._dy)
		self._head_rect = self._head_rect.move(dx, self._dy)
		self._walking_line = self._walking_line.move(dx, self._dy)
		self._left_rect = self._left_rect.move(dx, self._dy)
		self._right_rect = self._right_rect.move(dx, self._dy)

	def collide(self, character):
		if character.is_colliding(self._collision_rect):
			character.change_lives(-1)
			self._hit_sound.play()
		elif character.is_colliding(self._head_rect):
			character.change_points(10)
			self._death_sound.play()
			return Animation(self._death_animation[0], self._death_animation[1], self._death_animation[2], (self._collision_rect.x-14, self._collision_rect.y-14))
		return None

