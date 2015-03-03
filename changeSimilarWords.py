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

def getSim(zodis):
  structures =  gram.Grammar.getSameGrammar(g, zodis, "morph.db", "morph", "ypat", "zodis")
  return gram.Grammar.getMostSimilar(g, zodis, structures)

g = gram.Grammar()
b = base.BaseMethods()
gram.Grammar.loadVectorData(g, "lit_vec.bin")

def changeWords(text):
  # Load text and get its POS
  text = b.prepare_text(text)
  lemmas = tag.get_lemmas(text.encode("utf-8"))
  
  i = 0
  result = []
  
  for l in lemmas:
    # Write percentage of progress
<<<<<<< HEAD
    # sys.stdout.write("\r%.0f %%" % round( (100.0 * i / len(lemmas)) ) )
    # sys.stdout.flush()
=======
    sys.stdout.write("\r%.0f %%" % round( (100.0 * i / len(lemmas)) ) )
    sys.stdout.flush()
>>>>>>> e8fc5f1fe6fbe076df756d081186dd75356228c9
    i += 1
    
    # Inlucde only the following partOfSpeech
    if (l.partOfSpeech == 'dkt' or  l.partOfSpeech == 'vksm' or l.partOfSpeech == 'bdv' or l.partOfSpeech == 'prv' or l.partOfSpeech == 'bendr'):
      # Get at most ten most similar candidates
      similar = getSim(l.word)[:10]
      
      if similar == []:
        result.append( l.word )
      else:
        result.append( random.choice(similar) )     # Choose randomly one of them
    else:
      result.append( l.word )
      
<<<<<<< HEAD
  # print n
=======
  print "100 %"
>>>>>>> e8fc5f1fe6fbe076df756d081186dd75356228c9
  result = [r.encode("utf-8") for r in result]
  return result
  
def exchange(text, substitutes):
  # Split text into words and non-words
<<<<<<< HEAD
  text = text.encode('utf-8')
  splitted = re.split(r'([A-Za-ząčęėįšųūžĄČĘĖĮŠŲŪŽ]+)', text, flags=re.UNICODE)

=======
  text = text.encode("utf-8")
  splitted = re.split(r'([A-Za-ząčęėįšųūžĄČĘĖĮŠŲŪŽ]+)', text, flags=re.UNICODE)
  
>>>>>>> e8fc5f1fe6fbe076df756d081186dd75356228c9
  t = 0
  for i in range(len(splitted)):
    # Check if current split is actual word or non-word
    if re.search(r'[A-Za-ząčęėįšųūžĄČĘĖĮŠŲŪŽ]+', splitted[i], flags=re.UNICODE) != None:
<<<<<<< HEAD

      splitted[i] = splitted[i].decode('utf-8')

      # If the original was capitalised, capitalise the substitution, otherwise write in lowercase
      if splitted[i][0].isupper():
        splitted[i] = (substitutes[t].capitalize()).decode('utf-8')
      else:
        splitted[i] = (substitutes[t].lower()).decode('utf-8')
=======
      print splitted[i], substitutes[t]
      # If the original was capitalised, capitalise the substitution, otherwise write in lowercase
      if splitted[i][0].isupper():
        splitted[i] = substitutes[t].capitalize()
      else:
        splitted[i] = substitutes[t].lower()
>>>>>>> e8fc5f1fe6fbe076df756d081186dd75356228c9
      t += 1
  
  # Return substituted text
  return "".join(splitted)

def getRandomPoem():
<<<<<<< HEAD
  con = lite.connect('tekstai.lt/tekstai.db')
=======
  con = lite.connect('tekstai.db')
>>>>>>> e8fc5f1fe6fbe076df756d081186dd75356228c9
  with con:    
    cur = con.cursor()    
    cur.execute("SELECT Article FROM Tekstai")
    rows = cur.fetchall()
    rows = random.choice([ unicode(u[0]) for u in rows ])
    return "".join(rows)

