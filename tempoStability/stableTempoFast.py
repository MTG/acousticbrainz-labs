import os, sys, json
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser
from scipy.interpolate import interp1d
import time
from scipy.signal import filtfilt
import pickle

def gaussianSmooth(ibi,tStep):
    degree = max(int(5.0/float(tStep)),2)   # 5 second smoothing window, but atleast two samples
    window=degree*2-1  
    weight=np.array([1.0]*window)  
    weightGauss=[]
    ibi = np.append(np.append(np.zeros(degree-1), ibi), np.zeros(degree))
    for i in range(window):  
        i=i-degree+1  
        frac=i/float(window)  
        gauss=1/(np.exp((4*(frac))**2))  
        weightGauss.append(gauss)  
    weight=np.array(weightGauss)*weight  
    smoothed=np.zeros((len(ibi)-window))
    sumWt = sum(weight)
    for i in range(len(smoothed)):  
        smoothed[i]=sum(np.array(ibi[i:i+window])*weight)/sumWt
    return smoothed

def gaussianSmooth1(ibi,tStep):
    degree = max(int(2.5/float(tStep)),2)   # 2.5 second smoothing window, but atleast two samples
    window=degree*2-1  
    weight=np.array([1.0]*window)  
    weightGauss=[]
    for i in range(window):  
        i=i-degree+1  
        frac=i/float(window)  
        gauss=1/(np.exp((4*(frac))**2))  
        weightGauss.append(gauss)  
    weight=np.array(weightGauss)*weight  
    smoothed=np.zeros((len(ibi)-window))
    sumWt = sum(weight)
    smoothed = filtfilt(weight,[sumWt], ibi)
    return smoothed


def genTempoCurve(ibi, beats, tStep):
    tcTimes = np.arange(beats[0], beats[-1], tStep)
    iFn = interp1d(beats, ibi, kind='linear')
    tc = iFn(tcTimes)
    tc = gaussianSmooth1(tc, tStep)
    return np.round(tcTimes,1), np.round(tc,1)
    
def estBeatStability(ibi, perc, thres):
    ibisort = np.sort(ibi)
    ind = np.floor((100-perc)/200.0*len(ibi))
    beatVar = np.std(ibisort[ind:-ind])
    if (beatVar < thres):
        stable = True
    else:
        stable = False
    return round(beatVar,2), stable
    
def batchProcess(bpath,outpath, thres=2.0, thresRamp=20.0, perc=80.0, tstep=0.5):
    batchResults = []
    cnt = 0
    for root, dirs, files in os.walk(bpath):
        for f in files:
            fullpath = os.path.join(root, f)
            if os.path.splitext(fullpath)[1] == '.json':
                try:
                    result = singleFileProcess(fullpath, thres, thresRamp, perc, tstep)
                except: 
                    cnt+=1
                    continue
                sDir = fullpath.split('/')
                try:
                    os.makedirs(os.path.join(outpath, sDir[-3], sDir[-2]))
                except:
                    pass
                json.dump(result, open(os.path.join(outpath, sDir[-3], sDir[-2], f), 'w'))
    
    print "Could not process %d number of files"%cnt
                 
    return True

def singleFileProcess(fpath, thres, thresRamp, perc, tstep):
    #print str('Processing file: ' + fpath)
    feat = json.load(open(fpath))
    beats = feat['rhythm']['beats_position']
    ibi = 60.0/np.diff(beats)
    tcTimes, tc = genTempoCurve(ibi, beats[1:], tstep)
    N = len(tc)
    valsStart = np.median(tc[int(.10*N):int(.25*N)])
    valsEnd = np.median(tc[int(.75*N):int(.90*N)])
    result = {}
    result['speedUp'] = False
    result['tempoCurve'] = [tcTimes.tolist(), tc.tolist()]
    result['beatVar'], result['stableBeat'] = estBeatStability(ibi, perc, thres)
    result['tempoVar'] = round(100*abs(valsStart- valsEnd)/float(np.median(tc)),2)
    if result['tempoVar'] > thresRamp:
        result['speedUp'] = True
    return result

if __name__ == "__main__":
    currTime = time.time()
    dirs = pickle.load(open('dirNames.pkl','r'))
    parser = OptionParser()
    parser.add_option("-b", "--bpath", dest="basepath", default='NONE', help="Path to the base folder")
    parser.add_option("-o", "--opath", dest="outpath", default='NONE', help="Path to the output folder")
    parser.add_option("-i", "--index", dest="dirInd", default='NONE', help="Index of the 256 directories (see structure )")
    parser.add_option("-t", "--threshold", dest="thres", default=2.0, help="Standard Deviation threshold in BPM")
    parser.add_option("-v", "--thresholdRamp", dest="thresRamp", default=20.0, help="Percentage change in median tempo to declare a speed up in the song")
    parser.add_option("-p", "--percentile", dest="percentile", default=80.0, help="Percentile used to compute std.")
    parser.add_option("-s", "--step", dest="tstep", default=0.5, help="Time step in second")
    (options, args) = parser.parse_args()
    for ii in range(64*(int(options.dirInd)-1), 64*(int(options.dirInd))):
        batchResults = batchProcess(os.path.join(options.basepath,dirs[ii]),options.outpath, options.thres, options.thresRamp, options.percentile, options.tstep)
    
    
    print "TIME : " + str(time.time() - currTime)