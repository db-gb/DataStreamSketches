import mmh3
import math
import random
from copy import deepcopy


class MinHash:
    MAX_32_INT = pow(2, 32) - 1

    def __init__(self, epsilon=0.1, hash_type="mmh3"):
        """ epsilon: relative error, delta: failure probability
        for each hash function h, maintain the smallest hash value H """
        self._epsilon = epsilon
        self._hash_type = hash_type

        # Number of hash functions. Length of resulting signature.
        self._k = math.ceil(1/pow(self._epsilon, 2))

        # initialize the seeds for hash functions
        self._seed_range = int(math.pow(self._k, 2))
        self._seeds = [random.randint(1, self._seed_range) for _
                       in range(self._k)]

        # Initialize the signature
        self._minhash_signature = [1] * self._k

    def insert(self, token):
        """ Inserts a new token into the minhash signature by hashing it
            against all k seeds and comparing to the existing values in the
            signature. """
        for i in range(self._k):
            current_hash = self._hash(token, self._seeds[i])
            # Replace existing hash value if new value smaller
            if current_hash < self._minhash_signature[i]:
                self._minhash_signature[i] = current_hash

    def merge(self, other_mh):
        """ Merges two minhash signatures resulting in a single signature
            representing the union of the two original sets. """
        try:
            self._check_mergeability(other_mh)
            for i in range(self._k):
                if other_mh.set_signature[i] < self._minhash_signature[i]:
                    self._minhash_signature[i] = other_mh.minhash_signature[i]
        except AttributeError:
            print("Merge attempted on incompatible minhash instances.")

    def __add__(self, other_minhash):
        """ Performs merge but returns result in completely new minhash."""
        merged_minhash = deepcopy(self)
        merged_minhash.merge(other_minhash)
        return merged_minhash

    def _hash(self, token, seed):
        """ Compute the hash of a token."""
        if self._hash_type == "mmh3":
            return mmh3.hash(token, seed, signed=False)/MinHash.MAX_32_INT

    @classmethod
    def from_existing(cls, original):
        """ Creates a new minhash based on the parameters of an existing
            minhash. Two minhashes are mergeable iff they share array size and
            hash seeds. Therefore, to create mergeable minhashes, use an
            original to create new instances."""
        new_minhash = cls()
        new_minhash._epsilon = original.epsilon
        new_minhash._hash_type = original.hash_type
        new_minhash._k = original.k
        new_minhash._seed_range = original.seed_range
        new_minhash._seeds = original.seeds
        # Initialize the signature
        new_minhash._set_signature = [1] * new_minhash._k
        return new_minhash

    def _check_mergeability(self, other_minhash):
        """ Compares other minhash signature attributes to make sure that
            merges or Jaccard similarity estimates make sense. If two minhashes
            have different randomization seeds, no comparison or merge is
            possible."""
        if other_minhash.k != self._k:
            raise AttributeError("Minhash signature sets must be of equal "
                                 "lengths k in order to merge.")
        else:
            for i in range(self._k):
                if self._seeds[i] != other_minhash.seeds[i]:
                    raise AttributeError("Minhash hash functions must have "
                                         "same seed values for valid result.")

    def estimate_jaccard_similarity(self, other_mh):
        """ Provides an estimate for the Jaccard Similarity of two sets by
            calculating the ratio of minhash signature rows that match for
            both sets. """
        counter = 0
        for i in range(self._k):
            if self._minhash_signature[i] == other_mh.minhash_signature[i]:
                counter += 1
        return counter/self._k

    @property
    def epsilon(self):
        """ Controls the estimate's quality. Resulting Jaccard Similarity
        estimate should be within epsilon of true value. The default value is
        0.01."""
        return self._epsilon

    @property
    def hash_type(self):
        """ Hashing algorithm being used. Default is mmh3 (Murmurhash)."""
        return self._hash_type

    @property
    def k(self):
        """ The number of hash functions used to hash each input token. Each
            minhash signature consists of k values, each of which being the
            smallest hash value produced by that hash function so far."""
        return self._k

    @property
    def seed_range(self):
        """ The range over which hash seeds are randomly chosen. """
        return self._seed_range

    @property
    def seeds(self):
        """ The set of k seeds which are used for the hash functions. """
        return self._seeds

    @property
    def minhash_signature(self):
        """ The current minhash signature consisting of the k smallest hashes
            encountered so far. """
        return self._minhash_signature
