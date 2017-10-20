# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd

from IPython.display import display
from IPython.display import Image
#import glob

path = "T:\courses\MSiA400\Jobs"
#allFiles = glob.glob(path+"\*.csv")


#newjobs = pd.read_csv(path+'20140211_new'+'.csv',header= 0 )

descripjobs = pd.read_csv("file:///T:/courses/MSiA400/Jobs/20140212_descriptions.csv",names = ['JVGUID','Description'], encoding = "ISO-8859-1")
columns = ['JVGUID','DateNew','BUID','CompanyName','Title','OnetCode','Location','Link','a','b','c','d']		
newjobs = pd.read_csv("file:///T:/courses/MSiA400/Jobs/20140212_new.csv", names = columns,encoding = "ISO-8859-1" )
newjobs = newjobs[1:]

combined = pd.merge(descripjobs, newjobs, on='JVGUID', how='outer')

combined['State'] = combined['Location'].str[:2]
combined['City'] = combined['Location'].str[4:]
'''
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)
frame = pd.concat(list_)
'''
#\20140211_new.csv"

combined[combined['a'].notnull()].head()

*****

desc_list = combined['Description'].tolist()

import nltk
from nltk.tokenize import RegexpTokenizer, sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from nltk.stem import PorterStemmer, WordNetLemmatizer
ps = PorterStemmer()

t = 0
for desc in desc_list:
    try:
        tokens = word_tokenize(desc)
    except:
        t+=1
print(t) #1100 Empty strings out of 38K

combined['Description'] = ['na' if x is np.nan else x for x in combined['Description']]



from collections import Counter
N = 100

stopwords = nltk.corpus.stopwords.words('english')
# RegEx for stopwords
RE_stopwords = r'\b(?:#-{})\b'.format('|'.join(stopwords))
# replace '|'-->' ' and drop all stopwords
words = (combined.Description
           .str.lower()
           .replace([r'\|', RE_stopwords], [' ', ''], regex=True)
           .str.cat(sep=' ')
           .split())
words_stem = [ps.stem(w) for w in words]

lemmatizer = WordNetLemmatizer()

words_lemm = [lemmatizer.lemmatize(w) for w in words]
rslt = pd.DataFrame(Counter(words_lemm).most_common(N),
                    columns=['Word', 'Frequency']).set_index('Word')
print(rslt)



from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
finder = TrigramCollocationFinder.from_words(words)
finder.nbest(trigram_measures.pmi, 100) 
