## F0Estimate


This class provides a space and time efficient sketch to estimate the number of distinct element up to a factor (1 +- epsilon) with probability at least 1-delta in a data stream.

This is an implementation of the first algorithm in the paper "Counting Distinct Elements in a Data Stream" by Ziv Bar-Yossef, T. S. Jayram, Ravi Kumar, D. Sivakumar & Luca Trevisan.




### Initialization

To initialize an instance of this class, we can specify the following parameters:

- `delta`: controls the failure probability. The default value is `0.01`.
- `epsilon`: controls the estimate's quality. The default value is `0.01`.
- `seed`: the seed for randomness. The default value is `42`.

The algorithm will use roughly `O~(1/eps^2 * log(1/delta))` memory (excluding overheads). 
The update time is `O(log 1/eps)`.

Examples of initialize an instance of F0Esimate:

```python
stream = F0Estimate(delta=0.01, epsilon=0.05, seed=42)
stream2 = F0Estimate()
```

### Insert

Insert a new token into the stream. The token must be byte-like objects. The easiest way to achieve this is to convert a token to string.

For example,

```python
stream = F0Estimate(delta=0.01, epsilon=0.05, seed=42)
stream.insert("apple")
stream.insert("orange")
stream.insert("apple")
```

### Estimator

Return the estimate of the number of distinct elements that have appeared in the stream so far up to a factor (1 +- epsilon) with probability at least 1-delta.

For example,


```python
stream = F0Estimate(delta=0.01, epsilon=0.05, seed=42)

for i in range(100, 200):
    stream.insert(str(i))

for i in range(150, 250):
    stream.insert(str(i))

print(stream.estimator())

>>> 150

```

### Merges

Merge with another sketch with the same seed. The resulted sketch will provide answer to the combine streams.

For example,

```python
stream = F0Estimate(delta=0.01, epsilon=0.05, seed=42)
stream2 = F0Estimate(delta=0.01, epsilon=0.05, seed=42)

for i in range(100, 200):
    stream.insert(str(i))

for i in range(150, 250):
    stream2.insert(str(i))

stream.merge(stream2)

print(stream.estimator())

>>> 150

```