from flask import Flask, request
from flask import render_template, jsonify
import json

import search
import data

app = Flask("abzlabs")
app.debug = True

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/genre/<g>')
def genre(g):
    matches = search.search_genre(g)
    ret = []
    for m in matches:
        d = data.get_meta_for_mbid(m)
        d["mbid"] = m
        ret.append(d)
    return render_template('genre.html', results=ret)

@app.route('/autocompletegenre')
def suggest_genre():
    term = request.args.get("term")
    ret = []
    if term:
        suggestions = search.autocomplete_genre(term)
        ret = [{"id": i, "label": l, "value": l} for i, l in enumerate(suggestions, 1)]
    return json.dumps(ret)

if __name__ == '__main__':
    app.run()
