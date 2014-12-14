
def process(mbid, data)
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
                "output": "%s - %s" % (artist, album),
                "payload" : { "mbid" : albumid } }
        if "artist" in tags:
            tags["artist_complete"] = {
                "input": artist,
                "output": artist,
                "payload" : { "mbid" : artistid } }
        if "title" in tags:
            tags["title_complete"] = {
                "input": title,
                "output": "%s - %s" % (artist, title),
                "payload" : { "mbid" : recordingid } }

        return data
