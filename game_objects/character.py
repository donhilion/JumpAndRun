from pygame import Rect
import pygame

from graphics.drawables.animated import Animated
from ressources.animations.animation_manager import AnimationManager
from ressources.pictures.picture_manager import PictureManager
from ressources.sounds.sound_manager import SoundManager


__author__ = 'Donhilion'


class Character(object):
	""" The character class.

	An object of this class represents the playable character.

	Attributes:
		_state: The current state of the character. This might be STANDING, WALKING or JUMPING.
		_lives: The current number of lives left.
		_points: The current points of this character
		_is_falling: Determines if the character is falling at the moment.
		_dy: Vertical speed of the character.
		_direction: The direction the character is looking. This can be LEFT, RIGHT or NONE.
		_invincible: Determines if the character is invincible at the moment.
		_walk_animation: Contains the walking animation.
		_stand_animation: Contains the standing animation
		_jump_animation: Contains the jumping animation for the NONE direction.
		_jump_right_animation: Contains the jumping animation for the directions LEFT and RIGHT.
		_collision_rect: The rectangle for collision detection.
		_walking_line: The rectangle to determine if the character is standing on the ground.
		_head_line: The rectangle for collision detection during jumping.
		_collect_sound: The sound for collecting coins.
	"""

	# Values for the _state attribute.
	STANDING, WALKING, JUMPING = range(3)
	# Values for the _direction attribute.
	LEFT, RIGHT, NONE = range(3)
	# Horizontal speed.
	SPEED = 1
	# If true more information is displayed.
	DEBUG = False
	# Maximal falling speed.
	MAX_FALLING = 2
	# Vertical acceleration.
	V_FALLING = 0.1

	def __init__(self, pos=(0, 0), state=STANDING, lives=3, points=0, walk_animation=None, stand_animation=None,
				 jump_animation=None, jump_right_animation=None):
		""" Generates a new instance of this class.

		Generates a new instance of the character class and sets the field information.
		If the animation arguments are left empty, the standard animations will be used.

		Args:
			pos: The starting position of the character.
			state: The starting state of the character.
			lives: The starting number of lives of the character.
			points: The starting point count of the character.
			walk_animation: The walking animation of the character.
			stand_animation: The standing animation of the character.
			jump_animation: The jumping animation of the character for the direction NONE.
			jump_right_animation: The jumping animation of the character for the directions LEFT and RIGHT.
		"""
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
				walk_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["HeroWalk"], True)
			if stand_animation is None:
				stand_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["HeroStand"])
			if jump_animation is None:
				jump_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["HeroJump"])
			if jump_right_animation is None:
				jump_right_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["HeroJumpRight"],
												True)
		self._walk_animation = walk_animation
		self._stand_animation = stand_animation
		self._jump_animation = jump_animation
		self._jump_right_animation = jump_right_animation

		self._collision_rect = Rect(pos[0], pos[1], 27, 48)
		self._walking_line = Rect(pos[0], pos[1] + 48, 27, 1)
		self._head_line = Rect(pos[0], pos[1] - 1, 27, 1)

		self._collect_sound = SoundManager.MANAGER.loaded["coin.wav"]

	def draw(self, surface, tick, camera, size):
		""" The drawing method.

		This method draws the character on the given surface.

		Args:
			surface: The surface the character will be drawn on.
			tick: The current tick of the game.
			camera: The position of the camera.
			size: The size of the window. This argument is not used at the moment.
		"""
		if self._state == Character.STANDING:
			self._stand_animation.draw(surface, self._collision_rect.x - camera[0], self._collision_rect.y - camera[1],
									   tick)
		elif self._state == Character.WALKING:
			self._walk_animation.draw(surface, self._collision_rect.x - camera[0], self._collision_rect.y - camera[1],
									  tick, self._direction == Character.LEFT)
		elif self._state == Character.JUMPING:
			if self._direction == Character.NONE:
				self._jump_animation.draw(surface, self._collision_rect.x - camera[0],
										  self._collision_rect.y - camera[1], tick)
			else:
				self._jump_right_animation.draw(surface, self._collision_rect.x - camera[0],
												self._collision_rect.y - camera[1], tick,
												self._direction == Character.LEFT)
		if Character.DEBUG:
			pygame.draw.rect(surface, (255, 255, 255), self._collision_rect, 1)
			pygame.draw.rect(surface, (255, 255, 255), self._walking_line, 1)
			pygame.draw.rect(surface, (255, 255, 255), self._head_line, 1)

	def tick(self, platforms, collectables):
		""" Method for handling game ticks.

		This method should be called every tick to calculate the character changes.

		Args:
			platforms: The platforms of the level.
			collectables: The collectables, like coins, of the level.
		"""
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
				self._collect_sound.play()


	def move(self, dx, platforms):
		""" This method moves the character.

		This method moves the character depending of the direction and the platforms of the level.

		Args:
			dx: The direction of the movement.
			platforms: The platforms of the level.
		"""
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
		""" This method lets the character jump.

		Calling this method, the vertical speed of the character is set to 5 in the up direction. This results in a jump.
		"""
		self._is_falling = True
		self._dy = -5

	def get_points(self):
		""" Method to get the current points.

		This method returns the current point count of the character.

		Returns:
			The current point count of the character.
		"""
		return self._points

	def is_colliding(self, rect):
		""" Method for checking for collision.

		This method checks if the character collides with the given rectangle.

		Args:
			rect: The rectangle to check with.

		Returns:
			True if the character collides with the given rectangle. Else otherwise.
		"""
		return rect.colliderect(self._collision_rect)

	def get_x(self):
		""" Returns the x coordinate.

		This method returns the x coordinate of the character.

		Returns:
			The x coordinate.
		"""
		return self._collision_rect.x + 14

	def get_y(self):
		""" Returns the y coordinate.

		This method returns the y coordinate of the character.

		Returns:
			The y coordinate.
		"""
		return self._collision_rect.y + 25

	def get_lives(self):
		"""	Returns the lives.

		This method returns the current live count of the character.

		Returns:
			The current lives.
		"""
		return self._lives

	def change_lives(self, dl):
		""" Changes the current lives.

		This method changes the current live count by the given amount.

		Args:
			dl: The delta to changes the live count by.
		"""
		self._lives += dl
		if dl < 0:
			self._invincible = 100
			self.jump()

	def change_points(self, dp):
		""" Changes the current points.

		This method changes the current point count by the given amount.

		Args:
			dp: The delta to change the point count by.
		"""
		self._points += dp

	def is_invincible(self):
		""" Returns the invincible flag.

		This method returns if the character is invincible at the moment.

		Returns:
			True if the character is invincible at the moment. Else otherwise.
		"""
		return self._invincible

	def get_walking_line(self):
		""" Returns the walking line.

		This method returns the character's current walking line.

		Returns:
			The character's current walking line.
		"""
		return self._walking_line
