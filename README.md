# Typological-Not-Parser
Cross-linguistic word order detector working with a parser (Benepar) and lemmatizer (Lemminflect) for English

This program is the final project of two students (Arda Ozogul and Ates Metin) for the Computational Linguistics class in Bogazici University.

It takes linguistic data as input (.txt files), reads glosses and the English translation and returns word order, adj-n order and gen-n order information. 

# Data limitations

Only takes transitive declarative sentences. Cannot take object or ind-object pro-dropped sentences, for subject pro drop see glossing conventions. 


# Importing dependencies

You need to download/import spacy, benepar, numpy matplotlib, lemminflect

- For Benepar see: https://github.com/nikitakit/self-attentive-parser

 if en_core_web_md is not installed:

  (1)	!python -m spacy download 'en_core_web_md'
	import en_core_web_md

  (2)	import spacy, benepar      
	nlp = spacy.load('en_core_web_md')

	from benepar.spacy_plugin import BeneparComponent

	benepar.download('benepar_en3')

	if spacy.__version__.startswith('2'):
    	    nlp.add_pipe(BeneparComponent("benepar_en3"))
	else:
    	    nlp.add_pipe("benepar", config={"model": "benepar_en3"})

  If doesn't work, try restarting runtime after running (1).


- For Lemminflect see: https://github.com/bjascob/LemmInflect


# Input file requirements:

The program takes .txt files

The data should be written in order such as 'sentence' - 'gloss' - 'translation' with a row indicating "language name" at the beginning. 

The test file should be written in order such as 'word order' - 'ADJ-N order' - 'GEN-N order'. The test file is case sensitive, write 'None' for no label. Otherwise write in capitals. 

For further info, please see the samples: 'turkish.txt' & 'turkish_test.txt'


# Glossing conventions

'-' indicates morpheme boundary, '.' indicates fusion of morphemes and space indicates word boundary. 

the program doesn't detect null arguments, for subject pro drop, please write 'pro'.

pronouns must be written in the English nominative form such as:
  
   'i-dat', 'we-gen', etc.


# Dependencies:

- benepar
- lemminflect
- spacy

# 

Many thanks to Ümit Atlamaz, Utku Türk and Karahan Şahin.
