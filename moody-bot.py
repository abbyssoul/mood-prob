import json
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify, Response

from emotions import parser
from data_adaptor import Emotions_ORM, WordsData_ORM

app = Flask(__name__)
app.config.from_object("config")


def connect_db(app):
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db

@app.before_request
def before_request():
    g._database = connect_db(app)

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/emotions/', methods=['GET', 'POST'])
@app.route('/emotions/<id>', methods=['GET'])
def emotions(id=None):
    if request.method == 'POST':
        emotion_label = request.form['name']
        dim = [request.form['dim_0'], request.form['dim_1'], request.form['dim_2']]

        emos = Emotions_ORM(get_db()).create_emotion(emotion_label, dim)
        resp = json.dumps(emos.__dict__ if emos else None)

    elif request.method == 'GET':
        if id is not None:
            emos = Emotions_ORM(get_db()).fetch_emotion(id)
            resp = json.dumps(emos.__dict__ if emos else None)
        else:
            emos = Emotions_ORM(get_db()).fetch_emotions()
            resp = json.dumps([ e.__dict__ for e in emos])

    return Response(response=resp,
             status=200,
             mimetype="application/json")


@app.route('/words/', methods=['GET', 'POST'])
def words():
    if request.method == 'POST':
        word = request.form['word']
        emotions_power = request.json
        if emotions_power is None:
            abort(400)
        else:
            emos = WordsData_ORM(get_db()).create_entry(word, emotions_power)

            return render_template('form_action.html', word=word, emotions=emos)

    else:  # Handle GET
        emos = WordsData_ORM(get_db()).fetch_all()
        resp = json.dumps({k: [e.__dict__ for e in v] for k, v in emos.iteritems()})
        return Response(response=resp,
                        status=200,
                        mimetype="application/json")


# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    ep = parser.EmojiParser()
    print "Known emotions: {}".format([e for e in ep.known_emotions.iteritems()])
    return render_template('form_submit.html', emotions=[e for k, e in ep.known_emotions.iteritems()])

if __name__ == '__main__':
    app.debug = True
    app.run()
