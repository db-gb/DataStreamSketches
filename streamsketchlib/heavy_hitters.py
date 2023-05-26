from streamsketchlib.heavy_hitters_algorithms \
    import AbstractHeavyHittersAlgorithm, CountMinCashRegister, MisraGries


class HeavyHittersFinder(AbstractHeavyHittersAlgorithm):
    COUNTMIN = 0
    MISRAGRIES = 1

    def __init__(self, phi=0.05, epsilon=0.2, delta=0.01, seed=42,
                 algorithm=COUNTMIN):
        self._phi = phi
        self._epsilon = epsilon
        self._delta = delta
        self._seed = seed
        self._heavy_hitters_finder = None

        if algorithm == HeavyHittersFinder.COUNTMIN:
            self._heavy_hitters_finder = CountMinCashRegister(self._phi,
                                                                self._epsilon,
                                                                self._delta,
                                                                self._seed)
        elif algorithm == HeavyHittersFinder.MISRAGRIES:
            self._heavy_hitters_finder = MisraGries(self._phi, self._epsilon,
                                                    self._delta, self._seed)

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
        new_hh = cls(epsilon=original.epsilon, delta=original.delta,
                     phi=original.phi, seed=original.seed)

        algorithm_class = original._heavy_hitters_finder.__class__
        new_hh._heavy_hitters_finder = algorithm_class\
            .from_existing(original._heavy_hitters_finder)

        return new_hh

    @property
    def phi(self):
        """Defines the cutoff for what constitutes a heavy hitter. The default
        value is 0.05."""
        return self._phi

    @property
    def epsilon(self):
        """Controls margin of error within which false positives are permitted.
         The default value is 0.02."""
        return self._epsilon

    @property
    def delta(self):
        """Controls the failure probability. The default value is 0.01
        (used in non-deterministic algorithms only)."""
        return self._delta

    @property
    def seed(self):
        """The seed for randomness. The default value is 42 (used in
        non-deterministic algorithms only)."""
        return self._seed

