#!/usr/bin/env python

import psycopg2
import sys
import os
import json

PG_CONNECT = "dbname=acousticbrainz"

def main(destination):
    conn = psycopg2.connect(PG_CONNECT)

    noname = conn.cursor()
    noname.execute("select mbid from lowlevel")
    print "getting tot"
    total = noname.rowcount
    print "total", total
    q = "select mbid, data::text as data from lowlevel"
    cur = conn.cursor('lowlevelnamed')
    cur.execute(q)
    i = 0
    for x in cur:
        i+= 1
        if i % 100 == 0:
            sys.stdout.write(".")
            sys.stdout.flush()
        if i % 10000 == 0:
            print " %s/%s" % (i, total)
        mbid, data = x
        dname = os.path.join(destination, mbid[:2], mbid[2:4])
        fname = "%s.json" % mbid
        try:
            os.makedirs(dname)
        except OSError as e:
            if e.errno == 17:
                pass # already exists
            else:
                raise
        with open(os.path.join(dname, fname), "w") as fp:
            #json.dump(data, fp)
            fp.write(data)
    print ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print >>sys.stderr, "Usage: %s [dest dir]"
        sys.exit(1)
    main(sys.argv[1])