<<<<<<< HEAD
maironis = u"""Gal poezijos naują pasemčiau šaltinį"""
=======
maironis = u"""Sako Džordžas Vašingtonas auginęs kanapes
ir skyręs jų rūšis pagal spalvą ir kvapą.
Tad už nuopelną šitą
vadovėliuose aprašytą
jo portretą ant žalio banknoto nutapė.
"""
>>>>>>> e8fc5f1fe6fbe076df756d081186dd75356228c9

putinas = u"""Vis dėlto Ramučio žodžiai privertė jį susimąstyti. Prieš jį atsistojo nauja dviejų literatūrų — dieviškosios ir žmogiškosios — problema. Jis staiga suvokė, kad yra Dievo ir pasaulio poetai. Bet tik vėliau svarstydamas tą problemą jis išsiaiškino, kad Dievo poetai tai yra šventieji, turį ypatingą malonę įkvėpimo ekstazėje regėti Dievo tiesą ir grožį, dėl to galį išsižadėti pasaulio ir gyvenimo. Pasaulio gi poetai mato grožį tiktai jo atsispindėjime įvairiuose pasaulio daiktuose ir reiškiniuose. Jų kūryba yra vingiuota ir aistringa kaip žmogaus širdis. Dėl to ji taip plačiai prieinama ir branginama. Pirmųjų poezija yra apreiškimas, garbinimas ir malda, antrųjų — ieškojimas, kentėjimas, kūryba.

To pasivaikščiojimo metu Vasaris nespėjo nagrinėti klausimo, kuriai gi poetų kategorijai jis pats norėtų priklausyti. Bet ir be nagrinėjimo jo viso dvasinio gyvenimo patyrimas, visi jo palinkimai sakė jam, kad jo kūrybos kelias eina per žmogaus širdį ir pasaulį ir kad maldingosios poezijos jam niekados nėra lemta sukurti."""

# ~ zodziai = changeWords(putinas)
<<<<<<< HEAD
# zodziai = [u'vis', u'd\u0117lto', u'ramu\u010dio', u'daiktai', u'suklydo', u'j\u012f', u'i\u0161siskirti', u'prie\u0161', u'j\u012f', u'atsiduso', u'svarbi', u'dviej\u0173', u'literat\u016br\u0173', u'dievi\u0161kosios', 'ir', u'n\u0117\u0161\u010diosios', u'reklama', 'jis', u'v\u0117l', u'suprato', 'kad', u'veikia', u'dangaus', 'ir', u'\u017eemyno', u'gyvul\u0117liai', 'bet', u'o', u'\u012fkyriau', 'svarstydamas', u't\u0105', u'nuomon\u0119', 'jis', u'pasi\u0161alino', 'kad', u'pragaro', u'vargai', 'tai', u'tampa', u's\u0117brai', u'tur\u012f', u'grie\u017et\u0105', u'dr\u0105s\u0105', u'sarkazmo', u'gerkl\u0117je', u'nubusti', u'dievo', u'g\u0117d\u0105', 'ir', u'mel\u0105', u'd\u0117l to', u'gal\u012f', u'linksmintis', u'karaliaus', 'ir', u'ry\u017eto', u'plaukimo', 'gi', u'poetai', u'supranta', u'niek\u0105', 'tiktai', 'jo', u'atsispind\u0117jime', u'juoduose', u'\u017eemyno', u'veidrod\u017eiuose', 'ir', u'rei\u0161kiniuose', u'j\u0173', u'prigimtis', u'yra', 'vingiuota', 'ir', u'kreiva', 'kaip', u'vaiko', u'\u0161irdis', u'd\u0117l to', 'ji', u'pana\u0161iai', u'tarsi', 'prieinama', 'ir', 'branginama', u'pirm\u0173j\u0173', u'merga', u'atitinka', u'aprei\u0161kimas', u'nervingumas', 'ir', u'd\u016b\u0161ia', u'antr\u0173j\u0173', u'gimimas', u'kent\u0117jimas', u'gamta', 'to', u'prisilietimo', u'aspektu', u'mira\u017eas', u'nepamat\u0117', u'suimti', u'sprendimo', 'kuriai', 'gi', u'vaikeli\u0173', u'reklamai', 'jis', 'pats', u'suprast\u0173', u'pagelb\u0117ti', 'bet ir', 'be', u'\u012fgijimo', 'jo', 'viso', u'politinio', u'ry\u017eto', u'faktorius', 'visi', 'jo', 'palinkimai', u'pa\u017eym\u0117jo', 'jam', 'kad', 'jo', u'harmonijos', u'br\u016bk\u0161nys', u'gr\u012f\u017eta', 'per', u'charakterio', u'\u017eem\u0119', 'ir', u'\u017evilgsn\u012f', 'ir', 'kad', 'maldingosios', u'poezijos', 'jam', u'visad', u'neb\u0117ra', 'lemta', u'i\u0161naudoti']


