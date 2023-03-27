from math import ceil, inf, pow, log
import numpy as np
import mmh3


class CountMin:

    def __init__(self, epsilon=0.05, delta=0.05, seed=10):
        self.epsilon = epsilon
        self.delta = delta
        self.k = ceil(2/self.epsilon)
        self.t = ceil(log(1/self.delta))
        self.C = np.zeros((self.t, self.k), dtype=int)
        self.max_32_int = pow(2, 32) - 1
        self._hash_seeds = [0 for _ in range(self.t)]

        for i in range(self.t):
            self._hash_seeds[i] = i*i*seed

    def _hash(self, token, seed):
        """ Compute the hash of a token. """
        hash_value = mmh3.hash(token, seed, signed=False)/self.max_32_int
        bin = hash_value * self.k
        return int(bin)

    def process(self, token, count):
        for i in range(self.t):
            col = self._hash(token, self._hash_seeds[i])
            self.C[i, col] = self.C[i, col] + count

    def estimate_frequency(self, token):
        estimate = inf
        for i in range(self.t):
            col = self._hash(token, self._hash_seeds[i])
            estimate = min(estimate, self.C[i, col])
        return estimate
