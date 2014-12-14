import sys
import index

def process(mbid, data):
    data["mbid"] = mbid
    del data["tempoCurve"]
    return data

if __name__ == "__main__":
    name = "tempo"
    if len(sys.argv) > 1 and sys.argv[1] == "config":
        index.create_schema(schemafile="%s_index" % name, indexname=name)
    else:
        index.do_index(tablename=name, indexname=name, process=process)
