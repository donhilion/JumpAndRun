import pygame
from pygame.locals import *
from game_objects.character import Character
from game_objects.collectable import Collectable
from game_objects.enemy import FlyingEnemy
from graphics.screen import Screen
from resources.levels.level_manager import LevelManager

from resources.pictures.picture_manager import PictureManager
from resources.sounds.sound_manager import SoundManager
from settings.settings import Settings
import window

__author__ = 'Donhilion'


class GameSurface(Screen):
	""" The game surface class.

	An object of this class represents the game surface where a level will be shown and the character moves.

	Attributes:
		_screen: The screen surface to draw on.
		_width: The width of the window.
		_height: The height of the window.
		_window: The surrounding window.
		_camera: The position of the camera.
		_bg: The background picture.
		_bg_w: The width of the background picture.
		_bg_h: The height of the background picture.
		_heart: The picture of a heart for the live counter.
		_coin: The picture of a coin for the point counter.
		_tick: The tick counter of the game.
		_last_ticks: The last tick provided by pygame.
		_dx: The horizontal direction resulting from the keys pressed.
		_jumping: Flag which determines if the jump button is pressed.
		_font: The font used for displaying lives and points.
		_level: The current level.
		_character: The character of this game.
		_character_death_animation: The death animation of the character.
		_platforms: The platforms of this game.
		_collectables: The collectables of this game.
		_goal: The goal of this game.
		_goal_pic: The picture of the goal.
		_deadzone: The deadzone of the game.
		_enemies: The enemies of the game.
		_animations: The current animations to display.
		_jump_sound: The sound for the character jumping.
		_bg_sound: The background music.
	"""

	# The name of the background picture file.
	BG_PICTURE_NAME = "bg.png"
	# The name of the heat picture file.
	HEART_PICTURE_NAME = "Heart.png"
	# The name of the coin picture file.
	COIN_PICTURE_NAME = "Coin.png"
	# The name of the goal picture file.
	GOAL_PICTURE_NAME = "goal.png"
	# The name of the jump sound file.
	JUMP_SOUND_NAME = "jump.wav"
	# The name of the background sound file.
	BG_SOUND_NAME = "music0.wav"

	def __init__(self, screen, width, height, window, level="level1"):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.

		Args:
			screen: The screen surface to draw on.
			width: The width of the window.
			height: The height of the window.
			window: The surrounding window.
			level: The name of the level which should be loaded.
		"""
		self._screen = screen
		self._width = width
		self._height = height
		self._window = window
		self._camera = [0, 0]
		self._bg = PictureManager.MANAGER.get_picture(GameSurface.BG_PICTURE_NAME)
		self._bg_w = self._bg.get_width()
		self._bg_h = self._bg.get_height()
		self._heart = PictureManager.MANAGER.get_picture(GameSurface.HEART_PICTURE_NAME)
		self._coin = PictureManager.MANAGER.get_picture(GameSurface.COIN_PICTURE_NAME)
		self._tick = 0
		self._last_ticks = pygame.time.get_ticks()
		self._dx = 0
		self._jumping = False
		self._font = pygame.font.SysFont("arial", 24)

		self._level = LevelManager.MANAGER.get_level(level)

		self._character = Character(pos=self._level.get_start())
		self._character_death_animation = None
		self._platforms = self._level.get_platforms()

		collectables = self._level.get_collectables()
		self._collectables = []
		for collectable in collectables:
			self._collectables.append(Collectable(collectable, pic=self._coin))

		goal = self._level.get_goal()
		self._goal = Rect(goal, (50, 50))
		self._goal_pic = PictureManager.MANAGER.get_picture(GameSurface.GOAL_PICTURE_NAME)

		deadzone = self._level.get_deadzone()
		self._deadzone = Rect(deadzone[:2], deadzone[2:])

		self._enemies = self._level.get_enemies()[:]
		self._animations = []

		self._jump_sound = SoundManager.MANAGER.get_sound(GameSurface.JUMP_SOUND_NAME)
		self._bg_sound = SoundManager.MANAGER.get_sound(GameSurface.BG_SOUND_NAME)

	def reset_tick(self):
		""" Resets the ticks.

		This method resets the ticks.
		It should be called before the game is resumed after a pause.
		"""
		self._last_ticks = pygame.time.get_ticks()

	def draw(self):
		""" Draws the game.

		This method draws the level and the character on the screen surface.
		Before something is drawn, the changes in the game world will be calculated depending on the amount of ticks which have passed.
		"""
		y = -(self._camera[1] % self._bg_h)
		while y < self._height:
			x = -(self._camera[0] % self._bg_w)
			while x < self._width:
				self._screen.blit(self._bg, (x, y))
				x += self._bg_w
			y += self._bg_h

		tick = self._tick / 10

		# calculate the ticks
		current_ticks = pygame.time.get_ticks()
		delta = (current_ticks - self._last_ticks)
		self._tick += delta
		self._last_ticks = current_ticks

		# handle the ticks
		for i in range(self._tick / 10 - tick):
			# handle enemies
			for enemy in self._enemies:
				enemy.tick(self._platforms)

			if self._character_death_animation is None:
				# check walking collision
				standing = False
				walking_line = self._character.get_walking_line()
				for platform in self._platforms:
					if platform.collides(walking_line):
						standing = True
						break
				self._character._is_falling = not standing
				if standing and self._jumping:
					self._character.jump()
					self._jump_sound.play()

				if not self._character.is_invincible():
					for enemy in self._enemies:
						animation = enemy.collide(self._character)
						if animation is not None:
							self._enemies.remove(enemy)
							self._animations.append(animation)

				self._character.tick(self._platforms, self._collectables)
				if self._dx != 0:
					self._character.move(self._dx, self._platforms)

				if self._character.is_colliding(self._deadzone) or self._character.get_lives() < 1:
					self._character_death_animation = self._character.get_death_animation()

				if self._character.is_colliding(self._goal):
					self._bg_sound.stop()
					self._window.switch(window.Window.WIN_SCREEN, self._character.get_points())

		# center camera around player
		self._camera[0] = self._character.get_x() - self._width / 2
		self._camera[1] = self._character.get_y() - self._height / 2

		# draw the platforms
		for platform in self._platforms:
			platform.draw(self._screen, tick, self._camera, (self._width, self._height))

		# draw collectables
		for collectable in self._collectables:
			collectable.draw(self._screen, tick, self._camera, (self._width, self._height))

		# draw enemies
		for enemy in self._enemies:
			enemy.draw(self._screen, tick, self._camera, (self._width, self._height))

		# draw the character
		if self._character_death_animation is None:
			self._character.draw(self._screen, tick, self._camera, (self._width, self._height))
		elif not self._character_death_animation.draw(self._screen, self._camera, tick):
			self._bg_sound.stop()
			self._window.switch(window.Window.GAME_OVER)

		# draw animations
		for animation in self._animations:
			if not animation.draw(self._screen, self._camera, tick):
				self._animations.remove(animation)

		# draw points
		text = self._font.render(str(self._character.get_points()), True, (255, 255, 255))
		self._screen.blit(text, (self._width - text.get_width() - 10, 10))
		self._screen.blit(self._coin, (self._width - text.get_width() - 32, 14))

		# draw lives
		self._screen.blit(self._heart, (10, 14))
		text = self._font.render(str(self._character.get_lives()), True, (255, 255, 255))
		self._screen.blit(text, (32, 10))

		# draw the goal
		self._screen.blit(self._goal_pic, (self._goal.x - self._camera[0], self._goal.y - self._camera[1]))


	def key_down(self, key):
		""" Handles key down events.

		This method handles key down events.
		The pressing of the escape button results in the changing to the menu screen.
		The cursor keys will move the character.

		Args:
			key: The key event information provided by pygame.
		"""
		if key == K_ESCAPE:
			self._bg_sound.stop()
			self._window.switch(window.Window.MENU)
		elif key == K_RIGHT:
			self._dx += 1
		elif key == K_LEFT:
			self._dx -= 1
		elif key == K_UP or key == K_SPACE:
			self._jumping = True

	def key_up(self, key):
		""" Handles key up events.

		This method handles key up events.
		The release of the cursor keys will be handled.

		Args:
			key: The key event information provided by pygame.
		"""
		if key == K_RIGHT:
			self._dx -= 1
		elif key == K_LEFT:
			self._dx += 1
		elif key == K_UP or key == K_SPACE:
			self._jumping = False

	def start_music(self):
		""" Starts the music.

		This method will start the background sound as a repeating music.
		"""
		self._bg_sound.play()
		pass

	def get_settings(self, settings):
		""" Reads the settings.

		This method reads and applies the given settings.

		Args:
			settings: The settings to read.
		"""
		# set volume
		volume = settings.get_value(Settings.SOUND_VOLUME) / 10.0
		music = settings.get_value(Settings.MUSIC_VOLUME) / 10.0
		fx = settings.get_value(Settings.FX_VOLUME) / 10.0

		music *= volume
		fx *= volume
		SoundManager.MANAGER.set_volume(fx)
		self._bg_sound.set_volume(music)
