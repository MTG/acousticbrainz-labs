import csv
import requests
import json


def get_mbid_from_file(mbid_file):

    mbids = []
    with open(mbid_file, 'r') as f:
        mbids = f.read().splitlines()   

    return mbids


def get_gid_map(gid_map_file): 

    gid = {}
    with open(gid_map_file, 'rb') as csvfile: 
        reader = csv.reader(csvfile)
        for row in reader:
            gid[row[0]] = row[1]

    return gid


def get_full_id_list_from_map(mbids, gid):

    id_list = []
    for el in mbids:
        if el in gid:
            id_list.append(el)
            id_list.append(gid[el])

        else: 
            id_list.append(el)

    id_list = list(set(id_list))

    return id_list


def write_id_list_to_file(id_list):

    with open('mbid_list.txt', 'w+') as f:
        for row in id_list: 
            f.write(row + '\n')


def main(mbid_file, gid_map_file):

    mbids = get_mbid_from_file(mbid_file)
    gid = get_gid_map(gid_map_file)
    id_list = get_full_id_list_from_map(mbids, gid)
    write_id_list_to_file(id_list)

    return = id_list


if __name__ == "__main__":

    mbid_file = 'MLHD_recording_mbids.txt'
    gid_map_file = 'recording_gid_redirect.csv'
    id_list = main(mbid_file, gid_map_file)