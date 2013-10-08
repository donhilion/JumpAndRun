import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((500, 500))

bg_filename = "ressources/pictures/background.png"

bg = pygame.image.load(bg_filename).convert()

resized_bg = pygame.transform.scale(bg, (100,100))

running = True

while running:
	for event in pygame.event.get():
		if event.type == QUIT:
			print("The end")
			running = False
			break
		if event.type == KEYUP and event.key == K_ESCAPE:
			print("The end")
			running = False
			break
	for i in range(5):
		for j in range(5):
			screen.blit(resized_bg, (100*i,100*j))

	pygame.display.update()
	#pygame.display.flip()