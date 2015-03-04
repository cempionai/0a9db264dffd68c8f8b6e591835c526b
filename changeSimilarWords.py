#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libraries import common_patterns as cp
from libraries import morphological_tagger as tag
from libraries import grammar as gram
from libraries import BaseMethods as base
import fileinput
import random
import locale
import sys
import re
import sqlite3 as lite
import pickle

from collections import defaultdict

def getSim(zodis, averageVec, averageSize=7):
	structures =	gram.Grammar.getSameGrammar(g, zodis, '', "morph", "ypat", "zodis")
	return gram.Grammar.getMostSimilar(g, zodis, structures, averaging=averageVec, averageCount=averageSize)

g = gram.Grammar()
b = base.BaseMethods()
gram.Grammar.loadVectorData(g, "lit_vec.bin")
gram.Grammar.loadGrammarDatabase(g, "morph.db", "morph", "ypat", "zodis")


def changeWords(text, randomise = True, average = False, averageCount = 7):
	# Load text and get its POS
	text = b.prepare_text(text)
	lemmas = tag.get_lemmas(text.encode("utf-8"))
	
	i = 0
	result = []
	
	for l in lemmas:
		# Write percentage of progress
		# sys.stdout.write("\r%.0f %%" % round( (100.0 * i / len(lemmas)) ) )
		# sys.stdout.flush()
		i += 1
		
		# Inlucde only the following partOfSpeech
		if (l.partOfSpeech == 'dkt' or	l.partOfSpeech == 'vksm' or l.partOfSpeech == 'bdv' or l.partOfSpeech == 'prv' or l.partOfSpeech == 'bendr'):
			# Get at most ten most similar candidates
			similar = getSim(l.word, average, averageCount)[1:10]
			
			wordToWrite = l.word
			if similar != []:
				if randomise:
					wordToWrite = random.choice(similar)		 # Choose randomly one of them
				else:
					wordToWrite = similar[0]		 # Choose most similar
			
			# Average in the chosen word
			gram.Grammar.includeWordInAverage(g, wordToWrite);     
			result.append(wordToWrite)  
		else:
			result.append( l.word )
      
	result = [r.encode("utf-8") for r in result]
	return result
	
def exchange(text, substitutes):
	# Split text into words and non-words
	text = text.encode('utf-8')
	splitted = re.split(r'([A-Za-ząčęėįšųūžĄČĘĖĮŠŲŪŽ]+)', text, flags=re.UNICODE)

	t = 0
	for i in range(len(splitted)):
		# Check if current split is actual word or non-word
		if re.search(r'[A-Za-ząčęėįšųūžĄČĘĖĮŠŲŪŽ]+', splitted[i], flags=re.UNICODE) != None:

			splitted[i] = splitted[i].decode('utf-8')

			# If the original was capitalised, capitalise the substitution, otherwise write in lowercase
			if splitted[i][0].isupper():
				splitted[i] = (substitutes[t].capitalize()).decode('utf-8')
			else:
				splitted[i] = (substitutes[t].lower()).decode('utf-8')

			t += 1
	
	# Return substituted text
	return "".join(splitted)

def getRandomPoem():

	con = lite.connect('tekstai.lt/tekstai.db')

	with con:		
		cur = con.cursor()		
		cur.execute("SELECT Article FROM Tekstai")
		rows = cur.fetchall()
		rows = random.choice([ unicode(u[0]) for u in rows ])
		return "".join(rows)

def generateLines(line):
	print line

	while True:	
		zodziai = changeWords(line, True, average = True, averageCount = 7)
		line = exchange(line, zodziai)
		print line

maironis = u"""Gal poezijos naują pasemčiau šaltinį"""
# ~ maironis = u"""Kur bėga Šešupė, kur Nemunas teka, Tai mūsų tėvynė, graži Lietuva;"""
# ~ maironis = u"""Jau niekas tavęs taip giliai nemylės, Kaip tavo nuliūdęs poeta!"""
# ~ maironis = u"""Kur lygūs laukai, Snaudžia tamsūs miškai, Lietuviai barzdočiai dūmoja;"""
# ~ maironis = u"""To pasivaikščiojimo metu Vasaris nespėjo nagrinėti klausimo, kuriai gi poetų kategorijai jis pats norėtų priklausyti"""

# ~ generateFromPrevVectors(maironis)
generateLines(maironis)
