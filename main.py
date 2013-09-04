'''
Created on 10.07.2012

@author: Donhilion
'''

import logging
import pygame
from graphics.loading_window import LoadingWindow
from graphics.window import Window


# TODOs
# Logger
# Ressourcen Manager
# Localisation
# Graphics
# Logic

if __name__ == '__main__':
	pygame.init()
	window = LoadingWindow()
	window.load()

	window = Window()
	window.start()