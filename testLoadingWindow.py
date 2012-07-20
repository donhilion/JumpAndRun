import pygame
from graphics.loading_window import LoadingWindow
from graphics.window import Window

pygame.init()
window = LoadingWindow()
window.load()

window = Window()
window.start()
