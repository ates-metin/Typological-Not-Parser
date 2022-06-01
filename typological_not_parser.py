# -*- coding: utf-8 -*-
"""Typological Not-Parser

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sKOb5ij9s9XUf8An-wvRSq-eAFuyRfkS

This part installs Berkeley Neural Parser (Benepar) and an English lemmatizer (Lemminflect).
"""

# benepar from: https://github.com/nikitakit/self-attentive-parser
!pip install benepar
!pip install spacy
!python -m spacy download 'en_core_web_md'
import en_core_web_md

# english lemmatizer from: https://github.com/bjascob/LemmInflect
!pip3 install lemminflect

"""This part installs and imports the relevant packages such as getLemma, nltk, regEx, benepar_en3, etc."""

from lemminflect import getLemma    # lemmatizer for english

# requirements for benepar
import spacy, benepar      
nlp = spacy.load('en_core_web_md')

from benepar.spacy_plugin import BeneparComponent

benepar.download('benepar_en3')

if spacy.__version__.startswith('2'):
    nlp.add_pipe(BeneparComponent("benepar_en3"))
else:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})

#     #     #     #     #

import re
import warnings      # this disables unnecessary warnings
warnings.filterwarnings('ignore')


# matplotlib to draw charts of data

import sys
import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt

import matplotlib.rcsetup as rcsetup
print(rcsetup.all_backends)

# numpy

import numpy as np

"""The function definition of the parser."""

# code taken from Berkeley Neural Parser - Spacy
def parse(sentence):
  doc = nlp(sentence)
  sent = list(doc.sents)[0]
  parsed = sent._.parse_string
  return parsed

def ask_karahan():  # the points we fail
  return 'ask karahan'

"""an example:"""

parse('i love hot dogs')

"""Functions to find the relevant constituents of a given English sentence."""

# finds the subject
def find_subject(sentence):
  '''[ENG] Finds the subject for a given string. Finds the NP or sentencial labeled
  ('SBAR' 'S') constituents to avoid adverbs and such. 
  Returns a spacy_token type object.'''

  doc = nlp(sentence.strip())
  sent = list(doc.sents)[0]
  labeled = label_children(sent)
  for item in labeled:
    if item == ['NP']:
      indx = labeled.index(item)
      return list(sent._.children)[indx]
    elif item == ['SBAR']:
      indx = labeled.index(item)
      return list(sent._.children)[indx]
    elif item == ['S']:
      indx = labeled.index(item)
      return list(sent._.children)[indx]
    elif 'S' in item:
      indx = labeled.index(item)
      return list(sent._.children)[indx]     
    else:
      return ask_karahan()

# finds the direct object (kind of?)
def find_direct_object(sentence):
  '''[ENG] Finds direct object for a given string. Finds it according to the position
  of the VP. Returns a spacy_token type object. '''

  doc = nlp(sentence.strip())
  sent = list(doc.sents)[0]
  l_vp = find_lowest_vp(sentence)
  return list(l_vp._.children)[1]

# returns the XP's immediately dominated
def label_children(sent) -> list: 
  '''[ENG] Returns the labels of constituents which are immediately dominated 
  for a given spacy_token type object, returns a list''' 

  children = []
  for item in list(sent._.children):
    label = list(item._.labels)
    children.append(label)
  return children

# finds the lowest vp 
def find_lowest_vp(sentence):
  '''[ENG] Find the lowest VP for a given string. This includes several nested
  VP's as well. Returns a spacy_token type object.'''

  doc = nlp(sentence.strip())
  sent = list(doc.sents)[0]
  there_is_VP = True
  while there_is_VP:
    labeled = label_children(sent)   
    if ['VP'] in labeled:  # detects VP among constituents
      indx = labeled.index(['VP'])
      sent = list(sent._.children)[indx]
    else:   # there is no VP 
      there_is_VP = False
      
  return sent

# finds the v head of the lowest vp
def find_verb(sentence):
  '''[ENG] Finds the V-head of the lowest VP (the leftmost constituent)
  for a given string. Returns a spacy_token type object.'''

  return list(find_lowest_vp(sentence))[0]

"""The word order function. """

