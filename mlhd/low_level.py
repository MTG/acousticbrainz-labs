import csv
import requests
import json
import os

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_counts_from_file(counts_file):

	with open(counts_file, 'r') as f:
    	count_mapping = json.load(f)

    return count_mapping


def get_rec_list(counts):

	rec_list = []

    for i in range(0, counts):
        rec = ids + ':' + str(i)
        rec_list.append(rec)

    return rec_list


def write_lowlevel_file(ids, low_level):

	#Check if the directory exists
    if not os.path.exists(ids[0:2] + '/' + ids[2:4]):
        os.makedirs(ids[0:2] + '/' + ids[2:4])

    #Check if the file exists and if not, write it 
	if not os.path.isfile(ids[0:2] + '/' + ids[2:4] + '/' + ids[4:] + '_low_level_' + '.json'):        
	    with open(ids[0:2] + '/' + ids[2:4] + '/' + ids[4:] + '_low_level_' + '.json', 'w+') as f:
	        json.dump(low_level, f, indent=4)

    return 


def get_lowlevel_for_chunk(rec_chunk, low_level):

	chunklist = ";".join(rec_chunk)
	payload = {'recording_ids': chunklist}

	r = requests.get('https://acousticbrainz.org/api/v1/low-level', params=payload)
	if ids in low_level:
	    low_level[ids].update(r.json()[ids])
	else:
	    low_level.update(r.json())

	return


def get_lowlevel_for_all(count_mapping)

	for ids, counts in count_mapping.items():

	    if counts != None: 

	        low_level = {}
	        rec_list = get_rec_list(counts)

	        for rec_chunk in list(chunks(rec_list, 10)):    
	        	get_lowlevel_for_chunk(rec_chunk, low_level)

	        write_lowlevel_file(ids, low_level)


def main(counts_file):

	count_mapping = get_counts_from_file(counts_file)
	get_lowlevel_for_all(count_mapping)


if __name__ == "__main__":

	counts_file = 'id_counts.json'
	main(counts_file)