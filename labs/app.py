from flask import Flask
app = Flask("abzlabs")

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/genresug')
def suggest_genre():
    term = request.GET.get("term")
    ret = []
    if term:
        suggestions = util.autocomplete(term)
        ret = [{"id": i, "label": l, "value": l} for i, l in enumerate(suggestions, 1)]

if __name__ == '__main__':
    app.run()
