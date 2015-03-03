#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libraries import common_patterns as cp
from libraries import morphological_tagger as tag
from libraries import grammar as gram
from libraries import BaseMethods as base
from collections import namedtuple
import fileinput
import random
import locale
import sys
import re
import sqlite3 as lite
import pickle

POS = namedtuple('POS', ['word', 'success', 'partOfSpeech', 'infinitive', 'morphDetails'])

def create_database(filename):
	""" Creates a database to save words in. Returns a connection to it. """
	con = lite.connect(filename)
	cur = con.cursor()
	cur.execute('CREATE TABLE lexicon (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT, success INTEGER, \
									   partOfSpeech TEXT, infinitive TEXT, morphDetails TEXT)')
	con.commit()

	return con

def get_from_database(filename):
	""" Gets POS-tagged words from a database. Returns a list of POS-tuples"""

	con = lite.connect(filename)
	cur = con.cursor()
	res = cur.execute('SELECT word, success, partOfSpeech, infinitive, morphDetails FROM lexicon')
	tuples = []

	for row in res:
		tuples.append( POS(row[0], row[1], row[2], row[3], row[4]) )

	return tuples

if __name__ == '__main__':
	database = [t.word for t in get_from_database('lexicon.db')]
	words = set(base.BaseMethods.prepare_text(open('text.txt', 'r').read().decode('utf8')).split())
	con = lite.connect('lexicon.db')
	cur = con.cursor()

	for word in words:

		if not word in database:
			try:
				lemmas = tag.get_lemmas(word)[0]
				print lemmas, '\n'
				cur.execute('INSERT INTO lexicon (word, success, partOfSpeech, infinitive, morphDetails) \
							 VALUES (?, ?, ?, ?, ?)', 
							 lemmas )
				con.commit()

			except IndexError:
				pass
	