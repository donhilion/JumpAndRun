'''
Created on 10.07.2012

@author: Donhilion
'''

class RessourceManager(object):
	''' A manager for resources.

	This manager loads resources/files asynchroniously.
	'''
	
	def __init__(self):
		pass

class RessourceWrapper(object):
	''' A wrapper for resources.

	This wrapper contains informations about the status of the ressource
	including if the ressource is loaded, status messages and the ressource
	itself.

	Attributes:
		status: The current status of this ressource. Could be LOADED, 
			FAILED or PENDING
		messages: A list of messages. This is a list of strings.
		name: The name of this ressource. This is a string.
		data: Contains the data of this ressource when the status is 'loaded'.
	'''

	PENDING, LOADED, FAILED = range(3)

	def __init__(self, name=""):
		self.status = RessourceWrapper.PENDING
		self.messages = []
		self.name = name
		self.data = None	