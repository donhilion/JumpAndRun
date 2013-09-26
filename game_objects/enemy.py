import pygame
from pygame.rect import Rect
from ressources.pictures.picture_manager import PictureManager

__author__ = 'donhilion'

class Enemy(object):

	SPEED = 1
	LEFT, RIGHT = range(2)
	MAX_FALLING = 2
	V_FALLING = 0.1

	def __init__(self, pos = None, direction = LEFT, pic = None):
		if pos is None:
			pos = [0,0]
		if pic is None:
			pic = PictureManager.MANAGER.loaded["monster.png"]
		self._pos = pos
		self._direction = direction
		self._collision_rect = Rect(pos, (30,30))
		self._head_rect = Rect((pos[0], pos[1]-4), (30,4))
		self._walking_line = Rect((pos[0], pos[1]+30), (30,1))
		self._left_rect = Rect((pos[0]-1, pos[1]+30), (1,1))
		self._right_rect = Rect((pos[0]+30, pos[1]+30), (1,1))
		self._dy = 0
		self._pic = pic

	def draw(self, surface, tick, camera, size):
		surface.blit(self._pic, (self._collision_rect.x - camera[0], self._collision_rect.y - camera[1]))

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
		elif character.is_colliding(self._head_rect):
			character.change_points(10)
			return True
		return False

