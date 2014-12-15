import psycopg2
import config
from operator import itemgetter

import json
gt = json.load(open("groundtruth.json"))

def get_meta_for_mbid(mbid):
    conn = psycopg2.connect(config.PG_CONNECT)
    cur = conn.cursor()
    cur.execute("SELECT data FROM lowlevel WHERE mbid = %s", (mbid, ))
    if cur.rowcount:
        data = cur.next()[0]
        tags = data["metadata"]["tags"]
        return {"artist": tags.get("artist", [None])[0],
                "title": tags.get("title", [None])[0]}

def get_click_for_mbid(mbid):
    conn = psycopg2.connect(config.PG_CONNECT)
    cur = conn.cursor()
    cur.execute("SELECT data FROM tempo WHERE mbid = %s", (mbid, ))
    if cur.rowcount:
        data = cur.next()[0]
        time, val = data["tempoCurve"]
        data = {"labels": time, "datasets": [{"data": val}]}
        return data
    return {}

def get_genre(mbid):
    conn = psycopg2.connect(config.PG_CONNECT)
    cur = conn.cursor()
    cur.execute("""SELECT hlj.data
                     FROM modeltest hl
                     JOIN modeltest_json hlj
                       ON hl.data = hlj.id
                    WHERE mbid = %s""", (str(mbid), ))
    if not cur.rowcount:
        return [], None

    row = cur.fetchone()
    d = row[0]
    if d:
        genres = d["highlevel"]["mbgenre-PERRELEASE-trunc"]["all"]
        estimated = d["highlevel"]["mbgenre-PERRELEASE-trunc"]["value"]
        g = []
        for k, v in genres.items():
            g.append({"class": k, "probability": v})
        print g
        return sorted(g, key=itemgetter("probability"), reverse=True), estimated
    else:
        return [], None

def tag(mbid):
    return gt["groundTruth"].get(mbid)
