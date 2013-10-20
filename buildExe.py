import operator
import sys
import pygame2exe
import os
import shutil

__author__ = 'Donhilion'

DIST_FOLDER = "dist"
RESOURCES_FOLDER = "resources"

ANIMATION_FOLDER = "animations"
ANIMATION_FILES = ("animations.json",)

LEVEL_FOLDER = "levels"
LEVEL_FILES = ("level0.json",)

PICTURE_FOLDER = "pictures"
PICTURE_FILES = (
"background.png", "Coin.png", "goal.png", "grass.png", "Heart.png", "Hero.png", "HeroDie.png", "menuBackground.png",
"monster.png", "platform.png", "sparksis.png")

SETTING_FOLDER = "settings"
SETTING_FILES = ("graphics.json", "pictures.json", "sounds.json")

SOUND_FOLDER = "sounds"
SOUND_FILES = ("coin.wav", "hit.wav", "jump.wav", "music0.wav", "step.wav")

if __name__ == '__main__':
	if operator.lt(len(sys.argv), 2):
		sys.argv.append('py2exe')
	pygame2exe.BuildExe().run()
	if not os.path.exists(DIST_FOLDER + os.path.sep + RESOURCES_FOLDER):
		os.makedirs(DIST_FOLDER + os.path.sep + RESOURCES_FOLDER)

	if not os.path.exists(DIST_FOLDER + os.path.sep + RESOURCES_FOLDER + os.path.sep + ANIMATION_FOLDER):
		os.makedirs(DIST_FOLDER + os.path.sep + RESOURCES_FOLDER + os.path.sep + ANIMATION_FOLDER)
	for animation_file in ANIMATION_FILES:
		shutil.copy(RESOURCES_FOLDER + os.path.sep + ANIMATION_FOLDER + os.path.sep + animation_file,
					DIST_FOLDER + os.path.sep + RESOURCES_FOLDER + os.path.sep + ANIMATION_FOLDER)

	if not os.path.exists(DIST_FOLDER + os.path.sep + RESOURCES_FOLDER + os.path.sep + LEVEL_FOLDER):
		os.makedirs(DIST_FOLDER + os.path.sep + RESOURCES_FOLDER + os.path.sep + LEVEL_FOLDER)
	for level_file in LEVEL_FILES:
		shutil.copy(RESOURCES_FOLDER + os.path.sep + LEVEL_FOLDER + os.path.sep + level_file,
					DIST_FOLDER + os.path.sep + RESOURCES_FOLDER + os.path.sep + LEVEL_FOLDER)

	if not os.path.exists(DIST_FOLDER + os.path.sep + RESOURCES_FOLDER + os.path.sep + PICTURE_FOLDER):
		os.makedirs(DIST_FOLDER + os.path.sep + RESOURCES_FOLDER + os.path.sep + PICTURE_FOLDER)
	for picture_file in PICTURE_FILES:
		shutil.copy(RESOURCES_FOLDER + os.path.sep + PICTURE_FOLDER + os.path.sep + picture_file,
					DIST_FOLDER + os.path.sep + RESOURCES_FOLDER + os.path.sep + PICTURE_FOLDER)

	if not os.path.exists(DIST_FOLDER + os.path.sep + RESOURCES_FOLDER + os.path.sep + SETTING_FOLDER):
		os.makedirs(DIST_FOLDER + os.path.sep + RESOURCES_FOLDER + os.path.sep + SETTING_FOLDER)
	for setting_file in SETTING_FILES:
		shutil.copy(RESOURCES_FOLDER + os.path.sep + SETTING_FOLDER + os.path.sep + setting_file,
					DIST_FOLDER + os.path.sep + RESOURCES_FOLDER + os.path.sep + SETTING_FOLDER)

	if not os.path.exists(DIST_FOLDER + os.path.sep + RESOURCES_FOLDER + os.path.sep + SOUND_FOLDER):
		os.makedirs(DIST_FOLDER + os.path.sep + RESOURCES_FOLDER + os.path.sep + SOUND_FOLDER)
	for sound_file in SOUND_FILES:
		shutil.copy(RESOURCES_FOLDER + os.path.sep + SOUND_FOLDER + os.path.sep + sound_file,
					DIST_FOLDER + os.path.sep + RESOURCES_FOLDER + os.path.sep + SOUND_FOLDER)