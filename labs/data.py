import psycopg2
import config

def get_meta_for_mbid(mbid):
    conn = psycopg2.connect(config.PG_CONNECT)
    cur = conn.cursor()
    cur.execute("SELECT data FROM lowlevel WHERE mbid = %s", (mbid, ))
    if cur.rowcount:
        data = cur.next()[0]
        tags = data["metadata"]["tags"]
        return {"artist": tags.get("artist", [None])[0],
                "title": tags.get("title", [None])[0]}