def get_word_order(gloss, translation):
  '''Returns word order for a given gloss, translation respectively'''

  vhead = str(find_verb(translation))
  vhead = getLemma(vhead, upos='VERB')[0]
  
  subj = str(find_subject(translation))
  subj.strip()
  a_list = []
  if ' ' in subj:       # if the subject consists of several words, 
    subj = re.split(r'\s', subj)     #takes the longest one
    for word in subj:
      a_list.append(len(word))
    mx = max(a_list)
    indx = a_list.index(mx)
    subj = getLemma(subj[indx],upos='VERB')[0]
  else:
    subj = getLemma(subj, upos='VERB')[0]

  do = str(find_direct_object(translation))
  do = getLemma(do, upos='VERB')[0]
  do.strip()
  another_list = []
  if ' ' in do:            # if the direct object consists of several words,
    do = re.split(r'\s', do)  # takes the longest one
    for word in do:
      another_list.append(len(word))
    max1 = max(another_list)
    indx1 = another_list.index(max1)
    do = getLemma(do[indx1], upos='NOUN')[0]
  else:
    do = getLemma(do, upos='NOUN')[0]

  if (vhead and do) in gloss:
    v = gloss.index(vhead)
    o = gloss.index(do)

    if subj in gloss:
      s = gloss.index(subj)
      
      SVO = s < v < o
      SOV = s < o < v
      VOS = v < o < s
      VSO = v < s < o 
      OVS = o < v < s
      OSV = o < s < v 
      
      if SVO:
        return 'SVO'
      elif SOV:
        return 'SOV'
      elif VOS:
        return 'VOS'
      elif VSO:
        return 'VSO'
      elif OVS:
        return 'OVS'
      elif OSV:
        return 'OSV'
    
    elif 'pro' in gloss:
      s = gloss.index('pro')

      SVO = s < v < o
      SOV = s < o < v
      VOS = v < o < s
      VSO = v < s < o 
      OVS = o < v < s
      OSV = o < s < v 
    
      if SVO:
        return 'SVO'
      elif SOV:
        return 'SOV'
      elif VOS:
        return 'VOS'
      elif VSO:
        return 'VSO'
      elif OVS:
        return 'OVS'
      elif OSV:
        return 'OSV'
    
    else:
      return ask_karahan()
  
  else:
    return ask_karahan()

"""Converts accusative and genitive into nominative for identifying words in gloss."""

def nominative(string):
  '''Converts pronouns with case to nominative form.'''
  
  s=re.sub("^me$","i",string)
  s=re.sub("^my$","i",s)
  s=re.sub("^your$","you",s)
  s=re.sub("^him$","he",s)
  s=re.sub("^his$","he",s)
  s=re.sub("^her$","she",s)
  s=re.sub("^them$","they",s)
  s=re.sub("^us$","we",s)
  s=re.sub("^our$","we",s)

  s=re.sub("^me ","i ",s)
  s=re.sub("^my ","i ",s)
  s=re.sub("^your ","you ",s)
  s=re.sub("^him ","he ",s)
  s=re.sub("^his ","he ",s)
  s=re.sub("^her ","she ",s)
  s=re.sub("^them ","they ",s)
  s=re.sub("^us ","we ",s)
  s=re.sub("^our ","we ",s)

  s=re.sub(" me$"," i",s)
  s=re.sub(" my$"," i",s)
  s=re.sub(" your$"," you",s)
  s=re.sub(" him$"," he",s)
  s=re.sub(" his$"," he",s)
  s=re.sub(" her$"," she",s)
  s=re.sub(" them$"," they",s)
  s=re.sub(" us$"," we",s)
  s=re.sub(" our$"," we",s)

  s=re.sub(" me "," i ",s)
  s=re.sub(" my "," i ",s)
  s=re.sub(" your "," you ",s)
  s=re.sub(" him "," he ",s)
  s=re.sub(" his "," he ",s)
  s=re.sub(" her "," she ",s)
  s=re.sub(" them "," they ",s)
  s=re.sub(" us "," we ",s)
  s=re.sub(" our "," we ",s)

  s=re.sub("^me-","i-",s)
  s=re.sub("^my-","i-",s)
  s=re.sub("^your-","you-",s)
  s=re.sub("^him-","he-",s)
  s=re.sub("^his-","he-",s)
  s=re.sub("^her-","she-",s)
  s=re.sub("^them-","they-",s)
  s=re.sub("^us-","we-",s)
  s=re.sub("^our-","we-",s)

  s=re.sub("-me$","-i",s)
  s=re.sub("-my$","-i",s)
  s=re.sub("-your$","-you",s)
  s=re.sub("-him$","-he",s)
  s=re.sub("-his$","-he",s)
  s=re.sub("-her$","-she",s)
  s=re.sub("-them$","-they",s)
  s=re.sub("-us$","-we",s)
  s=re.sub("-our$","-we",s)

  s=re.sub("-me-","-i-",s)
  s=re.sub("-my-","-i-",s)
  s=re.sub("-your-","-you-",s)
  s=re.sub("-him-","-he-",s)
  s=re.sub("-his-","-he-",s)
  s=re.sub("-her-","-she-",s)
  s=re.sub("-them-","-they-",s)
  s=re.sub("-us-","-we-",s)
  s=re.sub("-our-","-we-",s)

  s=re.sub(" me-"," i-",s)
  s=re.sub(" my-"," i-",s)
  s=re.sub(" your-"," you-",s)
  s=re.sub(" him-"," he-",s)
  s=re.sub(" his-"," he-",s)
  s=re.sub(" her-"," she-",s)
  s=re.sub(" them-"," they-",s)
  s=re.sub(" us-"," we-",s)
  s=re.sub(" our-"," we-",s)

  s=re.sub("-me ","-i ",s)
  s=re.sub("-my ","-i ",s)
  s=re.sub("-your ","-you ",s)
  s=re.sub("-him ","-he ",s)
  s=re.sub("-his ","-he ",s)
  s=re.sub("-her ","-she ",s)
  s=re.sub("-them ","-they ",s)
  s=re.sub("-us ","-we ",s)
  s=re.sub("-our ","-we ",s)

  s=re.sub(" me\)"," i)",s)
  s=re.sub(" my\)"," i)",s)
  s=re.sub(" your\)"," you)",s)
  s=re.sub(" him\)"," he)",s)
  s=re.sub(" his\)"," he)",s)
  s=re.sub(" her\)"," she)",s)
  s=re.sub(" them\)"," they)",s)
  s=re.sub(" us\)"," we)",s)
  s=re.sub(" our\)"," we)",s)
  return s

