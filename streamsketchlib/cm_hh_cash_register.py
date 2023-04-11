from streamsketchlib.count_min import CountMin
from heapq import heappush, heappop


class HeavyHittersCMRegister:
    """ This class solves the heavy hitters problem using a count-min data
        structure. It works only for the cash register model of a stream where
        each token count must be greater than 0 (c > 0)."""
    def __init__(self, phi=0.01, epsilon=0.1, delta=0.01):
        self.phi = phi
        self.epsilon = epsilon
        self.delta = delta
        self.count_min = CountMin(phi=self.phi, epsilon=self.epsilon,
                                  delta=self.delta, seed=pow(13, 2))
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
        heavy_hitters = set()
        for count, item in self._min_heap:
            if item not in heavy_hitters:
                heavy_hitters.add(item)
        return list(heavy_hitters)


