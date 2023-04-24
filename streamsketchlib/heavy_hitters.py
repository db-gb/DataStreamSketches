from streamsketchlib.heavy_hitters_algorithms import AbstractHeavyHittersAlgorithm
from streamsketchlib.heavy_hitters_algorithms import CountMinCashRegister


class HeavyHittersFinder(AbstractHeavyHittersAlgorithm):
    COUNTMIN = 0
    MISRAGRIES = 1

    def __init__(self, phi=0.05, epsilon=0.2, delta=0.01, seed=42,
                 algorithm=COUNTMIN):
        self.phi = phi
        self.epsilon = epsilon
        self.delta = delta
        self.seed = seed
        self._heavy_hitters_finder = None

        if algorithm == HeavyHittersFinder.COUNTMIN:
            self._heavy_hitters_finder = CountMinCashRegister(self.phi,
                                                                self.epsilon,
                                                                self.delta,
                                                                self.seed)
        elif algorithm == HeavyHittersFinder.MISRAGRIES:
            pass

    def insert(self, token, count=1):
        self._heavy_hitters_finder.insert(token, count)

    def get_heavy_hitters(self):
        return self._heavy_hitters_finder.get_heavy_hitters()

    def merge(self, other_finder):
        self._heavy_hitters_finder.merge(other_finder._heavy_hitters_finder)

    @classmethod
    def from_existing(cls, original):
        """ Creates a new sketch based on the parameters of an existing sketch.
            Two sketches are mergeable iff they share array size and hash
            seeds. Therefore, to create mergeable sketches, use an original to
            create new instances. """
        new_hh = cls()
        new_hh.epsilon = original.epsilon
        new_hh.delta = original.delta
        new_hh.phi = original.phi

        algorithm_class = original._heavy_hitters_finder.__class__
        new_hh._heavy_hitters_finder = algorithm_class\
            .from_existing(original._heavy_hitters_finder)

        return new_hh