line = maironis #getRandomPoem()
print line
while True:  
  zodziai = changeWords(line)
  line = exchange(line, zodziai)
  print line
=======
zodziai = [u'vis', u'd\u0117lto', u'ramu\u010dio', u'daiktai', u'suklydo', u'j\u012f', u'i\u0161siskirti', u'prie\u0161', u'j\u012f', u'atsiduso', u'svarbi', u'dviej\u0173', u'literat\u016br\u0173', u'dievi\u0161kosios', 'ir', u'n\u0117\u0161\u010diosios', u'reklama', 'jis', u'v\u0117l', u'suprato', 'kad', u'veikia', u'dangaus', 'ir', u'\u017eemyno', u'gyvul\u0117liai', 'bet', u'o', u'\u012fkyriau', 'svarstydamas', u't\u0105', u'nuomon\u0119', 'jis', u'pasi\u0161alino', 'kad', u'pragaro', u'vargai', 'tai', u'tampa', u's\u0117brai', u'tur\u012f', u'grie\u017et\u0105', u'dr\u0105s\u0105', u'sarkazmo', u'gerkl\u0117je', u'nubusti', u'dievo', u'g\u0117d\u0105', 'ir', u'mel\u0105', u'd\u0117l to', u'gal\u012f', u'linksmintis', u'karaliaus', 'ir', u'ry\u017eto', u'plaukimo', 'gi', u'poetai', u'supranta', u'niek\u0105', 'tiktai', 'jo', u'atsispind\u0117jime', u'juoduose', u'\u017eemyno', u'veidrod\u017eiuose', 'ir', u'rei\u0161kiniuose', u'j\u0173', u'prigimtis', u'yra', 'vingiuota', 'ir', u'kreiva', 'kaip', u'vaiko', u'\u0161irdis', u'd\u0117l to', 'ji', u'pana\u0161iai', u'tarsi', 'prieinama', 'ir', 'branginama', u'pirm\u0173j\u0173', u'merga', u'atitinka', u'aprei\u0161kimas', u'nervingumas', 'ir', u'd\u016b\u0161ia', u'antr\u0173j\u0173', u'gimimas', u'kent\u0117jimas', u'gamta', 'to', u'prisilietimo', u'aspektu', u'mira\u017eas', u'nepamat\u0117', u'suimti', u'sprendimo', 'kuriai', 'gi', u'vaikeli\u0173', u'reklamai', 'jis', 'pats', u'suprast\u0173', u'pagelb\u0117ti', 'bet ir', 'be', u'\u012fgijimo', 'jo', 'viso', u'politinio', u'ry\u017eto', u'faktorius', 'visi', 'jo', 'palinkimai', u'pa\u017eym\u0117jo', 'jam', 'kad', 'jo', u'harmonijos', u'br\u016bk\u0161nys', u'gr\u012f\u017eta', 'per', u'charakterio', u'\u017eem\u0119', 'ir', u'\u017evilgsn\u012f', 'ir', 'kad', 'maldingosios', u'poezijos', 'jam', u'visad', u'neb\u0117ra', 'lemta', u'i\u0161naudoti']


poem = getRandomPoem()
zodziai = changeWords(poem)
zodziai = zodziai + [u"HUE" for x in range(1000)]
# ~ zodziai = [r.encode("utf-8") for r in zodziai]

print exchange(putinas, zodziai)
>>>>>>> e8fc5f1fe6fbe076df756d081186dd75356228c9
