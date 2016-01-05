#!/bin/env python2
# -*- coding: utf-8 -*-

import requests
import requests_cache
import json
import csv
import unicodedata
import cStringIO
import codecs
import argparse
import sqlite3
from urlparse import urlunparse
from urllib import urlencode

requests_cache.install_cache("msdtombidcache")

SEARCHSERVER_URL = "localhost:6502"

class DictUnicodeWriter(object):
    # From http://stackoverflow.com/a/5838817

    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        self.writer.writerow({k:v.encode("utf-8") for k,v in D.items()})
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()


#http://opensourceconnections.com/blog/2013/01/17/escaping-solr-query-characters-in-python/
# These rules all independent, order of
# escaping doesn't matter
escapeRules = {'+': r'\+',
               '-': r'\-',
               '&': r'\&',
               '|': r'\|',
               '!': r'\!',
               '(': r'\(',
               ')': r'\)',
               '{': r'\{',
               '}': r'\}',
               '[': r'\[',
               ']': r'\]',
               '^': r'\^',
               '~': r'\~',
               '*': r'\*',
               '?': r'\?',
               ':': r'\:',
               '"': r'\"',
               ';': r'\;',
               ' ': r'\ '}

def escapedSeq(term):
    """ Yield the next string based on the
        next character (either this char
        or escaped version """
    for char in term:
        if char in escapeRules.keys():
            yield escapeRules[char]
        else:
            yield char

def escapeSolrArg(term):
    """ Apply escaping to the passed in query terms
        escaping special characters like : , etc"""
    term = term.replace('\\', r'\\')   # escape \ first
    term = term.replace('"', r'\"')
    return term
    #return "".join([nextStr for nextStr in escapedSeq(term)])


def search(query):
    args = {"type": "recording",
             "fmt": "json",
             "query": query}

    newargs = []
    for key, value in sorted(args.items()):
        if isinstance(value, unicode):
            value = value.encode('utf8')
        newargs.append((key, value))

    url = urlunparse((
        'http',
        SEARCHSERVER_URL,
        '',
        '',
        urlencode(newargs),
        ''
    ))

    resp = requests.get(url)
    try:
        return resp.json()
    except ValueError:
        print resp.text
        return {}
    pass

def search_recording_artist(artist, title):
    # Perform a search using track name and artist name
    q = '"%s" AND artist:"%s"' % (escapeSolrArg(title), escapeSolrArg(artist))
    return search(q)


def search_recording_arid(artistid, title):
    # Perform a search using track name and artist musicbrainz id
    q = '"%s" AND arid:%s' % (escapeSolrArg(title), artistid)
    return search(q)


def fuzzy_equal(a, b):
    # compare 2 strings for equality by normalising to ascii (e.g. é->e)
    # and stripping all characters which are not [a-z]
    if isinstance(a, str):
        a = a.decode("utf-8")
    if isinstance(b, str):
        b = b.decode("utf-8")
    anorm = unicodedata.normalize('NFKD', a).encode('ascii', 'ignore')
    bnorm = unicodedata.normalize('NFKD', b).encode('ascii', 'ignore')

    astrip = filter(str.isalpha, anorm.lower())
    bstrip = filter(str.isalpha, bnorm.lower())

    return astrip == bstrip

def match_result(query, results):
    title = query["title"]
    artist = query["artist_name"]
    duration = int(float(query["duration"]))
    release = query["release"]

    match = {"query": query, "match": []}
    if results["recording-list"]["count"] == 0:
        return
    matchtype = ""
    matchduration = ""
    matchrelease = ""
    for recording in results["recording-list"]["recording"]:
        m = {"id": recording["id"],
             "title": recording["title"],
             "length": recording.get("length"),
             "artists": [],
             "releases": []}
        if recording["title"] == title:
            matchtype = "exact"
        elif fuzzy_equal(recording["title"], title):
            matchtype = "fuzzy"
        resdur = recording.get("length", 0) / 1000.0
        if duration > resdur * 0.9 and duration < resdur * 1.1:
            matchduration = "withindur"
        for artist in recording["artist-credit"]["name-credit"]:
            m["artists"].append({"id": artist["artist"]["id"], "name": artist["artist"]["name"]})
        for release in recording.get("release-list", {}).get("release", []):
            m["releases"].append({"id": release["id"], "title": release["title"]})
            if release["title"] ==  query["release"]:
                matchrelease == "release"
            elif fuzzy_equal(release["title"], query["release"]):
                matchrelease = "fuzzyrelease"
        match["match"].append(m)
    match["matchtypes"] = {"type": matchtype, "duration": matchduration, "release": matchrelease}
    return match


def match(infile, outfile):
    conn = sqlite3.connect(infile)
    cur = conn.execute("select track_id, title, song_id, release, artist_mbid, artist_name, duration from songs")

    results = []
    rows = cur.fetchall()
    size = len(rows)
    for i, row in enumerate(rows, 1):
        if i % 100 == 0:
            print "%s/%s" % (i, size)
        if i % 1000 == 0:
            print "  * saving"
            json.dump(results, open(outfile, "w"))
        data = {"track_id": row[0],
             "title": row[1],
             "song_id": row[2],
             "release": row[3],
             "artist_mbid": row[4],
             "artist_name": row[5],
             "duration": row[6]}
        artistid = data["artist_mbid"]
        title = data["title"]
        artist = data["artist_name"]
        if artistid:
            res = search_recording_arid(artistid, title)
        else:
            res = search_recording_artist(artist, title)

        res = match_result(data, res)
        if res:
            results.append(res)

    # Save last items
    json.dump(results, open(outfile, "w"))

def filter_results(input, filter_file, output):
    abmbids = set(open(filter_file).read().splitlines())
    data = json.load(open(input))

    newdata = []
    for row in data:
        matches = []
        for m in row["match"]:
            if m["id"] in abmbids:
                matches.append(m)
        if matches:
            row["matches"] = matches
            newdata.append(row)

    json.dump(newdata, open(output, "wb"))

def convert_csv(input, output):
    data = json.load(open(input))

    matches = []
    for row in data:
        for m in row["match"]:
            msd = row["query"]["track_id"]
            title = m["title"]
            artist = " and ".join([a["name"] for a in m["artists"]])
            matches.append( (msd, m["id"], title, artist) )

    dw = DictUnicodeWriter(open(output, "wb"), ["msdid", "mbid", "title", "artist"])
    for row in matches:
        dw.writerow({"msdid": row[0], "mbid": row[1], "title": row[2], "artist": row[3]})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Match MSD to MusicBrainz')
    subparsers = parser.add_subparsers(dest="mode")

    parser_match = subparsers.add_parser('match', help='Match MSD to MusicBrainz')
    parser_match.add_argument('track_metadata', type=str, help='MSD track_metadata file')
    parser_match.add_argument('output', type=str, help='Location to store results')

    parser_filter = subparsers.add_parser('filter', help='Filter results to a subset')
    parser_filter.add_argument('input', type=str, help='Input json file')
    parser_filter.add_argument('filter_file', type=str, help='File containing MBIDs to filter')
    parser_filter.add_argument('output', type=str, help='Output json file')

    parser_csv = subparsers.add_parser('csv', help='Convert json to csv')
    parser_csv.add_argument('input', type=str, help='Input json file')
    parser_csv.add_argument('output', type=str, help='Output csv file')

    args = parser.parse_args()
    mode = args.mode
    if mode == "match":
        match(args.track_metadata, args.output)
    elif mode == "filter":
        filter_results(args.input, args.filter_file, args.output)
    elif mode == "csv":
        convert_csv(args.input, args.output)

