#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libraries import sentence_tokenizer as st
from libraries import morphological_tagger as tag
from libraries import BaseMethods
import fileinput
import random
import sys
import re
import sqlite3 as lite
import pickle
from collections import defaultdict

class Markov(BaseMethods.BaseMethods):
  """ A class implementing a Markov-chain-based text generator. """

  depth = 1
  model = defaultdict(lambda: defaultdict(lambda: 0))

  def __init__(self, depth = 1, text = ''):
    """ If 'text' is non-empty, learns a Markov model from it. """

    self.depth = depth

    if text != '':
      self.update_markov_model(self.prepare_text(text).split())

  def update_markov_model(self, training_sample):
    """ Returns a dictionary where
          - keys are words in the text
          - values are dictionaries of words that follow after them,
            with their counts as values
        
        (!) 'training_sample' needs to be a list of words, not a string
    """
    
    # Prepare the word list for learning: join 'depth' consecutive items together
    # We will save the result in 'words', which will later serve for training.
    words = []

    for i in range(len(training_sample) / self.depth):
      current = ''
      j = self.depth * i

      for k in range(self.depth):
        current += training_sample[j + k] + ' '

      words.append(current[:-1])

    # Now, go for training!
    for i in range(len(words) - 1):
      
      if words[i] not in self.model:               
        # If word is not in dicitonary, add the one following it with occurence 1
        self.model[ words[i] ][ words[i+1] ] = 1
      
      else:
        # Otherwise, go on building our Markov chain!
        if words[i+1] not in self.model[ words[i] ]:    
          self.model[ words[i] ][ words[i+1] ] = 1 
        
        else:
          self.model[ words[i] ][ words[i+1] ] = 1 + self.model[words[i]][words[i+1]]

    return self.model

  def save(self, file):
    """ Saves the Markov model to a pickle. """

    pickle.dump(self.model, file)

  def load(self, file):
    """ Loads the Markov model from a pickle. """

    self.model = pickle.load(file)

  def next_word(self, word):
    """ Randomly returns the word going after 'word'.
        The probability of the returned word matches the
        probability of it appearing after 'word' in analyzed
        corpus.
    """

    if word not in self.model:
      return None

    else:

      # Prepare to mirror the probabilities of words
      # following 'word' in real corpus text
      new_probs = {}
      summa = 0

      for (k, v) in self.model[word].iteritems():
        new_probs[k] = v + summa
        summa = new_probs[k]

      # Now, return one of the words randomly. Note that
      # because of what we've done above, the probability
      # of this function returning X is the same as X appearing
      # after 'word' in corpus text.
      rnd = random.random() * summa
      
      for (k, v) in new_probs.iteritems():
        
        if rnd < v:
          return k

  def randomize_text(self, seed = '', length = 10):
    """ Randomizes text of 'length' starting with 'seed'
        using the Markov model that is learned. 
        Returns a list(!) of words.
    """

    if seed == '':
      seed = random.choice(self.model.keys())

    seed = seed.lower().strip()
    text = [seed]

    if seed not in self.model:
      return text
    
    else:

      for i in range(length):
        text.append( self.next_word(seed) )
        seed = text[ len(text) - 1 ]

    return text

if __name__ == '__main__':

  # First example. A Markov chain with depth 1, created sentence by sentence
  """markov = Markov(depth = 1)
  con = lite.connect('../delfi.lt/delfi.db')
  cur = con.cursor()
  articles = '\n'.join([s[0] for s in cur.execute('SELECT main_text FROM articles').fetchall()])
  sentences = st.SentenceTokenizer().segment_text(articles)

  for sentence in sentences:
    markov.update_markov_model(Markov.prepare_sentence(sentence))"""

  # Second example. A Markov chain with depth 2, from a text dump
  markov2 = Markov(
                    depth = 2, 
                    text = open('eiles.txt').read().decode('utf8')
                  )
  
  # Now, just some command-line fun.
  seed = ''

  while seed != 'EXIT':
    seed = raw_input('Įveskite pradinį žodį (EXIT išeiti):  ')
    print ' '.join(markov2.randomize_text(seed, 50))