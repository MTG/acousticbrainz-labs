import pyelasticsearch
es = pyelasticsearch.ElasticSearch("http://localhost:9200")

def autocomplete_genre(g):
    query = {"placeholder": {"text": g.lower(), "completion": {"field": "toptags.tag.name_complete"}}}
    completes = es._search_or_count('_suggest', query, index="acousticbrainz")
    if "placeholder" in completes:
        options = completes["placeholder"][0]["options"]
        options = sorted(options, key=lambda x: x["score"])
    else:
        options = []
    return [o["text"] for o in options]

def search_genre(g):
    query = {"query": {
                "filtered":{
                    "filter":{
                        "term":{
                            "toptags.tag.name.raw":g.lower()}
                        }
                    }
                }
            }
    result = es.search(query=query, doc_type="lastfm", index="acousticbrainz")
    h = result["hits"]["hits"]
    return [x["_id"] for x in h]

def recordings_for_genre(g):
    pass
