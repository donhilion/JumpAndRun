'''
Created on 10.07.2012

@author: Donhilion
'''

class RessourceManager(object):
	''' A manager for ressources.

	This manager loads ressources/files asynchronious.
	'''
	def __init__(self):
		pass

class RessourceWrapper(object):
	''' A wrapper for ressources.

	This wrapper contains informations about the status of the ressource
	including if the ressource is loaded, status messages and the ressource
	itself.

	Attributes:
		status: The current status of this ressource. Could be 'loaded', 
			'failed' or 'pending'
		messages: A list of messages. This is a list of strings.
		name: The name of this ressource. This is a string.
		data: Contains the data of this ressource when the status is 'loaded'.
	'''

	def __init__(self, name=""):
		#TODO: check input
		self.status = 0 #TODO: enum, set to pending
		self.messages = []
		self.name = name
		self.data = None	