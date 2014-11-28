import pyelasticsearch
es = pyelasticsearch.ElasticSearch("http://localhost:9200")

def autocomplete_genre(g):
    query = {"placeholder": {"text": term.lower(), "completion": {"field": "name_suggest"}}}
    completes = es._search_or_count('_suggest', query, index="acousticbrainz")
    if "placeholder" in completes:
        options = completes["placeholder"][0]["options"]
        options = sorted(options, key=lambda x: x["score"])
    else:
        options = []
    return [o["text"] for o in options]

def search_genre(g):
    pass

def recordings_for_genre(g):
    pass
