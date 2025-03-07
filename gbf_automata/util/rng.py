import time

import numpy as np

rng = np.random.default_rng(seed=time.time_ns())


def rng_uniform(variance: int):
    return rng.uniform(-variance, variance)
