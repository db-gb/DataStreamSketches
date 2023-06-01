from streamsketchlib.distinct_count_algorithms \
    import AbstractDistinctCountAlgorithm
from streamsketchlib.distinct_count_algorithms import BJKST_1


class DistinctCount(AbstractDistinctCountAlgorithm):
    BJKST_1 = 1

    def __init__(self, epsilon=0.01, delta=0.01, algorithm=BJKST_1,
                 hash_type="mmh3", seed=42):
        """ epsilon: relative error
        delta: failure probability
        """
        self._epsilon = epsilon
        self._delta = delta
        self._algorithm = algorithm
        self._hash_type = hash_type
        self._seed = seed

        if self._algorithm == DistinctCount.BJKST_1:
            self._f0_sketch = BJKST_1(epsilon=self._epsilon, delta=self._delta,
                                      hash_type=self._hash_type,
                                      seed=self._seed)

    def insert(self, token):
        self._f0_sketch.insert(token)
    
    def estimator(self):
        return self._f0_sketch.estimator()

    def merge(self, another_sketch):
        self._f0_sketch.merge(another_sketch.f0_sketch)

    @classmethod
    def from_existing(cls, original):
        new_distinct_counter = cls(epsilon=original.epsilon,
                                   delta=original.delta,
                                   algorithm=original.algorithm,
                                   hash_type=original.hash_type,
                                   seed=original.seed)
        return new_distinct_counter

    @property
    def epsilon(self):
        """ Controls the estimate's quality. The default value is 0.01."""
        return self._epsilon

    @property
    def delta(self):
        """ Controls the failure probability. The default value is 0.01."""
        return self._delta

    @property
    def algorithm(self):
        """ The Distinct-Count Algorithm being used. Default is BJKST_1."""
        return self._algorithm

    @property
    def hash_type(self):
        """ Hashing algorithm being used. Default is mmh3 (Murmurhash)."""
        return self._hash_type

    @property
    def seed(self):
        """ The seed for randomness. The default value is 42."""
        return self._seed

    @property
    def f0_sketch(self):
        """ The instance of the sketching algorithm being used to solve
            Distinct-Count."""
        return self._f0_sketch