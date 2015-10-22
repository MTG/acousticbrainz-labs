from flask import Flask, request
from flask import render_template, jsonify
import json

import search
import data

app = Flask("abzlabs", static_url_path="/static", static_folder="static")
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

@app.route('/artist/<name>')
def artist(name):
    matches = search.search_tracks_for_artist(name)
    ret = []
    for m in matches:
        d = data.get_meta_for_mbid(m)
        d["mbid"] = m
        ret.append(d)
    return render_template('artist.html', data=ret)


@app.route('/track/<mbid>')
def track(mbid):
    d = data.get_meta_for_mbid(mbid)
    btdata = data.get_click_for_mbid(mbid)
    bt = json.dumps(btdata)
    genres, estimated = data.get_genre(mbid)
    genre = data.tag(mbid)
    return render_template('track.html', data=d, beattrack=bt, mbid=mbid, genres=genres, genre=genre, estimated=estimated)

@app.route('/bpm-source')
def range():
    f = request.args.get("range_from")
    to = request.args.get("range_to")
    ret = search.search_bpm_range(f,to)
    
    #ret = [{"id": i, "label": l, "value": l} for i, l in enumerate(ret, 1)]
    return json.dumps(ret)


@app.route('/autocompletegenre')
def suggest_genre():
    term = request.args.get("term")
    ret = []
    if term:
        suggestions = search.autocomplete_genre(term)
        ret = [{"id": i, "label": l, "value": l} for i, l in enumerate(suggestions, 1)]
    return json.dumps(ret)

@app.route('/autocompleteartist')
def suggest_artist():
    term = request.args.get("term")
    ret = []
    if term:
        suggestions = search.autocomplete_artist(term)
        ret = [{"id": i, "label": l, "value": l} for i, l in enumerate(suggestions, 1)]
    return json.dumps(ret)


@app.route('/autocompletetrack')
def suggest_track():
    term = request.args.get("term")
    ret = []
    if term:
        suggestions = search.autocomplete_track(term)
        ret = [{"id": i, "label": l[0], "value": l[1]} for i, l in enumerate(suggestions, 1)]
    return json.dumps(ret)

if __name__ == '__main__':
    app.run()
