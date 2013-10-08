import pygame
from pygame.locals import *
from game_objects.character import Character
from game_objects.collectable import Collectable
from ressources.levels.level_manager import LevelManager

from ressources.pictures.picture_manager import PictureManager
from ressources.sounds.sound_manager import SoundManager
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
		#self.bg = PictureManager.MANAGER.loaded["background.png"]
		#self.bg = PictureManager.MANAGER.loaded["bg2.png"]
		self.bg = PictureManager.MANAGER.loaded["sparksis.png"]
		self.bg_w = self.bg.get_width()
		self.bg_h = self.bg.get_height()
		self.heart = PictureManager.MANAGER.loaded["Heart.png"]
		self.coin = PictureManager.MANAGER.loaded["Coin.png"]
		self.tick = 0
		self.last_ticks = pygame.time.get_ticks()
		self.dx = 0
		self.jumping = False
		self.font = pygame.font.SysFont("arial", 24)

		self.level = LevelManager.MANAGER.levels[level]

		self.character = Character(pos=self.level.get_start())
		self.platforms = self.level.get_platforms()

		collectables = self.level.get_collectables()
		self.collectables = []
		for collectable in collectables:
			self.collectables.append(Collectable(collectable, pic = self.coin))

		goal = self.level.get_goal()
		self.goal = Rect(goal, (50, 50))
		self.goal_pic = PictureManager.MANAGER.loaded["goal.png"]


		deadzone = self.level.get_deadzone()
		self.deadzone = Rect(deadzone[:2], deadzone[2:])

		self.enemies = self.level.get_enemies()
		self.animations = []

		self.jump_sound = SoundManager.MANAGER.loaded["jump.wav"]
		self.bg_sound = SoundManager.MANAGER.loaded["test.ogg"]

	def reset_tick(self):
		self.last_ticks = pygame.time.get_ticks()

	def draw(self):
		y = -(self.camera[1] % self.bg_h)
		while y < self.bg_h:
			x = -(self.camera[0] % self.bg_w)
			while x < self.bg_w:
				self.screen.blit(self.bg, (x,y))
				x += self.bg_w
			y += self.bg_h

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
				self.jump_sound.play()

			if not self.character.is_invincible():
				for enemy in self.enemies:
					animation = enemy.collide(self.character)
					if animation is not None:
						self.enemies.remove(enemy)
						self.animations.append(animation)

			self.character.tick(self.platforms, self.collectables)
			if self.dx != 0:
				self.character.move(self.dx, self.platforms)

			if self.character.is_colliding(self.deadzone) or self.character.get_lives() < 1:
				self.bg_sound.stop()
				self.window.switch(window.Window.GAME_OVER)

			if self.character.is_colliding(self.goal):
				self.bg_sound.stop()
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

		# draw animations
		for animation in self.animations:
			if not animation.draw(self.screen, self.camera, tick):
				self.animations.remove(animation)

		# draw points
		text = self.font.render(str(self.character.get_points()), True, (255, 255, 255))
		self.screen.blit(text, (self.width - text.get_width() - 10, 10))
		self.screen.blit(self.coin, (self.width - text.get_width() - 32, 14))

		# draw lives
		self.screen.blit(self.heart, (10, 14))
		text = self.font.render(str(self.character.get_lives()), True, (255, 255, 255))
		self.screen.blit(text, (32, 10))

		# draw the goal
		self.screen.blit(self.goal_pic, (self.goal.x-self.camera[0], self.goal.y-self.camera[1]))




	def key_down(self, key):
		if key == K_ESCAPE:
			self.bg_sound.stop()
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

	def start_music(self):
		#self.bg_sound.play(-1)
		pass
