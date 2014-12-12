#!/usr/bin/env python

import sys
sys.path.append("../tempoStability")

import urllib2
import json
import os
from time import sleep
import subprocess
from operator import itemgetter
import psycopg2
import config
from threading import Thread
import random
from hashlib import sha256, sha1
import tempfile
import yaml
import argparse

DEFAULT_NUM_THREADS = 1

SLEEP_DURATION = 30 # number of seconds to wait between runs

class ClickTrack(Thread):
    """
        This thread calculates tempo stability of a track
    """

    def __init__(self, mbid, ll_data):
        Thread.__init__(self)
        self.mbid = mbid
        self.ll_data = ll_data

    def _calculate(self):
        self.data = ''

    def run(self):
        self._calculate()

class LastFm(Thread):
    """
        This thread gets tag and metadata from lastfm
    """

    def __init__(self, mbid, ll_data):
        Thread.__init__(self)
        self.mbid = mbid
        self.ll_data = ll_data

    def _calculate(self):
        """
           Invoke essentia high level extractor and return its JSON output
        """


        self.tags = ''
        self.info = ''

    def run(self):
        self._calculate()

def get_documents(conn):
    """
        Fetch a number of low level documents to process from the DB
    """
    cur = conn.cursor()
    cur.execute("""SELECT ll.mbid, ll.data::text, ll.id
                     FROM lowlevel AS ll
                LEFT JOIN highlevel AS hl
                       ON ll.id = hl.id
                    WHERE hl.mbid IS NULL
                    LIMIT 100""")
    docs = cur.fetchall()
    cur.close()
    return docs



def main(num_threads):
    print "High level extractor daemon starting with %d threads" % num_threads

    conn = None
    num_processed = 0

    pool = {}
    docs = []
    while True:
        # Check to see if we need more database rows
        if len(docs) == 0:
            # Fetch more rows from the DB
            if not conn:
                conn = psycopg2.connect(config.PG_CONNECT)
            docs = get_documents(conn)

            # We will fetch some rows that are already in progress. Remove those.
            in_progress = pool.keys()
            filtered = []
            for mbid, doc, id in docs:
                if mbid not in in_progress:
                    filtered.append((mbid, doc, id))
            docs = filtered

        if len(docs):
            # Start one document
            mbid, doc, id = docs.pop()
            th = HighLevel(mbid, doc, id)
            th.start()
            print "start %s" % mbid
            pool[mbid] = th

        # If we're at max threads, wait for one to complete
        while True:
            if len(pool) == 0 and len(docs) == 0:
                if num_processed > 0:
                    print "processed %s documents, none remain. Sleeping." % num_processed
                num_processed = 0
                # Let's be nice and not keep any connections to the DB open while we nap
                conn.close()
                conn = None
                sleep(SLEEP_DURATION)

            for mbid in pool.keys():
                if not pool[mbid].is_alive():

                    # Fetch the data and clean up the thread object
                    hl_data = pool[mbid].get_data()
                    ll_id = pool[mbid].get_ll_id()
                    pool[mbid].join()
                    del pool[mbid]

                    # Calculate the sha for the data
                    try:
                        jdata = json.loads(hl_data)
                    except ValueError:
                        print "error %s: Cannot parse result document" % mbid
                        print hl_data
                        jdata = {}

                    norm_data = json.dumps(jdata, sort_keys=True, separators=(',', ':'))
                    sha = sha256(norm_data).hexdigest()

                    print "done  %s" % mbid
                    if not conn:
                        conn = psycopg2.connect(config.PG_CONNECT)

                    cur = conn.cursor()
                    cur.execute("""INSERT INTO highlevel_json (data, data_sha256)
                                        VALUES (%s, %s)
                                     RETURNING id""", (norm_data, sha))
                    id = cur.fetchone()[0]
                    cur.execute("""INSERT INTO highlevel (id, mbid, build_sha1, data, submitted)
                                        VALUES (%s, %s, %s, %s, now())""", (ll_id, mbid, build_sha1, id))
                    conn.commit()
                    num_processed += 1

            if len(pool) == num_threads:
                # tranquilo!
                sleep(.1)
            else:
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract high level data from lowlevel data')
    parser.add_argument("-t", "--threads", help="Number of threads to start", default=DEFAULT_NUM_THREADS, type=int)
    args = parser.parse_args()
    main(args.threads)
