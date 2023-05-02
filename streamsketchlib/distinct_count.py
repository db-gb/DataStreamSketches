from streamsketchlib.distinct_count_algorithms import AbstractDistinctCountAlgorithm
from streamsketchlib.distinct_count_algorithms import BJKST_1


class DistinctCount(AbstractDistinctCountAlgorithm):

    BJKST_1 = 1

    def __init__(self, epsilon=0.01, delta=0.01, algorithm=BJKST_1, hash_type="mmh3", seed=42):
        """ epsilon: relative error
        delta: failure probability
        """
        self.epsilon = epsilon
        self.delta = delta
        self.hash_type = hash_type
        self.seed = seed

        if algorithm == DistinctCount.BJKST_1:
            self._f0_sketch = BJKST_1(epsilon = self.epsilon, delta = self.delta, hash_type = self.hash_type, seed = self.seed)

    def insert(self, token):
        self._f0_sketch.insert(token)
    
    def estimator(self):
        return self._f0_sketch.estimator()

    def merge(self, another_sketch):
        self._f0_sketch.merge(another_sketch._f0_sketch)
    
    @classmethod
    def from_existing(cls, original):
        new_distinct_counter = cls()
        new_distinct_counter.epsilon = original.epsilon
        new_distinct_counter.delta = original.delta
        new_distinct_counter.phi = original.hash_type

        algorithm_class = original._f0_sketch.__class__
        new_distinct_counter._f0_sketch = algorithm_class.from_existing(original._f0_sketch)

        return new_distinct_counter
