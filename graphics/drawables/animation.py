import pygame

__author__ = 'donhilion'

class Animation(object):

	def __init__(self, picture_manager, frame_list, animation, pos = (0,0)):
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
