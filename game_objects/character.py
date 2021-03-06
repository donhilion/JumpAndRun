from pygame import Rect
import pygame

from graphics.drawables.animated import Animated
from graphics.drawables.animation import Animation
from resources.animations.animation_manager import AnimationManager
from resources.pictures.picture_manager import PictureManager
from resources.sounds.sound_manager import SoundManager


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
		_death_animation: Contains the death animation of the character.
		_collision_rect: The rectangle for collision detection.
		_top_rect: The rectangle for on the top of the character.
		_bottom_rect: The rectangle for on the bottom of the character.
		_left_rect: The rectangle for on the left of the character.
		_right_rect: The rectangle for on the right of the character.
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
	# Width of the character.
	WIDTH = 27
	# Height of the character.
	HEIGHT = 48

	def __init__(self, pos=[0, 0], state=STANDING, lives=3, points=0, walk_animation=None, stand_animation=None,
				 jump_animation=None, jump_right_animation=None, death_animation=None):
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
			death_animation: The death animation of the character.
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
			animation = animation_manager.get_animation("animations")
			if walk_animation is None:
				walk_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["HeroWalk"], True)
			if stand_animation is None:
				stand_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["HeroStand"])
			if jump_animation is None:
				jump_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["HeroJump"])
			if jump_right_animation is None:
				jump_right_animation = Animated(PictureManager.MANAGER, animation[0], animation[1]["HeroJumpRight"],
												True)
			if death_animation is None:
				death_animation = (PictureManager.MANAGER, animation[0], animation[1]["HeroDie"])
		self._walk_animation = walk_animation
		self._stand_animation = stand_animation
		self._jump_animation = jump_animation
		self._jump_right_animation = jump_right_animation
		self._death_animation = death_animation

		self._pos = pos[:]

		self._collision_rect = Rect(pos[0], pos[1], Character.WIDTH, Character.HEIGHT)

		self._top_rect = Rect(pos[0], pos[1], Character.WIDTH, 1)
		self._bottom_rect = Rect(pos[0], pos[1] + Character.HEIGHT - 1, Character.WIDTH, 1)
		self._left_rect = Rect(pos[0], pos[1], 1, Character.HEIGHT - 1)
		self._right_rect = Rect(pos[0] + Character.WIDTH - 1, pos[1], 1, Character.HEIGHT - 1)

		self._collect_sound = SoundManager.MANAGER.get_sound("coin.wav")

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
			move = camera[:]
			move[0] *= -1
			move[1] *= -1
			pygame.draw.rect(surface, (255, 255, 255), self._collision_rect.move(move), 2)
			pygame.draw.rect(surface, (255, 0, 0), self._top_rect.move(move), 1)
			pygame.draw.rect(surface, (255, 0, 0), self._bottom_rect.move(move), 1)
			pygame.draw.rect(surface, (0, 0, 255), self._left_rect.move(move), 1)
			pygame.draw.rect(surface, (0, 0, 255), self._right_rect.move(move), 1)

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
		self._pos[1] += self._dy
		self._adjust_rects()

		movedX = 0
		movedY = 0
		for platform in platforms:
			while platform.collides(self._collision_rect):
				dx = 0
				dy = 0
				if platform.collides(self._top_rect):
					dy += 1
				if platform.collides(self._bottom_rect):
					dy -= 1
				if platform.collides(self._left_rect):
					dx += 1
				if platform.collides(self._right_rect):
					dx -= 1
				if dx == 0 and dy == 0: # completely in platform
					print("a")
					return # TODO: dead
				if (dx != 0 and dx == -movedX) or (dy != 0 and dy == -movedY): # crushed
					return # TODO: dead
				self._pos[0] += dx
				self._pos[1] += dy
				self._adjust_rects()
				movedX = dx
				movedY = dy

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

		self._pos[0] += dx * Character.SPEED
		self._adjust_rects()
		if self._state is not Character.JUMPING:
			self._state = Character.WALKING

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
		return self._bottom_rect.move(0,1)

	def get_death_animation(self):
		""" Returns the death animation.

		This method returns the death animation on the current location of the character.

		Returns:
			The death animation of the character.
		"""
		return Animation(self._death_animation[0], self._death_animation[1], self._death_animation[2],
						 (self._collision_rect.x - 11, self._collision_rect.y))

	def _adjust_rects(self):
		self._collision_rect.x = self._pos[0]
		self._collision_rect.y = self._pos[1]
		self._top_rect.x = self._collision_rect.x
		self._top_rect.y = self._collision_rect.y
		self._bottom_rect.x = self._collision_rect.x
		self._bottom_rect.y = self._collision_rect.y + Character.HEIGHT - 1
		self._left_rect.x = self._collision_rect.x
		self._left_rect.y = self._collision_rect.y
		self._right_rect.x = self._collision_rect.x + Character.WIDTH - 1
		self._right_rect.y = self._collision_rect.y
