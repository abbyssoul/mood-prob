# This handy script will generate some major flog

import datetime
import random
import numpy as np
import math


RANDOM_MESSAGES = [
    "one",
    "Hi there",
    "(awesome)",
    "No way",
    "Sure",
    "good thinking",
    "I am not a bot",
    "G'day mate",
    "How is it going?",
    "We have a HOT-{} ticket".format(random.randint(300, 10000)),
    "All abord",
    "I have no idea what I am doing here",
    "haha, same here"
]


def gen_flog(sample_size=130, freq=6*math.pi, base_date=datetime.datetime.now(), cluster_size=1, cluster_density_ms=800):
    """
    Generate random messages spam imitating activity in some of the chat groups
    p(message) = a * cos(w*t),
    message gets generated if p(msg) > threshold

    :param size:
    :param base_date:
    :return:
    """

    t = np.arange(sample_size)
    sin = np.sin(t*freq)

    time_stamp = base_date
    for i in t:
        time_stamp += datetime.timedelta(seconds=i)

        for j in xrange(cluster_size):
            time_stamp += datetime.timedelta(milliseconds=cluster_density_ms)
            yield "{} {}".format(time_stamp, random.choice(RANDOM_MESSAGES))

