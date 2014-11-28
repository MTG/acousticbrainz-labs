#!/usr/bin/env python

# Calculate the year that an album with recordings were first released
# TODO: For art music recordings, it would be nice to
#       get the date the work was composed instead

import sys
import json

import mb

def earliest_year_for_recording(mbid):
    recording = mb.get_recording(mbid)
    releases = recording.get("release-list", [])
    years = []
    for r in releases:
        mbrel = mb.get_release(r["id"])
        rg = mbrel.get("release-group", {})
        firstyear = rg.get("first-release-date")
        if firstyear and len(firstyear) >= 4:
            years.append(firstyear[:4])
    years.sort()
    if years:
        return years[0]
    else:
        return 0

def main(input, output):
    recordings = {}
    infile = open(input)
    for i, l in enumerate(infile.readlines(), 1):
        # if i % 100 == 0:
        #     sys.stdout.write(".")
        #     sys.stdout.flush()
        if i % 100000 == 0:
            json.dump(recordings, open(output, "w"))
            print " %d" % (i, )
        l = l.strip()
        year = earliest_year_for_recording(l)
        if year:
            print l, "", year
            recordings[l] = year
    json.dump(recordings, open(output, "w"))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print >> sys.stderr, "Usage: %s input output" % sys.argv[0]
    main(sys.argv[1], sys.argv[2])
