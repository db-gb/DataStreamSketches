import mmh3
import math
import random
from copy import deepcopy


class MinHash:
    MAX_32_INT = pow(2, 32) - 1

    def __init__(self, epsilon=0.2, hash_type="mmh3"):
        """ epsilon: relative error, delta: failure probability
        for each hash function h, maintain the smallest hash value H """
        self._epsilon = epsilon
        self._hash_type = hash_type

        # Number of hash functions
        self._signature_length = math.ceil(1/pow(self._epsilon, 2))

        # initialize the seeds for hash functions
        self._seed_range = int(math.pow(self._signature_length, 2))
        self._seeds = [random.randint(1, self._seed_range) for _
                       in range(self._signature_length)]

        # Initialize the signature
        self._minhash_signature = [1] * self._signature_length

    def insert(self, token):
        for i in range(self._signature_length):
            current_hash = self._hash(token, self._seeds[i])
            if current_hash < self._minhash_signature[i]:
                self._minhash_signature[i] = current_hash

    def merge(self, other_minhash):
        if other_minhash.signature_size != self._signature_length:
            raise AttributeError("Minhash signature sets must be of equal "
                                 "lengths k in order to merge.")
        else:
            for i in range(self._signature_length):
                if self._seeds[i] != other_minhash.seeds[i]:
                    raise AttributeError("Minhash hash functions must have "
                                         "same seed values for valid result.")
                else:
                    if other_minhash.set_signature[i] < \
                            self._minhash_signature[i]:
                        self._minhash_signature[i] = \
                            other_minhash.minhash_signature[i]

    def __add__(self, other_minhash):
        merged_sketch = deepcopy(self)
        merged_sketch.merge(other_minhash)
        return merged_sketch

    def _hash(self, token, seed):
        """ Compute the hash of a token. """
        if self._hash_type == "mmh3":
            return mmh3.hash(token, seed, signed=False)/MinHash.MAX_32_INT

    @classmethod
    def from_existing(cls, original):
        """ Creates a new minhash based on the parameters of an existing minhash.
            Two minhashes are mergeable iff they share array size and hash
            seeds. Therefore, to create mergeable minhashes, use an original to
            create new instances. """
        new_minhash = cls()
        new_minhash._epsilon = original.epsilon
        new_minhash._hash_type = original.hash_type
        new_minhash._signature_length = original._signature_length
        new_minhash._seed_range = original.seed_range
        new_minhash._seeds = original.seeds
        # Initialize the signature
        new_minhash._set_signature = [1] * new_minhash._signature_length

        return new_minhash

    @property
    def epsilon(self):
        """ Controls the estimate's quality. The default value is 0.02."""
        return self._epsilon

    @property
    def hash_type(self):
        """ No documentation yet. """
        return self._hash_type

    @property
    def signature_length(self):
        """ No documentation yet. """
        return self._signature_length

    @property
    def seed_range(self):
        """ Controls the estimate's quality. The default value is 0.02."""
        return self._seed_range

    @property
    def seeds(self):
        """ Controls the estimate's quality. The default value is 0.02."""
        return self._seeds

    @property
    def set_signature(self):
        """ Controls the estimate's quality. The default value is 0.02."""
        return self._set_signature




