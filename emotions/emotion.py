import json


class Emotion(object):
    """ Representation of a single emotion
    """
    def __init__(self, desc, dim, id=-1):
        self.description = desc
        self.dim = dim
        self.id = id

    def __str__(self):
        return self.description

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
