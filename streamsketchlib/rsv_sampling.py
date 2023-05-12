import random
from copy import deepcopy

class RsvSampling:
    """ Sample a random element in a data stream without knowing the stream length
    """
    def __init__(self, rsv_size):
        """ Return k random tokens (without replacement) from the stream 
        """
        self.rsv = []
        self.rsv_size = rsv_size
        self.stream_length = 0

    def insert(self, token):
        """ Insert a token into the stream. 
        """
        self.stream_length += 1
        if len(self.rsv) < self.rsv_size:
            self.rsv.append(token)
        else:
            j = random.randint(1, self.stream_length)
            if j <= self.rsv_size:
                self.rsv[j-1] = token

    def reservoir(self):
        """ Return the list of sampled tokens 
        """
        return self.rsv
    
    def merge(self, S):
        """ Merge two samplers with the same size 
        """
        new_rsv = random.sample(self.rsv+S.rsv, self.rsv_size)
        self.rsv = new_rsv
    
    def __add__(self, S):
        """ Return the merged sampler of self and S
        """
        new_sampler = deepcopy(self)
        new_sampler.merge(S)
        return new_sampler
    
    @classmethod
    def from_existing(cls, original):
        """ Create another reservoir sampler with the same size
        """
        new_sampler = cls(rsv_size = original.rsv_size)
        return new_sampler
    