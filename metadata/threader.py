#!/usr/bin/env python

import sys
sys.path.append("../tempoStability")

import os
from time import sleep
import subprocess
import psycopg2
import config
from threading import Thread
import random
import argparse

DEFAULT_NUM_THREADS = 1

SLEEP_DURATION = 30 # number of seconds to wait between runs

class ComputationThread(Thread):
    """
        This thread calculates tempo stability of a track
    """

    def __init__(self, mbid, ll_data):
        Thread.__init__(self)
        self.mbid = mbid
        self.ll_data = ll_data

    def run(self):
        self._calculate()


def get_documents(conn, other):
    """
        Fetch a number of low level documents to process from the DB
    """
    cur = conn.cursor()
    # woo, I'm injecting arbitrary text into an sql query. There's no way this can go wrong
    cur.execute("""SELECT ll.mbid, ll.data::text
                     FROM lowlevel AS ll
                LEFT JOIN %s AS other
                       ON ll.mbid = other.mbid
                    WHERE other.mbid IS NULL
                    LIMIT 5""" % other)
    docs = cur.fetchall()
    cur.close()
    return docs


def main(num_threads, ThreadKlass):
    print "Processing daemon starting with %d threads" % num_threads

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
            docs = get_documents(conn, ThreadKlass.tablename)
            print "got", len(docs), "docs to process"

            # We will fetch some rows that are already in progress. Remove those.
            in_progress = pool.keys()
            filtered = []
            for mbid, doc in docs:
                if mbid not in in_progress:
                    filtered.append((mbid, doc))
            docs = filtered

        if len(docs):
            # Start one document
            mbid, doc = docs.pop()
            th = ThreadKlass(mbid, doc)
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
                    data = pool[mbid].data
                    pool[mbid].join()
                    del pool[mbid]

                    print "done  %s" % mbid
                    if not conn:
                        conn = psycopg2.connect(config.PG_CONNECT)

                    ThreadKlass.write_to_database(conn, mbid, data)

                    num_processed += 1

            if len(pool) == num_threads:
                # tranquilo!
                sleep(.1)
            else:
                break
