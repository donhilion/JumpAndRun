import pygame
from pygame.locals import *
from game_objects.character import Character
from game_objects.enemy import Enemy
from game_objects.platform import Platform
from game_objects.collectable import Collectable
from ressources.levels.level_manager import LevelManager

from ressources.pictures.picture_manager import PictureManager
import window

class GameSurface(object):
	'''
	'''

	def __init__(self, screen, width, height, window, level="level0"):
		self.screen = screen
		self.width = width
		self.height = height
		self.window = window
		self.camera = [0,0]
		self.bg = PictureManager.MANAGER.loaded["background.png"]
		#self.bg = PictureManager.MANAGER.loaded["bg2.png"]
		self.bg = pygame.transform.scale(self.bg, (height, height))
		self.tick = 0
		self.last_ticks = pygame.time.get_ticks()
		self.dx = 0
		self.jumping = False
		self.font = pygame.font.SysFont("arial", 24)

		self.level = LevelManager.MANAGER.levels[level]

		self.character = Character(pos=self.level.get_start())
		self.platforms = self.level.get_platforms()

		self.collectables = self.level.get_collectables()

		goal = self.level.get_goal()
		self.goal = Rect(goal, (50, 50))
		self.goal_pic = PictureManager.MANAGER.loaded["goal.png"]


		deadzone = self.level.get_deadzone()
		self.deadzone = Rect(deadzone[:2], deadzone[2:])

		self.enemies = [Enemy([200,0])]

	def reset_tick(self):
		self.last_ticks = pygame.time.get_ticks()

	def draw(self):
		y = -(self.camera[1] % self.height)
		while y < self.height:
			x = -(self.camera[0] % self.height)
			while x < self.width:
				self.screen.blit(self.bg, (x,y))
				x += self.height
			y += self.height

		tick = self.tick / 10

		# calculate the ticks
		current_ticks = pygame.time.get_ticks()
		delta = (current_ticks - self.last_ticks)
		self.tick += delta
		self.last_ticks = current_ticks

		# handle the ticks
		for i in range(self.tick/10 - tick):
			# handle enemies
			for enemy in self.enemies:
				enemy.tick(self.platforms)

			# check walking collision
			standing = False
			for platform in self.platforms:
				if platform.collides(self.character._walking_line):
					standing = True
					break
			self.character._is_falling = not standing
			if standing and self.jumping:
				self.character.jump()

			if not self.character.is_invincible():
				for enemy in self.enemies:
					if enemy.collide(self.character):
						self.enemies.remove(enemy)

			self.character.tick(self.platforms, self.collectables)
			if self.dx != 0:
				self.character.move(self.dx, self.platforms)

			if self.character.is_colliding(self.deadzone) or self.character.get_lives() < 1:
				self.window.switch(window.Window.GAME_OVER)

			if self.character.is_colliding(self.goal):
				self.window.switch(window.Window.WIN_SCREEN, self.character.get_points())

		# center camera around player
		self.camera[0] = self.character.get_x() - self.width / 2
		self.camera[1] = self.character.get_y() - self.height / 2

		# draw the platforms
		for platform in self.platforms:
			platform.draw(self.screen, tick, self.camera, (self.width, self.height))

		# draw collectables
		for collectable in self.collectables:
			collectable.draw(self.screen, tick, self.camera, (self.width, self.height))

		# draw enemies
		for enemy in self.enemies:
			enemy.draw(self.screen, tick, self.camera, (self.width, self.height))


		# draw the character
		self.character.draw(self.screen, tick, self.camera, (self.width, self.height))

		# draw points
		text = self.font.render(str(self.character.get_points()), True, (255, 255, 255))
		self.screen.blit(text, (self.width - text.get_width() - 10, 10))

		# draw lives
		text = self.font.render(str(self.character.get_lives()), True, (255, 255, 255))
		self.screen.blit(text, (10, 10))

		# draw the goal
		self.screen.blit(self.goal_pic, (self.goal.x-self.camera[0], self.goal.y-self.camera[1]))




	def key_down(self, key):
		if key == K_ESCAPE:
			self.window.switch(window.Window.MENU)
		elif key == K_RIGHT:
			self.dx += 1
		elif key == K_LEFT:
			self.dx -= 1
		elif key == K_UP:
			self.jumping = True

	def key_up(self, key):
		if key == K_RIGHT:
			self.dx -= 1
		elif key == K_LEFT:
			self.dx += 1
		elif key == K_UP:
			self.jumping = False
