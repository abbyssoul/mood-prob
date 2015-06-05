import numpy as np


class Stats(object):
    """
    Run-time statistics of emotional fluctuation
    """

    def __init__(self, dim=3, max_semple_size=1024):
        self.min = np.zeros(dim)
        self.max = np.zeros(dim)
        self.mean = np.zeros(dim)
        self.M2 = np.zeros(dim)
        self.sample_size = 0

    def update(self, value):
        delta = value - self.mean

        self.sample_size += 1
        self.mean += (delta / self.sample_size)
        self.M2 += np.dot(delta, (value - self.mean))

        self.min = np.minimum(self.min, value)
        self.max = np.minimum(self.max, value)

    @property
    def variance(self):
        return (self.M2 / (self.sample_size - 1)) if self.sample_size > 1 else self.M2

    def __str__(self):
        return "{{'samples': {}, 'min': {}, 'max': {}, 'average': {}, 'variance': {}}}".format(
            self.sample_size, self.min, self.max, self.mean, self.variance)

