import json
import pandas as pd


def map(genre):

    gen_new = []
    with open('genre_mapping.json') as f:
        data = json.load(f)
        
        for el in genre:
            gen_new.append(data[el])

    return pd.Series(gen_new)
            

