## Reservoir Sampling

This class provides an implementation of reservoir sampling in a data stream. To import the class, use the following

```python
from streamsketchlib.rsv_sampling import RsvSampling
```

### Overview

The class uses reservoir sampling to maintain k tokens uniformly sampled at random from a data stream of unknown length. The update time for each new token is constant, and the memory use is proportional to k times the size of a token.

### Initialization

To create a reservoir sampler, specify the desired sample size during initialization.

```python
sampler = RsvSampling(rsv_size = 1000)
```

### Insert

Insert a token into the data stream.

```python
n = 1000
sampler = RsvSampling(rsv_size = 10)
for i in range(n):
    sampler.insert(i)
```

### Reservoir

Return the tokens sampled uniformly at random from the data stream observed so far.

```python
n = 1000
sampler = RsvSampling(rsv_size = 10)
for i in range(n):
    sampler.insert(i)
for i in sampler.reservoir():
    print(i)

>>> 31
473
487
510
203
748
157
942
268
382
```