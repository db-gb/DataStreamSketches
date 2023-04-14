import mmh3 
import math


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
        self.m = math.ceil(self.n*math.log2(1/delta)/math.log(2))
        self.k = math.ceil(math.log(1/delta))
        self.max_128_int = pow(2, 128)-1

        self.B = [False for _ in range(self.m)]
        self.seeds = [seed*i for i in range(self.k)]

    def _hash(self, token, seed):
        x = mmh3.hash128(token, seed, signed=False)/self.max_128_int
        return int(x*(self.m-1))
    
    def insert(self, x):
        for i in range(self.k):
            self.B[self._hash(x, self.seeds[i])] = True

    def membership(self, x):
        for i in range(self.k):
            if self.B[self._hash(x, self.seeds[i])] is False:
                return False
        return True