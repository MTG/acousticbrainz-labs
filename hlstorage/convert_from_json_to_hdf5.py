import h5py
import json
import sys

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

if __name__=="__main__":
    filename = sys.argv[1]
    json_data = open(filename).read()
    data = json.loads(json_data)
    data = convert(data)
    output_file = h5py.File('output.hdf5','w')
    for feature_set in data:
        for feature_description in data[feature_set]:
            if type(data[feature_set][feature_description]) == dict:
                for feature_attribute in data[feature_set][feature_description]:
                    output_file["/"+feature_set+"/"+feature_description+"/"+feature_attribute] = data[feature_set][feature_description][feature_attribute]
