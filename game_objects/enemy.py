from pygame.rect import Rect
from graphics.drawables.animated import Animated
from graphics.drawables.animation import Animation
from resources.animations.animation_manager import AnimationManager
from resources.pictures.picture_manager import PictureManager
from resources.sounds.sound_manager import SoundManager
from utils.vector import Vector2

__author__ = 'Donhilion'


class Enemy(object):
	""" The enemy class.

	An instance of this class represents an enemy in the game.

	Attributes:
		_pos: The current position of the enemy.
		_direction: The current direction of the enemy. This could be LEFT or RIGHT.
		_collision_rect: The rectangle to check for collisions.
		_head_rect: The rectangle to check for deadly collisions.
		_walking_line: The rectangle to determine if the enemy is standing on the ground.
		_left_rect: The rectangle to determine if the enemy has reached the left end of a platform.
		_right_rect: The rectangle to determine if the enemy has reached the right end of a platform.
		_dy: The vertical speed of the enemy.
		_pic: The picture to display the enemy.
		_death_animation: The death animation of this enemy.
		_hit_sound: The sound when the character takes damage from this enemy.
		_death_sound: The sound when this enemy dies.
	"""

	# The horizontal speed.
	SPEED = 1
	# Value for the _direction attribute.
	LEFT, RIGHT = range(2)
	# Maximal falling speed.
	MAX_FALLING = 2
	# Vertical acceleration.
	V_FALLING = 0.1

	def __init__(self, pos=None, direction=LEFT, pic=None, death_animation=None):
		if pos is None:
			pos = [0, 0]
		if pic is None or death_animation is None:
			animation_manager = AnimationManager.MANAGER
			animation = animation_manager.get_animation("animations")
			if pic is None:
				pic = Animated(PictureManager.MANAGER, animation[0], animation[1]["Monster"])
			if death_animation is None:
				death_animation = (PictureManager.MANAGER, animation[0], animation[1]["MonsterExplode"])
		self._pos = pos
		self._direction = direction
		self._collision_rect = Rect(pos, (31, 31))
		self._head_rect = Rect((pos[0], pos[1] - 4), (31, 4))
		self._walking_line = Rect((pos[0], pos[1] + 31), (31, 1))
		self._left_rect = Rect((pos[0] - 1, pos[1] + 31), (1, 1))
		self._right_rect = Rect((pos[0] + 30, pos[1] + 31), (1, 1))
		self._dy = 0
		self._pic = pic
		self._death_animation = death_animation

		self._hit_sound = SoundManager.MANAGER.get_sound("hit.wav")
		self._death_sound = SoundManager.MANAGER.get_sound("coin.wav")

	def draw(self, surface, tick, camera, size):
		""" Draws the enemy.

		This method draws the enemy on the given surface.

		Args:
			surface: The surface to draw on.
			tick: the current tick of the game.
			camera: The position of the camera.
			size: The size of the window. This argument is not used at the moment.
		"""
		self._pic.draw(surface, self._collision_rect.x - camera[0], self._collision_rect.y - camera[1], tick, False)

	def tick(self, platforms):
		""" Method for handling the game ticks.

		This method should be called every tick to calculate the enemy changes.

		Args:
			platforms: The platforms of the level.
		"""
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
		""" Checks for collision.

		This method checks for a collision with the character.
		If the character collides on the side he gets damage.
		If the character collides on the top the enemy dies and the character gets points.

		Args:
			character: The character to check with.

		Returns:
			The death animation if the enemy dies. None otherwise.
		"""
		if character.is_colliding(self._collision_rect):
			character.change_lives(-1)
			self._hit_sound.play()
		elif character.is_colliding(self._head_rect):
			character.change_points(10)
			character.jump()
			self._death_sound.play()
			return Animation(self._death_animation[0], self._death_animation[1], self._death_animation[2],
							 (self._collision_rect.x - 14, self._collision_rect.y - 14))
		return None


class FlyingEnemy(Enemy):
	""" The flying enemy class.

	An instance of this class represents an flying enemy in the game.

	Attributes:
		_route: The route the enemy flies.
		_next_point: The index of the next point the enemy flies to.
		_vector: The current vector the enemy flies.
		_flying_type: The flying type of the enemy.
		_forward: This optional flag, used for the LINE type, determines if the enemy moves forward or backward in the list of points.
	"""

	# Values for the _flying_type attributes.
	LINE, CIRCLE = range(2)

	def __init__(self, route=None, flying_type=CIRCLE, pic=None, death_animation=None):
		if route is None or len(route) < 2:
			route = [[0, -50], [100, -50], [100, 0]]
		self._route = route
		self._next_point = 1
		self._vector = (Vector2(route[1]) - Vector2(route[0])).normal()
		self._flying_type = flying_type
		if flying_type == FlyingEnemy.LINE:
			self._forward = True

		if pic is None or death_animation is None:
			animation_manager = AnimationManager.MANAGER
			animation = animation_manager.get_animation("animations")
			if pic is None:
				pic = Animated(PictureManager.MANAGER, animation[0], animation[1]["Flying"])
			if death_animation is None:
				death_animation = (PictureManager.MANAGER, animation[0], animation[1]["FlyingExplode"])

		pos = route[0][:]
		Enemy.__init__(self, pos=pos, pic=pic, death_animation=death_animation)

	def tick(self, platforms):
		""" Method for handling the game ticks.

		This method should be called every tick to calculate the enemy changes.

		Args:
			platforms: The platforms of the level.
		"""
		vector = self._vector * Enemy.SPEED

		self._pos[0] += vector.x
		self._pos[1] += vector.y
		self._collision_rect.x = self._pos[0]
		self._collision_rect.y = self._pos[1]
		self._head_rect.x = self._pos[0]
		self._head_rect.y = self._pos[1] - 4

		if not self._vector == (Vector2(self._route[self._next_point]) - Vector2(self._pos)).normal():
			if self._flying_type == FlyingEnemy.CIRCLE:
				next_point = (self._next_point + 1) % len(self._route)
			elif self._forward:
				next_point = self._next_point + 1
				if next_point >= len(self._route):
					self._forward = False
					next_point -= 2
			else:
				next_point = self._next_point - 1
				if next_point < 0:
					self._forward = True
					next_point += 2
			self._vector = (Vector2(self._route[next_point]) - Vector2(self._route[self._next_point])).normal()
			self._next_point = next_point
