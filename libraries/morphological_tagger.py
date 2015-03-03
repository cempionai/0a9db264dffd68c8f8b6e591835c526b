#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
from bs4 import BeautifulSoup

from collections import namedtuple

POS = namedtuple('POS', ['word', 'success', 'partOfSpeech', 'infinitive', 'morphDetails'])

def get_lemmas(text):
  # ~ Įvestis: teksto eilutė. 
  # ~ get_lemmas grąžina sąrašą (list), kurio kiekvienas elementas yra įrašas (tuple), kurio:
  # ~ 0-inis elementas yra nagrinėjamas žodis (iš teksto eilutės), (pvz: negalėjo)
  # ~ 1 elementas yra Boolean tipo kintamasis, reiškiantis, ar pavyko nustatyti žodžio kalbos dalį
  # ~ 2 elementas yra kalbos dalis (jei ją pavyko nustatyti) (pvz: vksm)
  # ~ 3 elementas yra bendrinė žodžio forma (su pagrindinėmis formomis) (pvz: negalėti(-i,-ėjo) )
  # ~ 4 elementas yra žodžio ypatybės (pvz.: vksm., neig., nesngr., tiesiog. n., būt. k. l., dgs., 3 asm.)
  data = {
<<<<<<< HEAD
          "tekstas" : " " + text.encode('utf-8'),
=======
          "tekstas" : " " + text,
>>>>>>> e8fc5f1fe6fbe076df756d081186dd75356228c9
          "tipas" : "anotuoti",
          "pateikti" : "LM",
          "veiksmas" : "Rezultatas puslapyje"
         }
  # ~ Užkoduojame POST duomenis ir perduodame juos
  encoded_data = urllib.urlencode(data)
  
  # ~ Parse'iname HTML tekstą
  content = urllib2.urlopen("http://donelaitis.vdu.lt/main_helper.php?id=4&nr=7_2", encoded_data)
  soup = BeautifulSoup("".join(content.readlines()))

  # ~ Pasirenkame dalį, kuriame grąžinamas rezultatas
  annotator = soup.get_text()

  if not '<space' in annotator:
    annotator = ''

  # ~ Pataisome grąžintus tag'us, jog jie būtų korektiški HTML tag'ai
  annotator = annotator.replace("<word", "<word zodis")
  soup = BeautifulSoup(annotator)

  # ~ Išsirenkame reikiamas tag'o dalis
  result = [ (word.get('zodis'), u"nežinomas" not in word.get('type'),  "", word.get('lemma'), word.get('type')) for word in soup.find_all('word') ]
  rt = []
  # ~ Pataisome įrašą (tuple), jog elementas 2 būtų sutrumpinta kalbos dalis
  for r in result:
    if u"." in r[4] :
      rt.append( POS(r[0], r[1], r[4][:r[4].index(u".")], r[3], r[4]) )
    else:
      rt.append( POS(r[0], r[1], r[2], r[3], r[4]) )
  
  return rt 
  
########################################################################
# ~ Pavyzdys:

if __name__ == '__main__':

  donelaitis =  """
                Broliai seserys, imkit mane ir skaitykit
                Ir tatai skaitydami permanykit.
                Mokslo šito tėvai jūsų trokšdavo turėti,
                Ale to negalėjo nė vienu būdu gauti. 
                """

  lemmas = get_lemmas(donelaitis)

  for l in lemmas:
    print l[0], "|", l[1], "|", l[2], "|", l[3], "|", l[4]
