#!/usr/bin/python
# coding=utf-8
# @author: Tadas Krisciunas

import re

class BaseMethods:
	""" A class implementing a few methods for inheriting classes.
		Should not be used directly, but of course can if need be.
	"""

	removed = [u'.', u',', u'-', u'!', u'?', u'–', u';', u':', 
	           u'—', u'(', u')', u'\n', u'„', u'“', u'"']

	punctuation = [u'.', u',', u'-', u'!', u'?', u'–', u';', u':', u'—', u'(', u')']

	@staticmethod
  	def prepare_sentence(sentence):
	   	""" Prepares sentence for later parsing. """

	   	new_sentence = []

		for word in sentence:
			word = word.lower()

			if len(word) > 1:

				for symbol in BaseMethods.removed:
					word = word.replace(symbol, '')

			if word != '':
				new_sentence.append(word)

		return new_sentence

  	@staticmethod
	def prepare_text(text):
	    """ Prepares simple text for parsing: 
	        leaves only lowercase words separated by single spaces. 
	    """

	    text = text.lower()
	    
	    for symbol in BaseMethods.removed:
	      text.replace(symbol, ' ')
	    
	    return re.sub(re.compile(r'\s+'), ' ', text)
