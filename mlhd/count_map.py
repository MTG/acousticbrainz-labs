import csv
import requests
import json


def chunks(l, n):

    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_id_list_from_file(id_list_file):

    id_list = []
    with open(id_list_file, 'r') as f: 
        id_list = f.read().splitlines()

    return id_list


def get_count_for_id_chunk(id_chunk, count_mapping):

    new_id_chunk = []
    for el in id_chunk: 
        if el not in count_mapping: 
            new_id_chunk.append(el)

    chunklist = ";".join(new_id_chunk)
    payload = {'recording_ids': chunklist}

    r = requests.get('https://acousticbrainz.org/api/v1/count', params=payload)

    all_ids = set(new_id_chunk)
    found_ids = set(r.json().keys())
    missing_ids = all_ids - found_ids 

    count = []

    for el in found_ids:
        count.append(r.json()[el]['count'])

    count_mapping.update(dict(zip(found_ids, count)))
    count_mapping.update(dict.fromkeys(missing_ids, None))

    return


def get_count_for_all_ids(id_list):

    count_mapping = {}

    for id_chunk in list(chunks(id_list, 10)):

        if id_chunk not in count_mapping: 
            get_count_for_id_chunk(id_chunk, count_mapping)

    return count_mapping


def write_count_to_json(count_mapping):

    with open('data.json', 'w+') as f: 
        json.dump(count_mapping, f, indent=4)


def main(id_list_file):

    id_list = get_id_list_from_file(id_list_file)
    count_mapping = get_count_for_all_ids(id_list)
    write_count_to_json(count_mapping)

    return count_mapping


if __name__ == "__main__":

    id_list_file = 'mbid_list.txt'
    count_mapping = main(id_list_file)