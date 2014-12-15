import config
import pyelasticsearch
import json
import sys
import psycopg2

def recreate_index():
    index = "acousticbrainz"
    es = pyelasticsearch.ElasticSearch(config.ELASTICSEARCH_ADDRESS)
    try:
        es.delete_index(index)
    except pyelasticsearch.ElasticHttpNotFoundError:
        pass
    es.create_index(index)

def create_schema(schemafile, indexname):
    es = pyelasticsearch.ElasticSearch(config.ELASTICSEARCH_ADDRESS)
    schema = json.load(open(schemafile))
    es.put_mapping("acousticbrainz", indexname, schema)

def do_index(tablename, indexname, process):
    conn = psycopg2.connect(config.PG_CONNECT)
    while True:
        print "processing 100..."
        cur = conn.cursor()
        cur.execute("SELECT mbid, data FROM %s WHERE indexed IS NULL LIMIT 100" % tablename)
        if cur.rowcount == 0:
            print "no more to do"
            break
        items = cur.fetchall()
        cur.close()
        toindex = []
        for mbid, data in items:
            #data = json.loads(data)
            toindex.append(process(mbid, data))
        loaddata(indexname, toindex)
        cur = conn.cursor()
        for mbid, data in items:
            cur.execute("UPDATE %s SET indexed=now() WHERE mbid=%%s" % tablename, (mbid, ))
        conn.commit()


def loaddata(indexname, data):
    es = pyelasticsearch.ElasticSearch(config.ELASTICSEARCH_ADDRESS)
    if len(data):
        es.bulk_index("acousticbrainz", indexname, data, id_field="mbid")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "create":
        recreate_index()
    else:
        print "run", sys.argv[0], "create, to (re)create index"
