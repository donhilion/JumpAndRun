import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((100, 100))

running = True

while(running):
	for event in pygame.event.get():
		if event.type == QUIT:
			print("The end")
			running = False
			break
		if event.type == KEYUP and event.key == K_ESCAPE:
			print("The end")
			running = False
			break
	#pygame.display.flip()