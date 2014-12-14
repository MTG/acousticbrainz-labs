import pyelasticsearch

import json
import os

#es.create_index("movies")
#self.es.bulk_index(self.INDEX_NAME, type, values)
# es.put_mapping("acousticbrainz", "lastfm")

def get_tempo(mbid):
    DATA_HOME = "/homedtic/sgulati/acousticbrainz-labs/stableTempoResults"
    fname = os.path.join(DATA_HOME, mbid[0:2], mbid[2:4], "%s.json" % mbid)
    if os.path.exists(fname):
        data = json.load(open(fname))
        data["mbid"] = mbid
        return data
    return None

def get_lowlevel(mbid):
    DATA_HOME = "/incoming/acousticbrainz"
    fname = os.path.join(DATA_HOME, mbid[0:2], mbid[2:4], "%s.json" % mbid)
    if os.path.exists(fname):
        data = json.load(open(fname))
        data["mbid"] = mbid
        # todo: work, releasegroup, albumartist
        tags = data["metadata"]["tags"]
        artist = tags.get("artist")
        artistid = tags.get("musicbrainz_artistid")
        album = tags.get("album")
        albumid = tags.get("musicbrainz_albumid")
        title = tags.get("title")
        recordingid = tags.get("musicbrainz_recordingid")
        if "album" in tags:
            tags["album_complete"] = {
                "input": album,
                "output": "%s - %s" % (artist, album)
                "payload" : { "mbid" : albumid } }

        return data
    return None

def get_highlevel(mbid):
    DATA_HOME = "/incoming/acousticbrainz-highlevel-json-20141119/highlevel"
    fname = os.path.join(DATA_HOME, mbid[0], mbid[0:2], mbid)
    if os.path.exists(fname):
        data = json.load(open(fname))
        m = os.path.splitext(mbid)[0][:-2]
        data["mbid"] = m
        return data
    return None

def get_lastfm(mbid):
    DATA_HOME = "/incoming/ab-mbid-toptags-structured"
    fname = os.path.join(DATA_HOME, mbid[0], mbid[0:2], "%s.json" % mbid)
    if os.path.exists(fname):
        try:
            data = json.load(open(fname))
            data["mbid"] = mbid
            tags = data["toptags"]
            if "tag" not in tags:
                # No tags, just metadata - move it
                attr = {"artist": tag.get("artist", ""), "track": tag.get("track", "")}
                tags = {"@attr": attr}
            else:
                t = tags["tag"]
                # If there's just 1 tag it's in the dict, not a list
                if isinstance(tags, dict):
                    tags = [tags]
            data["toptags"] = tags
            return data
        except ValueError:
            pass
    return None

def loaddata(lowlevel, lastfm, tempo, highlevel):
    es = pyelasticsearch.ElasticSearch("http://localhost:9200")
    if len(lowlevel):
        es.bulk_index("acousticbrainz", "lowlevel", lowlevel)
    if len(lastfm):
        es.bulk_index("acousticbrainz", "lastfm", lastfm)
    if len(tempo):
        es.bulk_index("acousticbrainz", "tempo", tempo)
    if len(highlevel):
        es.bulk_index("acousticbrainz", "highlevel", highlevel)

def main():
    #recordings = open("highlevel-mbids").readlines()
    recordings = open("abzrecordings.txt").readlines()
    recordings = [r.strip() for r in recordings]

    lowlevel = []
    highlevel = []
    lastfm = []
    tempo = []
    lrec = len(recordings)
    for i, r in enumerate(recordings[:2100], 1):
        if not r:
            continue
        #ll = get_lowlevel(r)
        #if ll:
        #    lowlevel.append(ll)
        lfm = get_lastfm(r)
        if lfm:
            lastfm.append(lfm)
        #tem = get_tempo(r)
        #if tem:
        #    tempo.append(tem)
        #hl = get_highlevel(r)
        #if hl:
        #    highlevel.append(hl)
        if i % 1000 == 0:
            print "%s/%s" % (i, lrec)
            loaddata(lowlevel, lastfm, tempo, highlevel)
            lowlevel = []
            lastfm = []
            tempo = []
            highlevel = []

    # Import last data
    loaddata(lowlevel, lastfm, tempo, highlevel)

if __name__ == "__main__":
    main()
