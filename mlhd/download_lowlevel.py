import argparse
import datetime
import json
import os
import time

from requests.adapters import HTTPAdapter
import requests
from urllib3 import Retry

ret = Retry(total=10, backoff_factor=0.2)
adaptor = HTTPAdapter(max_retries=ret)
req_session = requests.Session()
req_session.mount('http://', adaptor)
req_session.mount('https://', adaptor)

def time_stats(done, total, starttime):
    """Count how far through a repeated operation you are.

    Use this method if you are performing a repeated operation over
    a list of items and you want to check progress and time remaining
    after each iteration.

    Args:
        done (int): how many items have been processed
        total (int): the total number of items that are to be processed
        starttime: the result of an initial call to time.monotonic()

    Returns:
        A tuple of (time elapsed, time remaining), as a string representation
        of a timedelta
    """
    nowtime = time.monotonic()
    position = done*1.0 / total
    duration = round(nowtime - starttime)
    durdelta = datetime.timedelta(seconds=duration)
    remaining = round((duration / position) - duration)
    remdelta = datetime.timedelta(seconds=remaining)

    return str(durdelta), str(remdelta)

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_mbids_from_counts_file(counts_file):
    with open(counts_file, 'r') as f:
        count_mapping = json.load(f)

    mbids = []
    for mbid, count in count_mapping.items():
        if count:
            mbids.extend(get_recording_list(mbid, count))

    return sorted(mbids)


def get_recording_list(mbid, count):
    """Given an mbid and a count return a list of this mbid `count` times"""

    return ['{}:{}'.format(mbid, i) for i in range(count)]


def filter_mbids_from_destination(mbids, dest_dir):
    """Check if any of the mbids in the list `mbids` have already been downloaded into `dest_dir`"""
    new_mbids = []
    for m in mbids:
        mbid, count = m.split(':')
        prefix = mbid[:2]
        tarfile = '{}.tar.bz2'.format(prefix)
        directory = os.path.join(mbid[0:2], mbid[2:4])
        fname = '{}-{}.json'.format(mbid, count)
        if not os.path.exists(os.path.join(dest_dir, tarfile)) and not os.path.exists(os.path.join(dest_dir, directory, fname)):
            new_mbids.append(m)

    return new_mbids


def write_lowlevel(dest_dir, mbid, offset, data):

    directory = os.path.join(dest_dir, mbid[0:2], mbid[2:4])
    os.makedirs(directory, exist_ok=True)

    fname = '{}-{}.json'.format(mbid, offset)
    with open(os.path.join(directory, fname), 'w+') as f:
        json.dump(data, f, indent=4)


def get_lowlevel_for_chunk(mbids):
    payload = {'recording_ids': ';'.join(mbids)}

    r = req_session.get('https://acousticbrainz.org/api/v1/low-level', params=payload)
    try:
        return r.json()
    except ValueError:
        return None


def get_lowlevel_for_all_and_save(mbids, dest_dir):
    items_per_chunk = 10

    num_items = len(mbids)
    count = 0
    start = time.monotonic()
    for rec_chunk in chunks(mbids, items_per_chunk):
        low_level = get_lowlevel_for_chunk(rec_chunk)
        count += items_per_chunk
        print('{}/{}'.format(count, num_items))
        print(rec_chunk[0])

        if low_level:
            for mbid, offsets in low_level.items():
                for offset, data in offsets.items():
                    write_lowlevel(dest_dir, mbid, offset, data)

        if count % 1000 == 0:
            duration, remaining = time_stats(count, num_items, start)
            print('{}/{} elapsed {} remaining {}'.format(count, num_items, duration, remaining))

        # time.sleep(0.3)


def main(counts_file, dest_dir):
    print('loading mbids')
    mbids = get_mbids_from_counts_file(counts_file)
    print('filtering existing items')
    mbids = filter_mbids_from_destination(mbids, dest_dir)

    print('downloading files')
    get_lowlevel_for_all_and_save(mbids, dest_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download lowlevel files from AcousticBrainz')
    parser.add_argument('json_count', help='Json file with mbid counts')
    parser.add_argument('dest_dir', help='location to save lowlevel files to')
    args = parser.parse_args()
    main(args.json_count, args.dest_dir)