# bunu düzgün bi regex olarak yazmak lazım -ateş
# glossda pronounların labelı unique, sadece pronoun olduğunu bildiğimiz şeylere kullanırsak gerek kalmaz -arda
# anladım, süper -ateş
# amelelik yapıp yazdım -arda

"""GEN-N and ADJ-N functions with RegEx."""

def gen_n_order(gloss,translation):
  '''Returns GEN-N order for a given gloss, translation respectively.'''
  
  if "PRP$" in parse(translation):
    regexstring=re.search("PRP\$ [a-z]+[\(\)\s]+[A-Za-z\(\)\s]+NN [a-z]+",parse(translation))[0]
    genandnoun=re.findall("[a-z]+",regexstring)
    genitive=getLemma(genandnoun[0],upos='NOUN')[0]
    noun=getLemma(genandnoun[-1],upos='NOUN')[0]
    genitive=nominative(genitive)
    noun=nominative(noun)
    if (genitive in gloss) and (noun in gloss):
      if gloss.index(genitive)<gloss.index(noun):
        return "GEN-N"
      elif gloss.index(noun)<gloss.index(genitive):
        return "N-GEN"
      else:
        return ask_karahan()
    else:
      return ask_karahan()

  elif "POS" in parse(translation):
    regexstring=re.search("[a-z]+\) \(POS ['a-z]+[\(\)\s]+[A-Za-z\(\)\s]+NN [a-z]+",parse(translation))[0]
    genandnoun=re.findall("[a-z]+",regexstring)
    genitive=getLemma(genandnoun[0],upos='NOUN')[0]
    noun=getLemma(genandnoun[-1],upos='NOUN')[0]
    if gloss.index(genitive)<gloss.index(noun):
      return "GEN-N"
    elif gloss.index(noun)<gloss.index(genitive):
      return "N-GEN"
    else:
      return ask_karahan()
  elif " of)" in parse(translation):
    regexstring=re.search("[a-z]+\)+ [ \(A-Z]+ of\)[ \(A-Z]+ [a-z]+",parse(translation))[0]
    genandnoun=re.findall("[a-z]+",regexstring)
    noun=getLemma(genandnoun[0],upos='NOUN')[0]
    genitive=getLemma(genandnoun[-1],upos='NOUN')[0]
    if gloss.index(genitive)<gloss.index(noun):
      return "GEN-N"
    if gloss.index(noun)<gloss.index(genitive):
      return "N-GEN"
  else:
    return ask_karahan()

