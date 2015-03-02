#!/usr/bin/python
# coding=utf-8
# @author: Tadas Krisciunas

import sqlite3 as lite
from collections import defaultdict
import pprint as p
import pickle

import morphological_tagger as mt
import sentence_tokenizer as st
import BaseMethods

class Patterns(BaseMethods.BaseMethods):
	""" A class that extracts, saves, loads and otherwise deals with
		sentence patterns. Patterns are the following:

			pattern = [('POS tag', 'detailed info'), ...]

		They can later be used to learn to generate grammatically correct
		sentences using Markov chains.
	"""

	patterns = []
	current  = 0

	def __init__(self, file = ''):
		""" If filename is non-empty, loads a pattern list from it. """

		if file != '':
			self.load(file)

	def save(self, file):
		"""
		Saves patterns to a pickle
		"""

		pickle.dump(self.patterns, file)

	def load(self, file):
		"""
		Loads patterns from a pickle.
		"""

		self.patterns = pickle.load(file)

	def get_patterns(self, database, table, text_column, limit = 100000, verbose = True):
		"""
		Returns POS patterns in the given database (where text is assumed to be in 'text_column').
		The form is a dictionary, where keys are patterns (| separated POS tags), and values are
		the counts of the sentence patterns in the database.
		"""

		# Get Lithuanian poems from the database
		con = lite.connect(database)
		cur = con.cursor()
		poems = [entry[0] for entry in cur.execute("SELECT " + text_column + " FROM " + table + ' LIMIT ' + str(limit))]

		# Now, get the most common sentence POS patterns in the database
		for poem in poems:
			tokenizer = st.SentenceTokenizer()
			sentences = tokenizer.segment_text(poem.replace('\n', ' '))

			for sen in sentences:
				
				sentence = self.prepare_sentence(sen)

				if verbose:
					print ' '.join(sentence)
				
				pos_tags = mt.get_lemmas(' '.join(sentence).encode('utf-8'))

				# Get the pattern of the POS tags. 
				pattern = []

				for tag in pos_tags:
					
					if tag[2] != '':
						pattern.append( (tag[2], tag[4]) )
					
					else:
						pattern.append( (None, None) )

					# Check if there are no punctuation marks after the word in the original sentence.
					# If there are, add them to the structure.
					
					try:
						i = sentence.index(tag[0])
					
					except ValueError:
						print '(!) There was an error, '+tag[0]+' that should have been in a sentence was not in it. (!)'
						i = len(sen)

					if i + 1 < len(sen):

						if sen[i + 1] in self.punctuation:
							pattern.append( (sen[i + 1], sen[i + 1]) )

				self.patterns.append(pattern)

				if verbose:
					print pattern

	def next_for_markov(self):
		""" Returns a list of detailed information ready to be ingested by the Markov class.
			Returns patterns sentence by sentence.
			Iterate until you get 'None' to go through all patterns.
		"""

		i = self.current
		self.current += 1

		if self.current > len(self.patterns):
			return None

		else:
			return [ tag[1] for tag in self.patterns[tmp] ]

###### Code for running ###############################
 
if __name__ == "__main__":
	p = Patterns()
	p.get_patterns('../delfi.lt/delfi.db', 'articles', 'main_text', limit = 500)
	p.save('delfi_patterns.pkl')