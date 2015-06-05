# coding=utf-8
from parser import EmojiParser
from stats import Stats

import numpy as np
from numpy import linalg



class Intelligence(object):
    """
    Emotion Intelligence of an entity
    Based on Lövheim Cube of emotion:

    Shame/humiliation	Low	Low	Low
    Distress/anguish	Low	Low	High
    Fear/terror	Low	High	Low
    Anger/rage	Low	High	High
    Contempt/disgust	High	Low	Low
    Surprise	High	Low	High
    Enjoyment/Joy	High	High	Low
    Interest/excitement	High	High	High
    """

    def __init__(self, name, emotion_parser):
        self.name = name
        self.parser = emotion_parser
        self.threshold = 1.0
        self.stats = Stats()

    def update(self, text):
        """
        Update emotional state of an entity

        :param text: Emotionally charged text that entity produced
        :return: self
        """

        for emoji, power in self.parser.get_emojis(text):
            emoji_dir = np.array(emoji.dim)
            self.stats.update(power * emoji_dir / np.linalg.norm(emoji_dir))

        return self

    def emotions(self):
        emo = []

        emo_point = np.array(self.stats.mean)

        for k, emotion in self.parser.known_emotions.iteritems():
            emo_origin = np.array(emotion.dim)
            dist = np.linalg.norm(emo_point - emo_origin)
            if dist < self.threshold:
                emo.append((emotion,
                            dist))

        return emo
