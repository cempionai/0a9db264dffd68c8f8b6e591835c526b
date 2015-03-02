#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libraries import sentence_tokenizer as st
from libraries import morphological_tagger as tag
from libraries import BaseMethods
import fileinput
import random
import sys
import re
import os
import time
import sqlite3 as lite
import pickle
import numpy as np
import scipy.spatial.distance
import codecs
from collections import defaultdict
import word2vec

class Grammar(BaseMethods.BaseMethods):
  """ A class implementing a Markov-chain-based text generator. """

  # Global word2vec model
  model = []

  def __init__(self, word2vecBinFile = ''):
    """ If 'word2vecBinFile' is non-empty, loads word2vec binary data """
    
    if word2vecBinFile != '':
      self.loadVectorData(self, word2vecBinFile)
  
  def unique(self, seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

  def getSameGrammar(self, word, database, table, column, wordColumn):
    """ Returns POS of the given word, searching among entries in a given database.
        The format of database is assumed to be such that the 'column' contains all POS of words, for example
        "vksm., teig., nesngr., tiesiog. n., būt. k. l., vns., 3 asm."
        (database morph.db keeps it in column ypat)
        Note that the actual part of speech is included in this column, so there is no need to specify it separately.
    """
    
    # Ensure database exists
    # ~ if os.path.isfile(database):
      # ~ print "ERROR: Database " + database + " does not exist."
      # ~ return
    
    # Get POS tags of a supplied word
    pos_tags = tag.get_lemmas(word.encode("utf-8"))[0]
    # ~ print pos_tags
    
    # Connect to a database
    con = lite.connect(database)
    with con:    
      cur = con.cursor()
      # Get all words with same POS
      cur.execute("SELECT " + wordColumn + " FROM " + table + " WHERE " + column + "=?", (pos_tags.morphDetails,) )
      rows = cur.fetchall()
      # Convert them to unicode
      possible_words = [unicode(row[0]) for row in rows]  # since query returns only one column, it must be the first
      
    return self.unique(possible_words)
  
  def loadVectorData(self, vectorBinPath):
    """ Loads a binary vector model from a given file"""
    
    # Ensure vector binary file exists
    if not os.path.isfile(os.path.abspath(vectorBinPath)):
      print "ERROR: word2vec binary data file " + vectorBinPath + " does not exist."
    # Load the file
    self.model = word2vec.load(vectorBinPath);
  
  def createVectorDataFromText(self, text, vectorBinPath, intermediateFile = ''):
    """ Writes given text to file, prepares a binary vector file and loads it"""
    
    # Sanitize input
    text = BaseMethods.BaseMethods.prepare_text(text)
    text = text.replace(' ', '\n')
    
    # Create file for auxiliary output
    if intermediateFile == '':
      intermediateFile = "words2vecInputData" + str(time.time())
    
    # Write supplied text to auxiliary output file
    with codecs.open(intermediateFile, 'w', encoding='utf8') as f:
      f.write(text)
      f.close()
    
    # Create vector data from auxiliary output file
    self.createVectorDataFromFile(intermediateFile, vectorBinPath)
  
  def createVectorDataFromFile(self, textCorpus, vectorBinPath):
    """ Prepares a binary vector model from a given file"""
    
    # Ensure both files exist
    if not os.path.isfile(os.path.abspath(textCorpus)):
      print "ERROR: Given text data file " + textCorpus + " does not exist."
      raise IOError("ERROR: Given text data file " + textCorpus + " does not exist.")
    # ~ if not os.path.isfile(os.path.abspath(vectorBinPath)):
      # ~ print "ERROR: word2vec binary data file " + vectorBinPath + " does not exist."
      # ~ raise IOError("ERROR: word2vec binary data file " + vectorBinPath + " does not exist.")

    word2vec.word2vec(textCorpus, vectorBinPath, size=100, verbose=True)
    
  def wordToVector(self, word):
    """ Returns the tuple. First element is a Boolean variable indicating a success (True) or failure (False).
    Second element of tuple is word2vec vector of a given word.
    Expected cause of failure is word absence from the current vocabulary.
    
    (!) This function breaks the encapsulation of Grammar class."""
        
    try:
      vector = self.model[word]
      return (True, vector)
    except:
      pass
    return (False, [])
    
  def getMostSimilar(self, mainWord, candidates = [], getSimilarityStatistics = False):
    """ Returns the list of words from 'candidates', sorted in the order of similarity to a particular word ('mainWord').
        If candidates is an empty list, whole current words2vec dictionary is used.
        If getSimilarityStatistics is true, a tuple is returned.
        First element is a closeness (similarity) parameter, second is similar word itself.
    """
    mainWord = mainWord.encode("utf-8")
    
    if candidates == []:
      # No list of words specified, use word2vec functions to get list of words from entire dictionary
      indexes, metrics = self.model.cosine(str(mainWord))
      wordList = self.model.generate_response(indexes, metrics).tolist()
    else:
      # Get vector of a main word
      wordVec = self.wordToVector(mainWord)[1]
      
      cosDist = []
      for cand in candidates:
        # Get vector for each candidate
        candidateVec = self.wordToVector(cand.encode("utf-8"))[1]
        # If both words (mainWord and candidate) are in dictionary, compute their cosine similarity
        if candidateVec != [] and wordVec != []:
          # Note that spatial.distance.cosine return 1 - cos(u,w) for vectors u, w, thus it is accordingly corrected
          cosDist.append( (1 - scipy.spatial.distance.cosine(wordVec, candidateVec), cand) )
    
    # Words are sorted according their similarity (more similar first)
    cosDist.sort(key = lambda tup: tup[0], reverse=True)
    
    # Return only words or both words and similarity cosine
    if getSimilarityStatistics:
      return cosDist
    else:
      return [word for (dist, word) in cosDist]
  

if __name__ == '__main__':
  # Example one: get all grammatically similar words to "karas" and find the most similar of them
  
  # Initialise
  g = Grammar()
  zodis = "karas"

  # Get grammatically equivalent words from database
  structures =  Grammar.getSameGrammar(g, zodis, "morph.db", "morph", "ypat", "zodis")
  
  # Load words2vec binary file (trained on lithuanian words)
  Grammar.loadVectorData(g, "lit_vec.bin")
  
  # Get most similar to "karas" words from 'structures'
  sim = Grammar.getMostSimilar(g, "karas", structures)

  for s in sim[:20]:
    print s 
