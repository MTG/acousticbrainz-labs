import os
import numpy as np
from numpy import cov
from numpy import genfromtxt
import json
import csv
import collections
from scipy import stats
from scipy.stats import spearmanr

features = [
    "length",
    "bpm",
    "average_loudness",
    "onset_rate",
    "replay_gain",
    "tuning_frequency"  
]

json_array = []

complex_features = [
    "beats_position",
    "chords_histogram",
    "hpcp_mean",
]

def load_json():
    """
        To load data from json dumps.
    """
    PATH = "00/"

    # json_files = [pos_json for pos_json in os.listdir(PATH) if pos_json.endswith('.json')]
    for pos_json in os.listdir(PATH):
        if pos_json.endswith('.json'):
            with open(PATH+pos_json) as f:
                data = json.load(f)
                json_array.append(extract_features(data))
    print(len(json_array))

    # arr = [row[0] for row in json_array]
    # print(len(arr))


def write_csv():
    """
        Helper function to write data to csv.
    """
    PATH = "00/"

    # json_files = [pos_json for pos_json in os.listdir(PATH) if pos_json.endswith('.json')]
    for pos_json in os.listdir(PATH):
        if pos_json.endswith('.json'):
            with open(PATH+pos_json) as f:
                data = json.load(f)
                json_array.append(extract_features(data))

    with open("output.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(json_array)

def load_csv(FNAME):
    data = genfromtxt(FNAME, delimiter=',')
    return data
    
def extract_features(decoded_data):

    arr = []
    #length
    arr.append(decoded_data["metadata"]["audio_properties"]["length"])
    #bpm
    arr.append(decoded_data["rhythm"]["bpm"])
    #average_loudness
    arr.append(decoded_data["lowlevel"]["average_loudness"])
    #onset_rate
    arr.append(decoded_data["rhythm"]["onset_rate"])
    #replay_gain
    arr.append(decoded_data["metadata"]["audio_properties"]["replay_gain"])
    #tuning_frequency
    arr.append(decoded_data["tonal"]["tuning_frequency"])
    
    return arr


def calc_z_scores(data):
    """
    used to calculate column vise z-scores for the list of data
    """
    data = np.array(data)
    z = np.zeros(data.shape)
    for i in range(0,data.shape[1]):
        arr = data[:, i].astype(np.float)
        arr = np.abs(stats.zscore(arr))
        z[:,i] = arr

    return z

def identify_anomalies(data):
    """
     returns a dict containing {ids,count}
     where count is the number of columns 
     threshold is taken to be 1.65 for a 95 % confidence value
    """
    arr = []
    z = calc_z_scores(data)
    for i in range(0,z.shape[1]):
        arr = np.concatenate((np.array(arr),np.where(z[:, i] > 1.65)[0]))
 
    unique, counts = np.unique(arr, return_counts=True)
    ids = dict(zip(unique, counts))
    return ids
    #check for ids which have more than or equalto 3 outlying features



if __name__ == "__main__":
    
    data = load_csv("output.csv")
    ids = identify_anomalies(data)

    outliers = [k for k, v in ids.items() if v >= 3]
    print("The offset of mbids which ate most likely to be misclassified are :")
    print(outliers)