def adj_n_order(gloss,translation):
  '''Returns ADJ-N order for a given gloss, translation respectively.'''
  
  if "JJ" in parse(translation):
    regexstring=re.search("JJ [a-z]+[\(\)\s]+[A-Z]+ [a-z]+",parse(translation))[0]
    adjandnoun=re.findall("[a-z]+",regexstring)
    adjective=getLemma(adjandnoun[0],upos='NOUN')[0]
    noun=getLemma(adjandnoun[-1],upos='NOUN')[0]
    if (adjective in gloss) and (noun in gloss):
      if gloss.index(adjective)<gloss.index(noun):
        return "ADJ-N"
      elif gloss.index(noun)<gloss.index(adjective):
        return "N-ADJ"
      else:
        return ask_karahan()
    else:
      return ask_karahan()
  else:
    return ask_karahan()

"""The function to read the given language data and return a list."""

def get_data(txt):
  '''reads data // returns the language name, list of glosses 
  and the list of tranlsations within a list'''
  
  f = open(txt,'r')
  splitted = f.read().lower().split('\n')
  
  data = []
  for item in splitted:
    if item != '' and item != '\n':
      data.append(item)
  language = data[0]
  data.remove(language)

  glosses = []
  translations = []
  for i in range(len(data)):
    if i % 3 == 1:
      glosses.append(data[i])
    elif i%3 == 2:
      translations.append(data[i])
  return [language, glosses, translations]

"""All functions put together."""

