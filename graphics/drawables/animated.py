import pygame

class Animated(object):
	'''
	'''

	def __init__(self, picture_manager, frame_list, animation, two_sided=False):
		frames = {}
		self.animation = []
		self.mirrored = None
		if two_sided:
			self.mirrored = []
		self.max_frame_count = 0

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
			self.max_frame_count += count
			self.animation.append((count, frame))
			if two_sided:
				self.mirrored.append((count, pygame.transform.flip(frame, True, False)))

	def draw(self, surface, x, y, count, flipped=False):
		count %= self.max_frame_count
		list = self.animation
		if flipped and self.mirrored is not None:
			list = self.mirrored
		for part in list:
			if count > part[0]:
				count -= part[0]
			else:
				surface.blit(part[1], (x, y))
				break
