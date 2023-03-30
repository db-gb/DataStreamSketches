from math import ceil, inf, pow, log
import numpy as np
import mmh3


class CountMin:
    max_32_int = pow(2, 32) - 1

    def __init__(self, epsilon=0.05, delta=0.05, seed=10):
        self.epsilon = epsilon
        self.delta = delta
        self.k = ceil(2/self.epsilon)
        self.t = ceil(log(1/self.delta))
        self.C = np.zeros((self.t, self.k), dtype=int)
        self._hash_seeds = [0 for _ in range(self.t)]

        for i in range(self.t):
            self._hash_seeds[i] = i*i*seed

    @classmethod
    def from_existing(cls, original_cm):
        """ Creates a new sketch based on the parameters of an existing sketch.
            Two sketches are mergeable iff they share array size and hash
            seeds. Therefore, to create mergeable sketches, use an original to
            create new instances. """
        new_cm = cls()
        new_cm.epsilon = original_cm.epsilon
        new_cm.delta = original_cm.delta
        new_cm.k = original_cm.k
        new_cm.t = original_cm.t
        new_cm.C = np.zeros((new_cm.t, new_cm.k), dtype=int)
        new_cm._hash_seeds = original_cm._hash_seeds
        return new_cm

    def _hash(self, token, seed):
        """ Compute the hash of a token. Converts hash value to a bin number
            based on k."""
        hash_value = mmh3.hash(token, seed, signed=False)/self.max_32_int
        bin_number = hash_value * self.k
        return int(bin_number)

    def insert(self, token, count):
        for i in range(self.t):
            col = self._hash(token, self._hash_seeds[i])
            self.C[i, col] = self.C[i, col] + count

    def estimate_frequency(self, token):
        estimate = inf
        for i in range(self.t):
            col = self._hash(token, self._hash_seeds[i])
            estimate = min(estimate, self.C[i, col])
        return estimate

    def merge(self, other_count_min):
        self.C = np.add(self.C, other_count_min.C)
