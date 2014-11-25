

'''
Created on Nov 21, 2014

Plot a histogram of difference in semitones btw ground truth and extracted keys. 
originally developed to read from json list created with getKeysForEntries.py
Extendable to reading from other formats.

@author: joro
'''

# coding: utf-8

# In[18]:

import matplotlib.pylab as plt
from collections import Counter, OrderedDict
import numpy as np

fig, ax = plt.subplots()


# In[19]:

import json

def calcErrorArray():
    f = open('matchedBillboardRecID2Key_key.json')
    m = json.load(f)
    f.close()

    chordIds = {'C':0, 'C#':1, 'D':2, 'D#':3, 'E':4, 'F':5, 'F#':6, 'G':7, 'G#':8, 'A':9, 'A#':10, 'B':11}
    # in semitones. 
    errorArray = []

    for keys_song in m.values():

        extracted_key = keys_song.values()[0]
        gtKey=  keys_song.keys()[0]
        error = chordIds[extracted_key] - chordIds[gtKey]
        if error > 6: error = error % (- len(chordIds))
        if error < -5: error = error % len(chordIds)
        errorArray.append(error)
    return errorArray


# In[24]:

errorArray = calcErrorArray()
errorKeysCounter = Counter(errorArray)
orderedErrorKeysCounter = OrderedDict(sorted(errorKeysCounter.items(), key=lambda t: t[0]))
musicKeys = orderedErrorKeysCounter.keys()
musicKeysCounts = [ orderedErrorKeysCounter[key] for key in musicKeys ]



# plotting 
x_values = np.arange(1, len(musicKeys) + 1, 1)


plt.bar(x_values, musicKeysCounts)
plt.xticks(x_values, musicKeys)
plt.show()

