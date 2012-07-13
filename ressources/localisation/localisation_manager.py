'''
Created on 10.07.2012

@author: Donhilion
'''

class LocalisationManager(object):
	''' A manager for localised strings.

	This manager handels the localisation of strings.

	Attributes:
		language: The current language. This is a two letter code like "en".
	'''
	
	def __init__(self, language="en"):
		self.language = language

	def get_language(self):
		''' Returns the current language.

		Returns the language which is in use at the moment.
		The type of the returned value is a string witch two characters.
		Examples: "en", "de"

		Returns: the current language.
		'''
		return self.language

	def set_language(self, language):
		''' Sets the current language.

		Sets the language which should be used from now on.
		The new language must be a string with two characters.
		Examples: "en", "de"

		Args:
			language: The new language to use. This mus be a string with two
				characters.
		'''
		self.language = language
