import argparse
import csv


def load_mbids_from_file(mbid_file):
    """Load a file of MBIDs"""
    with open(mbid_file, 'r') as f:
        mbids = f.read().splitlines()   

    return mbids


def get_gid_map(gid_map_file): 
    """Load the recording redirect file into a dictionary
    Args:
        gid_map_file: a filename containing mbid redirects in CSV format
    Returns:
        a dictionary of {line[0]: line[1]} for each line in the file
    """
    gid = {}
    with open(gid_map_file, 'r') as csvfile:
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

    id_list = sorted(list(set(id_list)))

    return id_list


def main(mbid_file, gid_map_file):
    """"""

    mbids = load_mbids_from_file(mbid_file)
    gid = get_gid_map(gid_map_file)
    id_list = get_full_id_list_from_map(mbids, gid)

    for mbid in id_list:
        print(mbid)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find all redirect MBIDs that exist for a given list of MBIDs')
    parser.add_argument('mbid_list', help='A file with a list of MBIDs')
    parser.add_argument('redirect_list', help='A csv file containing MBID redirects')
    args = parser.parse_args()

    main(args.mbid_list, args.redirect_list)
