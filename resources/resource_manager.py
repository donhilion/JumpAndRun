__author__ = 'Donhilion'


class ResourceManager(object):
	""" A manager for resources.

	This manager loads resources/files asynchronously.
	"""

	def __init__(self):
		pass


class ResourceWrapper(object):
	""" A wrapper for resources.

	This wrapper contains information about the status of the resource
	including if the resource is loaded, status messages and the resource
	itself.

	Attributes:
		status: The current status of this resource. Could be LOADED,
			FAILED or PENDING
		messages: A list of messages. This is a list of strings.
		name: The name of this resource. This is a string.
		data: Contains the data of this resource when the status is 'loaded'.
	"""

	# Values for the field status.
	PENDING, LOADED, FAILED = range(3)

	def __init__(self, name=""):
		self.status = ResourceWrapper.PENDING
		self.messages = []
		self.name = name
		self.data = None	