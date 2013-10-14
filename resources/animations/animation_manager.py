import xml.dom.minidom as dom
import logging
from thread import start_new_thread, allocate_lock

from resources.ressource_manager import RessourceWrapper

class AnimationManager(object):
	'''
	'''

	MANAGER = None

	def __init__(self):
		self.lock = allocate_lock()
		self.animations = {}
		AnimationManager.MANAGER = self

	def load_animation(self, name):
		wrapper = RessourceWrapper(name = name)
		start_new_thread(self.load_animation_asynchroniously, (wrapper,))
		return wrapper

	def load_animation_asynchroniously(self, wrapper):
		try:
			logging.debug("Begin loading animation " + wrapper.name)
			tree = dom.parse("resources/animations/" + wrapper.name)
			frames = {}
			animations = {}

			for first in tree.firstChild.childNodes:
				if first.nodeName == "frames":
					for frame in first.childNodes:
						name = None
						picture = None
						left = None
						top = None
						right = None
						bottom = None
						for entry in frame.childNodes:
							if entry.nodeName == "name":
								name = entry.firstChild.data.strip()
							elif entry.nodeName == "picture":
								picture = entry.firstChild.data.strip()
							elif entry.nodeName == "left":
								left = entry.firstChild.data.strip()
							elif entry.nodeName == "top":
								top = entry.firstChild.data.strip()
							elif entry.nodeName == "right":
								right = entry.firstChild.data.strip()
							elif entry.nodeName == "bottom":
								bottom = entry.firstChild.data.strip()
						if name is not None and picture is not None and \
								left is not None and top is not None and \
								right is not None and bottom is not None:
							frames[name] = (picture, left, top, right, bottom)
				elif first.nodeName == "animations":
					for animation in first.childNodes:
						name = None
						frames_of_animation = []
						for part in animation.childNodes:
							if part.nodeName == "name":
								name = part.firstChild.data.strip()
							else:
								frame = None
								duration = None
								for entry in part.childNodes:
									if entry.nodeName == "frame":
										frame = entry.firstChild.data.strip()
									elif entry.nodeName == "duration":
										duration = entry.firstChild.data.strip()
								if frame is not None and duration is not None:
									frames_of_animation.append((frame, duration))
						if name is not None:
							animations[name] = frames_of_animation

			self.lock.acquire()
			self.animations[wrapper.name] = (frames, animations)
			self.lock.release()
			logging.debug("End loading picture " + wrapper.name)
			wrapper.status = RessourceWrapper.LOADED
		except Exception as ex:
			logging.error("Error while loading animation " + \
				wrapper.name)
			logging.error(ex)
			wrapper.status = RessourceWrapper.FAILED
			try:
				self.lock.release()
			except Exception as ex:
				logging.error(ex)