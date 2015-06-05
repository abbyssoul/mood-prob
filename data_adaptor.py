from emotions import emotion
from itertools import groupby


def query_db(db, query, args=(), one=False):
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


class Emotions_ORM(object):

    def __init__(self, db):
        self.db = db

    def create_emotion(self, emotion_label, dim):

        res = query_db(self.db, 'INSERT INTO emotions (description, dimention_0, dimention_1, dimention_2) VALUES (?, ?, ?, ?);',
                       args=[emotion_label, dim[0], dim[1], dim[2]], one=True)
        return self.from_record(res)

    def fetch_emotions(self):
        emojis = query_db(self.db, "select * from emotions")
        if emojis is None:
            return None

        return [self.from_record(e) for e in emojis]

    def fetch_emotion(self, id):
        res = query_db(self.db, "select * from emotions where emotion_id=?", args=[id], one=True)
        return self.from_record(res)

    @classmethod
    def from_record(cls, record):
        return emotion.Emotion(record['description'],
                               [record['dimention_0'], record['dimention_1'], record['dimention_2']],
                               record['emotion_id']) if record is not None else record


class WordsData_ORM(object):

    def __init__(self, db):
        self.db = db

    def fetch_word(self, word):
        entries = query_db(self.db, "select * from entries NATURAL JOIN emotions where entries.word=? ", args=(word,))
        # entries = query_db("select * from entries JOIN emotions where word=? and ", args=(word,))
        if entries is None:
            return None

        return {word: [(e['power'], Emotions_ORM.from_record(e)) for e in entries]}

    def fetch_all(self):
        entries = query_db(self.db, "select * from entries NATURAL JOIN emotions")
        if entries is None:
            return None

        result = {}
        for key, group in groupby(entries, lambda x: x['word']):
            if key not in result:
                result[key] = [Emotions_ORM.from_record(emotion_entry) for emotion_entry in group]
            else:
                result[key].expand([Emotions_ORM.from_record(emotion_entry) for emotion_entry in group])

        return result

    def create_entry(self, word, emotions):
        for emotion_id, power in emotions.iteritems():
            res = query_db(self.db, 'INSERT INTO entries (word, emotion_id, power) VALUES (?, ?, ?);',
                           args=[word, emotion_id, power], one=True)
