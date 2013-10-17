from resources.pictures.picture_manager import PictureManager
from resources.settings.settings_manager import SettingsManager
from resources.resource_manager import ResourceWrapper

import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))

manager = PictureManager()
wrapper = manager.load_picture("background.png")

while wrapper.status == ResourceWrapper.PENDING:
	pass

print(wrapper.status)

manager = SettingsManager()
wrapper = manager.load_setting("graphics.json")

while wrapper.status == ResourceWrapper.PENDING:
	pass

print(wrapper.status)
print(wrapper.data["width"])
print(manager._settings["graphics.json"]["height"])
