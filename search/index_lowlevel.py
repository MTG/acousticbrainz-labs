import index
import sys

def process(mbid, data):
        data["mbid"] = mbid
        # todo: work, releasegroup, albumartist
        tags = data["metadata"]["tags"]
        artist = tags.get("artist")
        artistid = tags.get("musicbrainz_artistid")
        album = tags.get("album")
        albumid = tags.get("musicbrainz_albumid")
        title = tags.get("title")
        recordingid = tags.get("musicbrainz_recordingid")
        if "album" in tags and artist and album:
            tags["album_complete"] = {
                "input": album,
                "output": "%s - %s" % (artist[0], album[0]),
                "payload" : { "mbid" : albumid } }
        if "artist" in tags:
            tags["artist_complete"] = {
                "input": artist,
                "output": artist,
                "payload" : { "mbid" : artistid } }
        if "title" in tags and artist and title:
            tags["title_complete"] = {
                "input": title,
                "output": "%s - %s" % (artist[0], title[0]),
                "payload" : { "mbid" : recordingid } }
        print title
        print artist
        return data

if __name__ == "__main__":
    name = "lowlevel"
    if len(sys.argv) > 1 and sys.argv[1] == "config":
        index.create_schema(schemafile="%s_index" % name, indexname=name)
    else:
        index.do_index(tablename=name, indexname=name, process=process)