def Typological_Not_Parser(File):
  '''gets input as .txt file. See the readme file for glossing and file conventions'''
  
  data = get_data(File)
  glosses = data[1]
  translations = data[2]

  language = data[0]
  print(language.upper())
  print()
  print('{} datapoints for {}'.format(len(glosses),language))
  print()
  print('Type a command to continue. The commands are features/test/chart/input/commands/exit.')
  print()
  print('\'features\' shows the head-dependent structures for the given glossed data.')
  print('\'test\' is the evaluation function showing the accuracy of the program for the given test-data.')
  print('\'chart\' provides a pie chart for the given feature.')
  print('\'input\' takes manual input for testing.')
  print()
  print('Type \'commands\' to see commands again.')
  print()
  print('Type \'exit\' to exit. Type \'commands\' to see commands again.')
  


  sentences = []
  for i in range(len(glosses)):
    sentences.append([glosses[i],translations[i]])

  wo_labels = ['SVO','SOV','VSO','VOS','OVS','OSV']
  adj_n_labels = ['ADJ-N','N-ADJ']
  gen_n_labels = ['GEN-N','N-GEN']
  
  word_orders = []
  adj_n = []
  gen_n = []
  for sentence in sentences:
    
    res1 = get_word_order(sentence[0],sentence[1])
    if res1 in wo_labels:
      word_orders.append(res1)
    
    res2 = adj_n_order(sentence[0],sentence[1])
    if res2 in adj_n_labels:
      adj_n.append(res2)

    res3 = gen_n_order(sentence[0],sentence[1])
    if res3 in gen_n_labels:
      gen_n.append(res3)

  wo_counts = []
  adjn_counts = []
  genn_counts = []

  ### final items are tuples with frequency, label ###

  for i in range(len(wo_labels)):
    wo_counts.append(word_orders.count(wo_labels[i]))
  
  mxcount1 = max(wo_counts)
  wo_max = wo_labels[wo_counts.index(mxcount1)]
  if len(word_orders) != 0:
    wo_final = (mxcount1*100/len(word_orders), wo_max)
  else:
    wo_final = (0, 'None')
  for i in range(len(adj_n_labels)):
    adjn_counts.append(adj_n.count(adj_n_labels[i]))
  
  mxcount2 = max(adjn_counts)
  adjn_max = adj_n_labels[adjn_counts.index(mxcount2)]
  if len(adj_n) != 0:
    adjn_final = (mxcount2*100/len(adj_n), adjn_max)
  else:
    adjn_final = (0, 'None')
  for i in range(len(gen_n_labels)):
      genn_counts.append(gen_n.count(gen_n_labels[i]))
  
  mxcount3 = max(genn_counts)
  genn_max = gen_n_labels[genn_counts.index(mxcount3)]
  if len(gen_n) != 0:
    genn_final = (mxcount3*100/len(gen_n), genn_max)
  else:
    genn_final = (0, 'None')

  ### final items are tuples with frequency, label ###

  while True:
    print()
    print('Type a command to continue.')
    print()
    command = input().strip()
    
    if command == 'features':
      print()
      print('The data exhibit {}% {} order with {} datapoints'.format(wo_final[0],wo_final[1],len(word_orders)))
      print('The data exhibit {}% {} order with {} datapoints.'.format(adjn_final[0],adjn_final[1],len(adj_n)))
      print('The data exhibit {}% {} order with {} datapoints.'.format(genn_final[0],genn_final[1],len(gen_n)))

    elif command == 'chart':
      print()
      feature = input('Please enter a feature (WO, GEN-N, ADJ-N): ')
      print()
      if feature == 'WO':
        y = np.array([wo_counts[0],wo_counts[1],wo_counts[2],wo_counts[3],
            wo_counts[4],wo_counts[5]])
        plt.pie(y, labels = wo_labels)
        plt.show()

      elif feature == 'ADJ-N':
        y = np.array([adjn_counts[0],adjn_counts[1]])
        plt.pie(y, labels = adj_n_labels)
        plt.show()

      elif feature == 'GEN-N':
        y = np.array([genn_counts[0],genn_counts[1]])
      
        plt.pie(y, labels = gen_n_labels)
        plt.show()
      print('Type \'exit\' to show chart. The program itself \
will decide if it will show the chart or not.')

    elif command == 'test':
      print()
      test_file = input('Enter the test-file name: ')
      print()
      print('You may wait a long time for testing, as the program is kind of lazy.')
      print()
      r = open(test_file,'r')
      test_list = r.read().split('\n')
      
      test_name = test_list.pop(0)

      cleaned = []

      for item in test_list:
        if item in wo_labels:
          cleaned.append(item)
        elif item in adj_n_labels:
          cleaned.append(item)
        elif item in gen_n_labels:
          cleaned.append(item)
        elif item == 'None' or item == 'NONE':
          cleaned.append(item)

        wo_test_labels = []
        adjn_test_labels = []
        genn_test_labels = []

        for i in range(len(cleaned)):
          if i%3 == 0:
            wo_test_labels.append(cleaned[i])
          elif i%3 == 1:
            adjn_test_labels.append(cleaned[i])
          elif i%3 == 2:
            genn_test_labels.append(cleaned[i])

      ev_counts = []
      
      for sentence in sentences:
        wo1 = get_word_order(sentence[0],sentence[1])
        adjn1 = adj_n_order(sentence[0],sentence[1])
        genn1 = gen_n_order(sentence[0],sentence[1])

        i = sentences.index(sentence)
        
        if wo1 == wo_test_labels[i]:
          ev_counts.append(1)
        elif wo1 == 'ask karahan' and wo_test_labels[i] == 'None':
          ev_counts.append(1)
        else:
          ev_counts.append(0)
        
        if adjn1 == adjn_test_labels[i]:
          ev_counts.append(1)
        elif adjn1 == 'ask karahan' and adjn_test_labels[i] == 'None':
          ev_counts.append(1)
        else:
          ev_counts.append(0)
        
        if genn1 == genn_test_labels[i]:
          ev_counts.append(1)
        elif genn1 == 'ask karahan' and genn_test_labels[i] == 'None':
          ev_counts.append(1)
        else:
          ev_counts.append(0)
        
      score = np.sum(ev_counts)*100/ len(ev_counts)

      print(test_name.upper(),':')
      print()
      print('The accuracy for the given data is {}%'.format(score))

    elif command == 'commands':
      print()
      print('Commands: features/chart/test/input/exit')
    
    elif command == 'input':
      print()
      print('Be careful! Only takes sentences with transitive verbs!')
      print()
      gl = input('Please enter gloss: ')
      print()
      tr = input('Please enter translation: ')

      wo = get_word_order(gl,tr)
      GENN = gen_n_order(gl,tr)
      ADJN = adj_n_order(gl,tr)

      print()
      print('The data exhibit {}, {}, and {} orders.'.format(wo,GENN,ADJN))
    elif command == 'exit':
      break
    else:
      print('Invalid input')

Typological_Not_Parser('turkish.txt')

# Many thanks to Ümit Atlamaz, Utku Türk and Karahan Şahin for their support.