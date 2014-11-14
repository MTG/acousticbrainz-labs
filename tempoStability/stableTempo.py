import os, sys, json
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser
from scipy.interpolate import interp1d

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

def genTempoCurve(ibi, beats, tStep):
    tcTimes = np.arange(beats[0], beats[-1], tStep)
    iFn = interp1d(beats, ibi, kind='cubic')
    tc = iFn(tcTimes)
    tc = gaussianSmooth(tc, tStep)
    return tcTimes, tc
    
def estBeatStability(ibi, perc, thres):
    ibisort = np.sort(ibi)
    ind = np.floor((100-perc)/200.0*len(ibi))
    beatVar = np.std(ibisort[ind:-ind])
    if (beatVar < thres):
        stable = True
    else:
        stable = False
    return beatVar, stable
    
def batchProcess(bpath, thres, perc, tstep):
    batchResults = []
    for root, dirs, files in os.walk(bpath):
        for f in files:
            fullpath = os.path.join(root, f)
            if os.path.splitext(fullpath)[1] == '.json':
                result = singleFileProcess(fullpath, thres, perc, tstep)
                result['path'] = fullpath
                batchResults.append(result)
    return batchResults

def singleFileProcess(fpath, thres, perc, tstep):
    print str('Processing file: ' + fpath)
    feat = json.load(open(fpath))
    beats = feat['rhythm']['beats_position']
    ibi = 60.0/np.diff(beats)
    tcTimes, tc = genTempoCurve(ibi, beats[1:], tstep)
    result = {}
    result['tempoCurve'] = [tcTimes.tolist(), tc.tolist()]
    result['beatVar'], result['stableBeat'] = estBeatStability(ibi, perc, thres)
    return result

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-b", "--bpath", dest="basepath", default='NONE', help="Path to the base folder")
    parser.add_option("-t", "--threshold", dest="thres", default=2.0, help="Standard Deviation threshold in BPM")
    parser.add_option("-p", "--percentile", dest="percentile", default=80.0, help="Percentile used to compute std.")
    parser.add_option("-s", "--step", dest="tstep", default=0.5, help="Time step in second")
    (options, args) = parser.parse_args()
    if args:
        result = singleFileProcess(args[0], options.thres, options.percentile, options.tstep)
        plt.plot(result['tempoCurve'][0],result['tempoCurve'][1])
        print result['beatVar'], result['stableBeat']
        plt.show()
    elif options.basepath != 'NONE':
        batchResults = batchProcess(options.basepath,options.thres, options.percentile, options.tstep)
        for result in batchResults:
            print len(result['tempoCurve'][0])*options.tstep, result['beatVar'], result['stableBeat']
    