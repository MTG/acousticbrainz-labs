import argparse
import os
import json
import tempfile
import time

from requests.adapters import HTTPAdapter
import requests
from urllib3 import Retry

ret = Retry(total=10, backoff_factor=0.2)
adaptor = HTTPAdapter(max_retries=ret)
req_session = requests.Session()
req_session.mount('http://', adaptor)
req_session.mount('https://', adaptor)


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_id_list_from_file(id_list_file):
    with open(id_list_file, 'r') as f:
        id_list = f.read().splitlines()

    return id_list


def get_count_for_id_list(id_chunk):

    chunklist = ";".join(id_chunk)
    payload = {'recording_ids': chunklist}

    r = req_session.get('https://acousticbrainz.org/api/v1/count', params=payload)

    mapping = {}
    data = r.json()
    for k, v in data.items():
        mapping[k] = v['count']

    found_ids = mapping.keys()
    all_ids = set(id_chunk)
    missing_ids = all_ids - set(found_ids)

    mapping.update(dict.fromkeys(list(missing_ids), None))

    return mapping


def get_existing_mbids(json_output):
    """Check the json cache file (if it exists) and get a set of all
    MBID counts that have already been retrieved.
    If the file doesn't exist, return an empty set"""

    if not os.path.exists(json_output):
        return set()

    with open(json_output) as fp:
        data = json.load(fp)
        return set(data.keys())


def get_count_for_all_ids(id_list, json_filename):
    count_mapping = {}
    items_per_chunk = 10

    num_items = len(id_list)
    print('processing {} items'.format(num_items))

    # After each time that we get the counts, we write to the output file so that we can restart
    # the script at any time
    count = 0
    loops = 0
    mapping = {}
    for id_chunk in list(chunks(id_list, items_per_chunk)):
        new_mapping = get_count_for_id_list(id_chunk)
        mapping.update(new_mapping)
        count += items_per_chunk
        print('{}/{}'.format(count, num_items))

        # Only write every 100 loops (100 items) so that we don't spend more of our
        # time writing instead of doing lookups
        loops += 1
        if loops >= 1000:
            print(' - writing')
            rewrite_count_to_json(json_filename, mapping)
            loops = 0
            mapping = {}
        time.sleep(0.1)

    return count_mapping


def rewrite_count_to_json(json_filename, count_mapping):
    """load json_filename, update the result with count_mapping, and rewrite"""

    if os.path.exists(json_filename):
        data = json.load(open(json_filename))
        data.update(count_mapping)
    else:
        data = count_mapping

    # Write to temporary filename and rename for atomic operation
    with tempfile.NamedTemporaryFile('w', delete=False) as fp:
        json.dump(data, fp, indent=4)
        # TODO: os.fsync(f.fileno()) and close file before renaming
        os.rename(fp.name, json_filename)


def main(id_list_file, json_output):
    id_list = get_id_list_from_file(id_list_file)
    # Remove ids which are already in the json output file
    existing_mbids = get_existing_mbids(json_output)
    new_id_list = [l for l in id_list if l not in existing_mbids]
    print('id list was {}, now new list is {}'.format(len(id_list), len(new_id_list)))

    count_mapping = get_count_for_all_ids(new_id_list, json_output)

    return count_mapping


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find the counts of MBIDs in AcousticBrainz')
    parser.add_argument('mbid_list', help='A file with a list of MBIDs')
    parser.add_argument('json_count', help='Json filename to write counts to')
    args = parser.parse_args()

    main(args.mbid_list, args.json_count)
