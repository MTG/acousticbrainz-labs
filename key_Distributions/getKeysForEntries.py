'''
Created on Nov 21, 2014

Generate a dict of abzRecordingMBID -> (groundTruth, extracted_key_key)
from a list (currently read form a file: matchedBillboardRecID2Key_key.json) 

@author: joro
'''

import json
import os
import urllib2
# In[42]:

def normSemiToneNotation(gtKey):
    '''
    convert b to # (flat to sharp) notation 
    '''
    if gtKey[-1] == 'b': 
        ascii_ = ord( gtKey[0])
        if ascii_ == 65: ascii_ +=7
        return chr(ascii_-1) + '#'
    else:
        return gtKey



counterWrongKeys= 0;
billboardGrTruthDict = {}

a = open ('/Users/joro/Downloads/mapRecID2Key.json')
mapped2Bilboarddata = json.load(a)
a.close()

totalNumEntries = len(mapped2Bilboarddata)

for index, abzRecordingMBID in enumerate(mapped2Bilboarddata.keys()):
    print 'processing entry {} out of {}'.format(index, totalNumEntries)
    
    # get json extr features. use abz API
    currLowLevelString = urllib2.urlopen('http://acousticbrainz.org/' + abzRecordingMBID + '/low-level').read()
    currLowLevelJSON = json.loads(currLowLevelString)
    
#     print currLowLevelJSON
    extracted_key_key =  currLowLevelJSON['tonal']['key_key']
    groundtruthKey = mapped2Bilboarddata[abzRecordingMBID]
    
    # normalize semitone-notation #-b
    groundtruthKey = normSemiToneNotation(groundtruthKey)

    # store
    keyMap={}
    keyMap[groundtruthKey]=extracted_key_key
    billboardGrTruthDict[abzRecordingMBID] = keyMap


    
    if not groundtruthKey == extracted_key_key:
        counterWrongKeys +=1
        print "\t error at recording " + abzRecordingMBID
        print '\t gt key: ' + groundtruthKey 
        print '\t extracted key: ' + extracted_key_key 

print counterWrongKeys
print billboardGrTruthDict
        
with open('matchedBillboardRecID2Key_key.json', 'w') as f:
        json.dump(billboardGrTruthDict, f, sort_keys = True, indent = 4, ensure_ascii=False)    
        f.close()
        
        