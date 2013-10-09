import pygame

__author__ = 'Donhilion'


class Animation(object):
	""" The animation class.

	An object of this class represents an animation.

	Attributes:
		_animation: The list of frames and its duration of this animation.
		_max_frame_count: The overall duration of this animation.
		_first_tick: The first game tick after the animation was started.
		_pos: The position of the animation.
	"""

	def __init__(self, picture_manager, frame_list, animation, pos=(0, 0)):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.

		Args:
			picture_manager: The picture manager to use.
			frame_list: The list of frames.
			animation: The animation dictionary.
			pos: The position of this animation.
		"""
		frames = {}
		self._animation = []
		self._max_frame_count = 0
		self._first_tick = -1
		self._pos = pos

		for frame_key in frame_list:
			frame = frame_list[frame_key]
			picture = picture_manager.loaded[frame[0]]
			rect = pygame.Rect(float(frame[1]), float(frame[2]),
							   float(frame[3]) - float(frame[1]),
							   float(frame[4]) - float(frame[2]))
			part = picture.subsurface(rect)
			frames[frame_key] = part

		for part in animation:
			frame = frames[part[0]]
			count = int(part[1])
			self._max_frame_count += count
			self._animation.append((count, frame))

	def draw(self, surface, camera, tick):
		""" Draws this animation.

		This method draws this animation on the given surface.
		The animation will only be drawn once.

		Args:
			surface: The surface to draw on.
			camera: The position of the camera.
			tick: The current tick of the game.

		Returns:
			True if the animation was drawn. False otherwise.
		"""
		if self._first_tick < 0:
			self._first_tick = tick
		tick -= self._first_tick
		drawn = False
		for part in self._animation:
			if tick > part[0]:
				tick -= part[0]
			else:
				surface.blit(part[1], (self._pos[0] - camera[0], self._pos[1] - camera[1]))
				drawn = True
				break
		return drawn
