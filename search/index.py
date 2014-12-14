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
    cur = conn.cursor()
    cur.execute("SELECT mbid, data::text FROM %s WHERE indexed IS NULL LIMIT 10" % tablename)
    items = cur.fetchall()
    toindex = []
    for mbid, data in items:
        data = json.loads(data)
        toindex.append(process(mbid, data))
    loaddata(indexname, toindex)


def loaddata(indexname, data):
    es = pyelasticsearch.ElasticSearch(config.ELASTICSEARCH_ADDRESS)
    if len(data):
        print es.bulk_index("acousticbrainz", indexname, data, id_field="mbid")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "create":
        recreate_index()
    else:
        print "run", sys.argv[0], "create, to (re)create index"
