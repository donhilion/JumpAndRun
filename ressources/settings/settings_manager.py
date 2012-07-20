import xml.dom.minidom as dom
import logging
from thread import start_new_thread

from ressources.ressource_manager import RessourceWrapper

class SettingsManager(object):
	'''
	'''

	MANAGER = None

	def __init__(self):
		self.settings = {}
		SettingsManager.MANAGER = self


	def load_setting(self, name):
		ressource_wrapper = RessourceWrapper(name = name)
		start_new_thread(self.load_setting_asynchroniously, (ressource_wrapper,))
		return ressource_wrapper
	
	def load_setting_asynchroniously(self, wrapper):
		try:
			tree = dom.parse("ressources/settings/" + wrapper.name)
			dictionary = {}
			for node in tree.firstChild.childNodes:
				if node.nodeName == "entry":
					key = None
					value = None
					for entry in node.childNodes: 
						if entry.nodeName == "key": 
							key = eval("%s('%s')" % (entry.getAttribute("type"), 
								entry.firstChild.data.strip()))
						elif entry.nodeName == "value": 
							value = eval("%s('%s')" % \
								(entry.getAttribute("type"), 
									entry.firstChild.data.strip()))
					if key is not None and value is not None:
						dictionary[key] = value
			self.settings[wrapper.name] = dictionary
			wrapper.data = dictionary
			wrapper.status = RessourceWrapper.LOADED
		except Exception as ex:
			logging.error("Error while loading picture " + wrapper.name)
			logging.error(ex)
			wrapper.status = RessourceWrapper.FAILED