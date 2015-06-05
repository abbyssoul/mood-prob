# from textblob import TextBlob
from nltk.stem import WordNetLemmatizer

from emotion import Emotion

class EmojiParser(object):
    """ Maps phrases and words into emotions
    """

    def __init__(self):
        self.known_emotions = {
            'Shame':        Emotion("Shame",        [-1.0, -1.0, -1.0], 1),
            'Distress':     Emotion("Distress",     [-1.0, -1.0, 1.0], 2),
            'Terror':       Emotion("Terror",       [-1.0, 1.0, -1.0], 3),
            'Anger':        Emotion("Anger",        [-1.0, 1.0, 1.0], 4),
            'Contempt':     Emotion("Contempt",     [1.0, -1.0, -1.0], 5),
            'Surprise':     Emotion("Surprise",     [1.0, -1.0, 1.0], 6),
            'Joy':          Emotion("Joy",          [1.0, 1.0, -1.0], 7),
            'Excitement':   Emotion("Excitement",   [1.0, 1.0, 1.0], 8),
        }

        self.__data = {
            'shame':        [("Shame", 0.8)],
            'distress':     [("Distress", 0.8)],
            'terror':       [("Terror", 0.8)],
            'anger':        [("Anger", 0.8)],
            'contempt':     [("Contempt", 0.8)],
            'surprise':     [("Surprise", 0.8)],
            'joy':          [("Joy", 0.8)],
            'excitement':   [("Excitement", 0.8)],

            # 'understanding': [('Joy', 0.3)],
            # 'great': [('Joy', 0.5), ('Excitement', 0.5)],
            # 'angry': [('Anger', 0.8), ('Excitement', 0.2)],
            #
            # 'irritated': [('Anger', 0.8), ('Excitement', 0.2)],
            # 'lousy': [('Anger', 0.1), ('Distress', 0.2)],
            # 'upset': [('Anger', 0.1), ('Distress', 0.2)],
            # 'incapable': [('Anger', 0.1), ('Distress', 0.2)],
            # 'enraged': [('Anger', 0.1), ('Distress', 0.2)],
            # 'disappointed': [('Anger', 0.1), ('Distress', 0.2)],
            # 'doubtful': [('Anger', 0.1), ('Distress', 0.2)],
            # 'alone': [('Anger', 0.1), ('Distress', 0.2)],
            # 'hostile': [('Anger', 0.1), ('Distress', 0.2)],
            # 'discouraged': [('Anger', 0.1), ('Distress', 0.2)],
            # 'uncertain': [('Anger', 0.1), ('Distress', 0.2)],
            # 'paralyzed': [('Anger', 0.1), ('Distress', 0.2)],
            # 'insulting': [('Anger', 0.1), ('Distress', 0.2)],
            # 'ashamed': [('Shame', 0.8)],
            # 'indecisive': [('Anger', 0.1), ('Distress', 0.2)],
            # 'fatigued': [('Anger', 0.1), ('Distress', 0.2)],
            # 'sore': [('Anger', 0.1), ('Distress', 0.2)],
            # 'powerless': [('Anger', 0.1), ('Distress', 0.2)],
            # 'perplexed': [('Anger', 0.1), ('Distress', 0.2)],
            # 'useless': [('Anger', 0.1), ('Distress', 0.2)],
            # 'annoyed': [('Anger', 0.1), ('Distress', 0.2)],
            # 'diminished': [('Anger', 0.1), ('Distress', 0.2)],
            # 'embarrassed': [('Anger', 0.1), ('Distress', 0.2)],
            # 'inferior': [('Anger', 0.1), ('Distress', 0.2)],
            # 'upset': [('Anger', 0.1), ('Distress', 0.2)],
            # 'guilty': [('Anger', 0.1), ('Distress', 0.2)],
            # 'hesitant': [('Anger', 0.1), ('Distress', 0.2)],
            # 'vulnerable': [('Anger', 0.1), ('Distress', 0.2)],
            # 'hateful': [('Anger', 0.1), ('Distress', 0.2)],
            # 'dissatisfied': [('Anger', 0.1), ('Distress', 0.2)],
            # 'shy': [('Anger', 0.1), ('Distress', 0.2)],
            # 'empty': [('Anger', 0.1), ('Distress', 0.2)],
            # 'unpleasant': [('Anger', 0.1), ('Distress', 0.2)],
            # 'miserable': [('Anger', 0.1), ('Distress', 0.2)],
            # 'stupefied': [('Anger', 0.1), ('Distress', 0.2)],
            # 'forced': [('Anger', 0.1), ('Distress', 0.2)],
            # 'offensive': [('Anger', 0.1), ('Distress', 0.2)],
            # 'detestable': [('Anger', 0.1), ('Distress', 0.2)],
            # 'disillusioned': [('Anger', 0.1), ('Distress', 0.2)],
            # 'hesitant': [('Anger', 0.1), ('Distress', 0.2)],
            # 'bitter': [('Anger', 0.1), ('Distress', 0.2)],
            # 'repugnant': [('Anger', 0.1), ('Distress', 0.2)],
            # 'unbelieving': [('Anger', 0.1), ('Distress', 0.2)],
            # 'despair': [('Anger', 0.1), ('Distress', 0.2)],
            # 'aggressive': [('Anger', 0.1), ('Distress', 0.2)],
            # 'despicable': [('Anger', 0.1), ('Distress', 0.2)],
            # 'skeptical': [('Anger', 0.1), ('Distress', 0.2)],
            # 'frustrated': [('Anger', 0.1), ('Distress', 0.2)],
            # 'resentful': [('Anger', 0.1), ('Distress', 0.2)],
            # 'disgusting': [('Anger', 0.1), ('Distress', 0.2)],
            # 'distrustful': [('Anger', 0.1), ('Distress', 0.2)],
            # 'distressed': [('Anger', 0.1), ('Distress', 0.2)],
            # 'inflamed': [('Anger', 0.1), ('Distress', 0.2)],
            # 'abominable': [('Anger', 0.1), ('Distress', 0.2)],
            # 'misgiving': [('Anger', 0.1), ('Distress', 0.2)],
            # 'woeful': [('Anger', 0.1), ('Distress', 0.2)],
            # 'provoked': [('Anger', 0.1), ('Distress', 0.2)],
            # 'terrible': [('Anger', 0.1), ('Distress', 0.2)],
            # 'lost': [('Anger', 0.1), ('Distress', 0.2)],
            # 'pathetic': [('Anger', 0.1), ('Distress', 0.2)],
            # 'incensed': [('Anger', 0.1), ('Distress', 0.2)],
            # 'in despair': [('Anger', 0.1), ('Distress', 0.2)],
            # 'unsure': [('Anger', 0.1), ('Distress', 0.2)],
            # 'tragic': [('Anger', 0.1), ('Distress', 0.2)],
            # 'infuriated': [('Anger', 0.1), ('Distress', 0.2)],
            # 'sulky': [('Anger', 0.1), ('Distress', 0.2)],
            # 'uneasy': [('Anger', 0.1), ('Distress', 0.2)],
            # 'in a stew': [('Anger', 0.1), ('Distress', 0.2)],
            # 'cross': [('Anger', 0.1), ('Distress', 0.2)],
            # 'bad': [('Anger', 0.1), ('Distress', 0.2)],
            # 'pessimistic': [('Anger', 0.1), ('Distress', 0.2)],
            # 'dominated': [('Anger', 0.1), ('Distress', 0.2)],
            # 'worked up': [('Anger', 0.1), ('Distress', 0.2)],
            # 'a sense of loss': [('Anger', 0.1), ('Distress', 0.2)],
            # 'tense': [('Anger', 0.1), ('Distress', 0.2)],
            # 'boiling': [('Anger', 0.1), ('Distress', 0.2)],
            # 'fuming': [('Anger', 0.1), ('Distress', 0.2)],
            # 'indignant': [('Anger', 0.1), ('Distress', 0.2)],
        }

    def get_emojis(self, text):
        """
        Get emotions expressed in the text
        :param text: The emotionally charged text
        :return: Emotions and their power
        """

        lemmatizer = WordNetLemmatizer()
        words = text.split()

        emojis_in_text = []
        for word in words:
            try:
                clean_word = word.strip().lower()
                canonical_repr = lemmatizer.lemmatize(clean_word)
                emojis = self.__data.get(canonical_repr, [])
                for emoji, power in emojis:
                    emojis_in_text.append((self.known_emotions[emoji], power))
            except:
                pass

        return emojis_in_text
