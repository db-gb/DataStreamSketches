from streamsketchlib.count_min import CountMin
from heapq import heappush, heappop, heapify
from math import ceil
from abc import abstractmethod
from copy import deepcopy


class AbstractHeavyHittersAlgorithm:
    @abstractmethod
    def insert(self, token, count):
        pass

    @abstractmethod
    def get_heavy_hitters(self):
        pass

    @abstractmethod
    def merge(self, other_finder):
        pass

    @abstractmethod
    def from_existing(self, original):
        pass

    def __add__(self, other):
        merged_sketch = deepcopy(self)
        merged_sketch.merge(other)
        return merged_sketch


class CountMinCashRegister(AbstractHeavyHittersAlgorithm):
    """ This class solves the heavy hitters problem using a count-min data
        structure. It works only for the cash register model of a stream where
        each token count must be greater than 0 (c > 0)."""
    def __init__(self, phi=0.05, epsilon=0.2, delta=0.01, seed=42):
        self.phi = phi
        self.epsilon = epsilon
        self.delta = delta
        self.seed = seed
        self.count_min = CountMin(phi=self.phi, epsilon=self.epsilon,
                                  delta=self.delta, seed=self.seed)
        self.l1_norm = 0
        self._min_heap = []

    def insert(self, token, count):
        self.l1_norm += count
        cutoff = self.phi * self.l1_norm

        self.count_min.insert(str(token), count)
        point_query = self.count_min.estimate_count(token)
        if point_query >= cutoff:
            heappush(self._min_heap, (point_query, token))

        if len(self._min_heap) > 0:
            smallest_estimate = self._min_heap[0][0]
            while smallest_estimate < cutoff and len(self._min_heap) > 0:
                heappop(self._min_heap)
                if len(self._min_heap) > 0:
                    smallest_estimate = self._min_heap[0][0]

    def get_heavy_hitters(self):
        heavy_hitters = {}
        for count, item in self._min_heap:
            heavy_hitters[item] = self.count_min.estimate_count(item)
        return heavy_hitters

    @classmethod
    def from_existing(cls, original):
        """ Creates a new sketch based on the parameters of an existing sketch.
            Two sketches are mergeable iff they share array size and hash
            seeds. Therefore, to create mergeable sketches, use an original to
            create new instances. """
        new_cm_hh = cls()
        new_cm_hh.epsilon = original.epsilon
        new_cm_hh.delta = original.delta
        new_cm_hh.phi = original.phi
        new_cm_hh.count_min = CountMin.from_existing(original.count_min)
        new_cm_hh.l1_norm = 0
        new_cm_hh._min_heap = []
        return new_cm_hh

    def merge(self, other_instance):
        """ Merges other heavy-hitter instance into self. Both instance being
            merged and the instance being merged into need to share all
            parameters and hash seeds. Otherwise, the merge will fail. If it
            does not fail, the results will be meaningless. """
        self.count_min.merge(other_instance.count_min)

        self.l1_norm += other_instance.l1_norm
        cutoff = self.l1_norm * self.phi

        # A heavy-hitter in merged instance must have been heavy hitter in
        # at least one instance prior to merge.
        self._min_heap.extend(other_instance._min_heap)
        heapify(self._min_heap)

        # Remove any tokens that are no longer heavy hitters.
        smallest_estimate = self._min_heap[0][0]
        while smallest_estimate < cutoff and len(self._min_heap) > 0:
            old_value, token = heappop(self._min_heap)
            # Check to see if new token count qualifies it as a heavy hitter
            new_estimate = self.count_min.estimate_count(token)
            if new_estimate >= cutoff:
                heappush(self._min_heap, (new_estimate, token))
            if len(self._min_heap) > 0:
                smallest_estimate = self._min_heap[0][0]


class MisraGries(AbstractHeavyHittersAlgorithm):
    """ Implements the Misra-Gries algorithm for finding frequent items (ie
        heavy hitters). """

    def __init__(self, phi=0.05, epsilon=0.2, delta=0.01, seed=42):
        """ Parameter k controls heavy hitter threshold, i.e., total_count/k
            k - number of buckets
            m - count of all elements encountered (length of stream)
            phi - heavy hitters are elements occurring >= (phi * m) times
            epsilon - margin of error - elements occurring > (1-eps)*phi*m
                    times may be returned
        """
        self.phi = phi
        self.epsilon = epsilon

        self.k = ceil(1 / (self.phi * self.epsilon))
        self.counters = {}
        self.m = 0

    @classmethod
    def from_phi_and_eps(cls, phi=0.0025, epsilon=0.2):
        """ Initializes Misra-Gries instance directly from phi and epsilon."""
        new_misra = cls()
        new_misra.phi = phi
        new_misra.epsilon = epsilon
        new_misra.k = ceil(1 / (phi * epsilon))
        return new_misra

    def insert(self, token, count=1):
        """ Processes a new token into the dictionary. If an element already
            occupies a bucket, then increment that bucket count. If not, then
            if there are available buckets, store the token in a new bucket.
            Otherwise, decrement the count of all other buckets.
            Input: token - could be string or number """
        for _ in range(count):
            self.m += 1
            if token in self.counters:
                self.counters[token] += 1
            else:
                if len(self.counters) < self.k-1:
                    self.counters[token] = 1
                else:
                    for y in list(self.counters):
                        self.counters[y] -= 1
                        if self.counters[y] == 0:
                            del self.counters[y]

    def top_counters(self, amount):
        """ Return the buckets of top estimate counts
        count - stream length/num_buckets <= estimate count <= count
        """
        sorted_freq = sorted(self.counters, key=self.counters.get,
                             reverse=True)
        sorted_counters = {}
        for y in sorted_freq[:amount]:
            sorted_counters[y] = self.counters[y]
        return sorted_counters

    def get_heavy_hitters(self):
        """ Elements that occur more than phi * m times in stream are heavy
            hitters will be returned. Those occurring less than (1-eps)*phi*m
            times will be ignored. Those within the margin may or may not be
            returned """
        heavy_hitters = {}
        counters = self.counters.copy()
        threshold = (1 - self.epsilon) * self.phi * self.m
        for key, counter in counters.items():
            if counter > threshold:
                heavy_hitters[key] = counter
        return heavy_hitters

    def merge(self, other_sketch):
        """ Merge with another Misra-Gries sketch
        Requirements: other sketch must have the same number of counters k
        """
        self.m += other_sketch.m
        # adding counts key-wise
        for x in other_sketch.counters:
            if x in self.counters:
                self.counters[x] += other_sketch.counters[x]
            else:
                self.counters[x] = other_sketch.counters[x]
        # Remove (k+1)th counter value from the remaining counters
        keys_to_delete = []
        if len(self.counters) > self.k:
            sorted_values = sorted(self.counters.values(), reverse=True)
            c = sorted_values[self.k]
            for key in self.counters.keys():
                self.counters[key] -= c
                if self.counters[key] <= 0:
                    keys_to_delete.append(key)
        for key in keys_to_delete:
            del self.counters[key]

    def from_existing(self, original):
        pass

    #def get_memory_footprint(self):
    #    size = 0
    #    size += getsizeof(self)
    #    size += getsizeof(self.k)
    #    size += getsizeof(self.m)
    #    size += getsizeof(self.epsilon)
    #    size += getsizeof(self.phi)
    #    size += getsizeof(self.counters)
    #    for key, value in self.counters.items():
    #        size += getsizeof(key)
    #        size += getsizeof(value)
    #    return size

