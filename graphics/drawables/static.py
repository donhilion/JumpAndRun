import pygame

class Static(object):

	def __init__(self, picture_manager, frame, repeat=False, width=0, height=0):
		picture = picture_manager.loaded[frame[0]]
		rect = pygame.Rect(float(frame[1]), float(frame[2]),
			float(frame[3]) - float(frame[1]),
			float(frame[4]) - float(frame[2]))
		self.image = picture.subsurface(rect)


	def draw(self, surface, x, y):
		surface.blit(self.image, x, y)