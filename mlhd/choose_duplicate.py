
import argparse
import collections
import logging
import glob
import json
import os
import shutil
import time

from typing import List, Tuple

from requests.adapters import HTTPAdapter
import requests
from urllib3 import Retry

import util

log = logging.Logger('lookup')
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
log.setLevel(logging.INFO)
log.addHandler(ch)


ret = Retry(total=10, backoff_factor=0.2)
adaptor = HTTPAdapter(max_retries=ret)
req_session = requests.Session()
req_session.mount('http://', adaptor)
req_session.mount('https://', adaptor)


def get_mb_releases_for_recording(recording_id):
    url = 'https://musicbrainz.org/ws/2/release'
    params = {'recording': recording_id,
              'inc': 'recordings',
              'fmt': 'json'}
    headers = {'User-Agent': 'Acousticbrainz/1.0'}
    r = req_session.get(url, params=params, headers=headers)
    time.sleep(0.1)
    r.raise_for_status
    return r.json()


def get_mb_tracks_from_release_list(recording_id):
    releases = get_mb_releases_for_recording(recording_id)
    if 'error' in releases:
        return []
    releases = releases['releases']
    tracks = []
    for r in releases:
        for m in r.get('media', []):
            for t in m.get('tracks', []):
                r = t['recording']
                if r['id'] == recording_id:
                    tracks.append(t)
    return tracks


def get_recording_length_from_tracks(tracks):
    # If the recording itself has a length, return that (in seconds)
    for t in tracks:
        rlength = t['recording'].get('length')
        if rlength:
            return rlength / 1000
    return None


def get_track_lengths_from_tracks(tracks):
    pass

def remove_bad_durations_with_musicbrainz(files):
    if not files:
        return None
    filename = files[0][0]
    filename = os.path.basename(filename)
    mbid, ext = os.path.splitext(filename)
    mbid = mbid.rsplit('-', 1)[0]
    tracks = get_mb_tracks_from_release_list(mbid)
    length = get_recording_length_from_tracks(tracks)
    if length is None:
        return None

    keep = []
    for n, d in files:
        l = d["metadata"]["audio_properties"]["length"]
        if l < length -5 or l > length + 5:
            pass
        else:
            keep.append((n, d))
    if keep:
        return keep
    else:
        return None



def mbid_dirname(mbid):
    return os.path.join(mbid[:2], mbid[2:4])


def find_one(files: List[Tuple[str, dict]]):
    # files: list of (filename, data)
    # returns filename
    # Sort by integer of the duplicate
    # This means that mbid redirects with different mbids will be interleaved
    # but we don't have the exact submission dates to put them in the right order
    files.sort(key=lambda x: int(os.path.splitext(x[0])[0].split("-")[-1]))
    newfiles = remove_bad_durations(files)

    if not newfiles:
        files = remove_bad_durations_with_musicbrainz(files)

    if not files:
        return None

    flac = find_first_flac(files)
    if flac:
        return flac

    first = find_first_lossless(files)
    if first:
        return first

    bitrate = find_highest_bitrate(files)
    if bitrate:
        return bitrate

    return None


def find_first_flac(files):
    # returns filename
    flacs = [n for n, d in files if d["metadata"]["audio_properties"]["codec"] == "flac"]
    if flacs:
        return flacs[0]
    else:
        return None


def find_first_lossless(files):
    lossless_codecs = ("flac", "alac", "ape")
    lossless = [n for n, d in files if d["metadata"]["audio_properties"]["codec"] in lossless_codecs]
    if lossless:
        return lossless[0]
    else:
        return None


def find_highest_bitrate(files):
    # Given a list of files, prefer a vorbis then an mp3, then an aac
    # If there is more than one of these types, pick the one with the
    # highest bitrate
    files.sort(key=lambda x: x[1]["metadata"]["audio_properties"]["bit_rate"])
    groups = collections.defaultdict(list)
    for fn, data in files:
        codec = data["metadata"]["audio_properties"]["codec"]
        groups[codec].append(fn)

    for codec in ['vorbis', 'mp3', 'aac']:
        files = groups[codec]
        if files:
            return files[0]

    return None

def remove_bad_durations(files):
    lengths = [d["metadata"]["audio_properties"]["length"] for n, d in files]
    meanlength = float(sum(lengths)) / max(len(lengths), 1)
    keep = []
    for n, d in files:
        l = d["metadata"]["audio_properties"]["length"]
        if l < meanlength -5 or l > meanlength + 5:
            pass
        else:
            keep.append((n, d))
    if keep:
        return keep
    else:
        return None


def copy_file(fname, outputdir, mbid):
    outputdir = os.path.join(outputdir, mbid_dirname(mbid))
    util.mkdir_p(outputdir)
    shutil.copy(fname, os.path.join(outputdir, "{}.json".format(mbid)))


def main(inputdir, outputdir, mbidfile):
    mbids = open(mbidfile).read().splitlines()

    done = 0
    total = len(mbids)
    starttime = time.time()

    for m in mbids:
        process_one(inputdir, outputdir, m)
        done += 1
        if done % 1000 == 0:
            durdelta, remdelta = util.stats(done, total, starttime)
            log.info("Done %s/%s in %s; %s remaining", done, total, str(durdelta), str(remdelta))

def process_one(inputdir, outputdir, m):
        sourcedir = os.path.join(inputdir, mbid_dirname(m))
        # Get number of files
        # - if only 1, just copy it
        # - if more than 1, do stats
        files = glob.glob(os.path.join(sourcedir, '{}*.json'.format(m)))
        if len(files) == 1:
            copy_file(os.path.join(sourcedir, files[0]), outputdir, m)
        else:
            data = []
            for f in files:
                try:
                    data.append((f, json.load(open(os.path.join(sourcedir, f)))))
                except ValueError:
                    pass
                    #log.debug("bad file %s", f)

            good = find_one(data)
            if not good:
                #log.info("NO MATCH :( %s", m)
                pass
            else:
                copy_file(os.path.join(sourcedir, good), outputdir, m)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', required=False)
    parser.add_argument("inputdir")
    parser.add_argument("outputdir")
    parser.add_argument("mbidlist")

    args = parser.parse_args()

    if args.s:
        process_one(args.inputdir, args.outputdir, args.s)
    else:
        main(args.inputdir, args.outputdir, args.mbidlist)
