#!/usr/bin/env python

import nltk
from nltk.corpus import brown
import json, os

prondict =  nltk.corpus.cmudict.dict()

with open(os.path.expanduser("~/.config/plover/dict.json")) as data_file:
   stenodict = json.load(data_file)

onset = {
   'B': 'PW',
   'CH': 'KH',
   'D': 'TK',
   'DH': 'TH',
   'F': 'TP',
   'G': 'TKPW',
   'HH': 'H',
   'JH': 'SKWR',
   'K': 'K',
   'L': 'HR',
   'M': 'PH',
   'N': 'TPH',
   'P': 'P',
   'R': 'R',
   'S': 'S',
   'SH': 'SH',
   'T': 'T',
   'TH': 'TH',
   'V': 'SR',
   'W': 'W',
   'Y': 'KWR',
   'Z': 'S*'
   }

nucleus = {
   'AA': 'O',
   'AE': 'A',
   'AH':  'U',
   'AO': 'AU',
   'AW': 'OU',
   'AY': 'AOEU',
   'EH': 'E',
   'ER': 'ER',
   'EY': 'AEU',
   'IH': 'EU',
   'IY': 'AOE',
   'OW': 'OE',
   'OY': 'OEU',
   'UH': 'U',
   'UW': 'AOU'
   }

coda = {
   'ER': 'R',
   'B':'B',
   'CH': 'FP',
   'D': 'D',
   'DH': '*T',
   'F': 'F',
   'G': 'G',
   'JH': 'PBLJ',
   'K': 'BG',
   'L': 'L',
   'M': 'PL',
   'N': 'PB',
   'NG': 'PBG',
   'P': 'P',
   'R': 'R',
   'S': 'S',
   'SH': 'RB',
   'T': 'T',
   'TH': '*T',
   'V': 'F',
   'Z': 'Z'
   }
   
def word_to_steno(word):
   result = []
   for pron in prondict[word]:
      syll = []
      seg = []

#      if len(pron) != 3:
#         syll.append("VOID")
      
      for phone in pron:
         if phone[-1] == '1':
            syll.append(seg)
            syll.append([phone])
            seg = []
#         elif phone[-1] == '0':
#            seg += "VOID"
         else:
            seg.append(phone)
      syll.append(seg)
         
      entry = ''
      if len(syll) == 3:
         for phone in syll[0]:
            entry += onset.get(phone[:2], '')
         for phone in syll[1]:
            entry += nucleus.get(phone[:2], '')
         for phone in syll[2]:
            entry += coda.get(phone[:2], '')
         result.append(entry)
   return result

easy_words = []

for word in nltk.corpus.cmudict.words():
   for steno in word_to_steno(word):
      if stenodict.get(steno) == word:# and 3 <= len(steno) <= 6:
         print(word)
         easy_words.append(word)
         #print(steno)
         #print(prondict[word])

#for bigram in list(nltk.bigrams(brown.words())):
#   if bigram[0] in easy_words and bigram[1] in easy_words:
#         print(bigram[0] + ' ' + bigram[1])

#for trigram in list(nltk.trigrams(brown.words())):
#   if trigram[0] in easy_words and trigram[1] in easy_words and trigram[2] in easy_words:
#         print(trigram[0] + ' ' + trigram[1] + ' ' + trigram[2])
