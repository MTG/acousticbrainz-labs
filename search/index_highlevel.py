import index
import config
import sys
import json
import psycopg2

def process(mbid, data):
        data["mbid"] = mbid
        return data

def do_index(tablename, indexname, process):
    conn = psycopg2.connect(config.PG_CONNECT)
    while True:
        print "processing 1000..."
        cur = conn.cursor()
        cur.execute("SELECT h.mbid, j.data FROM highlevel h INNER JOIN highlevel_json j ON h.data=j.id WHERE h.indexed IS NULL LIMIT 1000")
        if cur.rowcount == 0:
            print "no more to do"
            break
        items = cur.fetchall()
        cur.close()
        toindex = []
        for mbid, data in items:
            #data = json.loads(data)
            toindex.append(process(mbid, data))
        index.loaddata(indexname, toindex)
        cur = conn.cursor()
        for mbid, data in items:
            cur.execute("UPDATE highlevel SET indexed=now() WHERE mbid=%s", (mbid, ))
        conn.commit()

if __name__ == "__main__":
    name = "lowlevel"
    if len(sys.argv) > 1 and sys.argv[1] == "config":
        index.create_schema(schemafile="%s_index" % name, indexname=name)
    else:
        do_index(tablename=name, indexname=name, process=process)
