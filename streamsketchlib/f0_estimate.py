import mmh3
import math
import random
import sys
import os
import bisect
from bisect import bisect_left
import time
import statistics
from pympler.asizeof import asizeof

def BinarySearch(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        return -1


class F0Estimate:
    """ Loglog algorithm: memory efficient data structure to estimate
    the number of distinct elements in streams """

    def __init__(self, epsilon=0.01, delta=0.01, c=1, hash_type="mmh3", seed=42):
        """ epsilon: relative error, delta: failure probability
        for each hash function h, maintain the smallest hash value H
        z = median of depth averages of width smallest hash values
        return 1/z - 1 """

        self.depth = c*int(math.log(1/delta, 2))
        self.epsilon = epsilon
        self.hash_type = hash_type

        # t ~ 2/eps^2
        self.t = c*int(math.pow(1/self.epsilon, 2))

        # data structure to store the smallest t hash values
        self.smallest_hashes = [[] for i in range(self.depth)]

        # a list to store all distinct values if F0 < t
        self.small_list = set()

        self.max_32_int = pow(2, 32)-1
        self.seeds = [0 for _ in range(self.depth)]

        for i in range(self.depth):
            self.seeds[i] = i*i*seed


    def _hash(self, token, seed):
        """ Compute the hash of a token. """
        if self.hash_type == "mmh3":
            return mmh3.hash(token, seed, signed=False)/self.max_32_int


    def insert(self, token):
        """ Insert a token into the sketch. Token must be byte-like objects. """
        if len(self.small_list) < self.t:
            self.small_list.add(token)

        for i in range(self.depth):
            hash_value = self._hash(token, self.seeds[i])
            j = BinarySearch(self.smallest_hashes[i], hash_value)

            if j == -1:
                if len(self.smallest_hashes[i]) < self.t:
                    bisect.insort(self.smallest_hashes[i], hash_value)

                elif self.smallest_hashes[i][self.t-1] > hash_value:
                    bisect.insort(self.smallest_hashes[i], hash_value)
                    self.smallest_hashes[i].pop()

    def merge(self, S):
        """ Merge self and another sketch S that must have same seeds """
        # merge the small lists
        for x in S.small_list:
            if len(self.small_list) < self.t:
                self.small_list.add(x)
            else:
                break

        # merge the smallest hash values
        for i in range(self.depth):
            for x in S.smallest_hashes[i]:
                j = BinarySearch(self.smallest_hashes[i], x)
                if j  == -1:
                    if len(self.smallest_hashes[i]) < self.t:
                        bisect.insort(self.smallest_hashes[i], x)
                    elif self.smallest_hashes[i][self.t-1] > x:
                        bisect.insort(self.smallest_hashes[i], x)
                        self.smallest_hashes[i].pop()


    def estimator(self):
        """ Return the estimate for the number of distinct
        elements inserted so far """
        #start_time = time.time()

        if len(self.small_list) < self.t:
            result = len(self.small_list)
            #print(f"F0 algorithm estimation time: {time.time() - start_time}")
            return result

        est = []
        for i in range(self.depth):
            l = len(self.smallest_hashes[i])
            est.append(int(self.t/self.smallest_hashes[i][l-1]))

        median_of_est = statistics.median(est)
        #print(f"F0 algorithm estimation time: {time.time() - start_time}")
        return int(median_of_est)
