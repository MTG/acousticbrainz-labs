import json
import pandas as pd


def map(genre, mapping_file):

    gen_new = []
    with open(mapping_file) as f:
        data = json.load(f)
        
        for el in genre:
            gen_new.append(data[el])

    return pd.Series(gen_new)
            

