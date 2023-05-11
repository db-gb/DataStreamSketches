import mmh3 
import math
from copy import deepcopy

class BloomFilter:
    """
    Bloom Filter
    """
    def __init__(self, n=10000, delta=0.01, seed=42):
        """
        n: the maximum number of insertions
        delta: false positive rate 
        """
        self.n = n
        self.delta = delta
        self.seed = seed

        self.m = math.ceil(self.n*math.log2(1/delta)/math.log(2))
        self.k = math.ceil(math.log(1/delta))
        self.max_128_int = pow(2, 128)-1
        self.B = [0 for _ in range(self.m)]
        self.seeds = [self.seed*i for i in range(self.k)]

    def _hash(self, token, seed):
        x = mmh3.hash128(token, seed, signed=False)/self.max_128_int
        return int(x*(self.m-1))
    
    def delete(self, x):
        for i in range(self.k):
            self.B[self._hash(x, self.seeds[i])] -= 1

    def insert(self, x):
        for i in range(self.k):
            self.B[self._hash(x, self.seeds[i])] += 1

    def membership(self, x):
        for i in range(self.k):
            if self.B[self._hash(x, self.seeds[i])] == 0:
                return False
        return True
    
    def merge(self, X):
        for i in range(len(self.B)):
            self.B[i] += X.B[i]

    def __add__(self, X):
        merged_filter = BloomFilter.from_existing(self)
        merged_filter.B = deepcopy(self.B)
        for i in range(len(merged_filter.B)):
            merged_filter.B[i] += X.B[i]
        return merged_filter

    @classmethod
    def from_existing(cls, original):
        """ Creates a new Bloom Filter based on existing Bloom Filter with similar parameters
        so that they are mergeable."""
        new_filter = BloomFilter(n = original.n, delta = original.delta, seed = original.seed)
        return new_filter
