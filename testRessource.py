from ressources.pictures.picture_manager import PictureManager
from ressources.ressource_manager import RessourceWrapper

import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))

manager = PictureManager()
wrapper = manager.load_picture("background.png")

while wrapper.status == RessourceWrapper.PENDING:
	pass

print(wrapper.status)