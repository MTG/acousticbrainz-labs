import index
import sys

def process(mbid, data):
    tags = data["toptags"]
    data["mbid"] = mbid
    if "tag" not in tags:
        # No tags, just metadata - move it
        attr = {"artist": tags.get("artist", ""), "track": tags.get("track", "")}
        tags = {"@attr": attr}
    else:
        t = tags["tag"]
        # If there's just 1 tag it's in the dict, not a list
        if isinstance(tags, dict):
            tags = [tags]
    data["toptags"] = tags
    return data

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "config":
        index.create_schema(schemafile="lastfm_index", indexname="lastfm")
    else:
        index.do_index(tablename="lastfm", indexname="lastfm", process=process)
