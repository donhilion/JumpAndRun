import pygame

__author__ = 'Donhilion'


class Animated(object):
	""" The animated class.

	An instance of this class represents an animated object.

	Attributes:
		_animations: The list of pictures of this animation with the duration.
		_mirrored: If the animated object is two sided this is a list of mirrored pictures similar to _animations.
		_max_frame_count: Contains the complete number of frames for one animation cycle.
	"""

	def __init__(self, picture_manager, frame_list, animation, two_sided=False):
		""" Generates a new instance of this class.

		Generates a new instance of this class and sets the field information.

		Args:
			picture_manager: The instance of the picture manager to use.
			frame_list: The list of frames.
			animation: The animation dictionary.
			two_sided: Determines if the animated object has two sides.
		"""
		frames = {}
		self._animation = []
		self._mirrored = None
		if two_sided:
			self._mirrored = []
		self._max_frame_count = 0

		for frame_key in frame_list:
			frame = frame_list[frame_key]
			picture = picture_manager.loaded[frame["picture"]]
			rect = pygame.Rect(float(frame["left"]), float(frame["top"]),
							   float(frame["right"]) - float(frame["left"]),
							   float(frame["bottom"]) - float(frame["top"]))
			part = picture.subsurface(rect)
			frames[frame_key] = part

		for part in animation["parts"]:
			frame = frames[part["frame"]]
			count = int(part["duration"])
			self._max_frame_count += count
			self._animation.append((count, frame))
			if two_sided:
				self._mirrored.append((count, pygame.transform.flip(frame, True, False)))

	def draw(self, surface, x, y, count, flipped=False):
		""" Draws this animated object.

		This method draws the animated object on the given surface.

		Args:
			surface: The surface to draw on.
			x: The x coordinate.
			y: The y coordinate.
			count: The current tick of the game.
		"""
		count %= self._max_frame_count
		animation_list = self._animation
		if flipped and self._mirrored is not None:
			animation_list = self._mirrored
		for part in animation_list:
			if count > part[0]:
				count -= part[0]
			else:
				surface.blit(part[1], (x, y))
				break
