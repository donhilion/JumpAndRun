import pygame

__author__ = 'Donhilion'

pygame.mixer.init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
#pygame.init()                      #initialize pygame
#pygame.mixer.init()
#sound = pygame.mixer.Sound("resources/sounds/test.wav")
#sound.play()
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.load("test.ogg")
#pygame.mixer.music.load("resources/sounds/step.wav")
pygame.mixer.music.play()
#channel.play()

while pygame.mixer.music.get_busy():
	pygame.time.Clock().tick(100)
