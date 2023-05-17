## Heavy Hitters  
  
This class provides a space and time efficient data structure (called a sketch) to find the most frequent elements of a data stream. All elements that occur at least `phi * m` times are returned (where `m` is the length of the stream), while elements that occur less than`(phi - epsilon) * m` times are ignored. 
  
  
To import the class, use the following:  
  
```python  
from streamsketchlib.heavy_hitters import HeavyHittersFinder 
```  
### Overview  
  
It supports the following operations:  
  
- insert a token and count (default is 1) as encountered in the data stream. 
- return all heavy hitter elements and their approximate counts. 
- combine the sketches of two streams so that we can find all the heavy hitters in the combined stream.  
  
### Initialization  
  
To initialize an instance of this class, we can specify the following parameters:  

  -`phi`: defines the cutoff for what constitutes a heavy hitter. The default value is `0.05`.
 - `epsilon`: controls margin of error within which false positives are permitted. The default value is `0.02`.  
 - `delta`: controls the failure probability. The default value is `0.01` (non-deterministic algorithms only). 
 - `seed`: the seed for randomness. The default value is `42`.
 - `algorithm`:	
   - `COUNTMIN` (default) : This is an implementation of the    heavy hitters algorithm in the paper  "An Improved Data Stream Summary: The Count-Min Sketch and its Applications" by Graham Cormode and S. Muthukrishnan. Specifically, it is the "cash register model" version of the algorithm that permits only positive counts upon insert. The data structure uses roughly `O~(1/eps * log(1/delta))` memory (excluding overhead).
   - `MISRAGRIES`: This is an implementation of the algorithm in the paper "Finding Repeated Elements" by J. Misra and David Gries. The data structure is deterministic and uses roughly  `0~(1/(phi * eps))` memory (excluding overhead. 
For example,  
  
```python  
stream = HeavyHittersFinder(phi=0.01, epsilon=0.2)  
stream2 = HeavyHittersFinder()  
```  
  
### insert  
  
Insert a new token into the sketch. The token must be byte-like objects. The easiest way to achieve this is to convert a token to string.  By default, items are inserted with a count of 1. However, this can be easily overridden in cases where each token has an associated count (such as a sales quantity).

For example,  
  
  
```python  
stream = stream = HeavyHittersFinder(phi=0.01, epsilon=0.2, delta=0.01)  
stream.insert("apple")  
stream.insert("orange", 10)  
stream.insert("apple", 5)  
```


### get_heavy_hitters
Returns a dictionary of all the heavy-hitters that have appeared in the stream so far along with an estimated count for each. 
(NOTE: the estimated count is a very poor estimate and is useful mostly for comparing heavy-hitters relative to one another).  
  
For example,  
```python
stream = HeavyHittersFinder(phi=0.01, epsilon=0.2)  
  
stream.insert("heavy-hitter", 10000)  
stream.insert("lightweight", 1)
  
print(stream.get_heavy_hitters())  

>>> {'heavy-hitter': 10000}

```  
  
### merge  
  
Merge with another sketch with the same initialization parameters. The resulted sketch will provide answer to the combined stream.  
  
For example,  
  
```python  
stream = HeavyHittersFinder(delta=0.01, epsilon=0.05, seed=42)  
stream2 = HeavyHittersFinder(delta=0.01, epsilon=0.05, seed=42)  

stream.insert("heavy-hitter", 10000)  
stream.insert("lightweight", 1)

stream2.insert("other heavy-hitter", 8000)  
stream2.insert("lightweight", 1)
  
stream.merge(stream2)  
print(stream.get_heavy_hitters())  
  
>>> {'heavy-hitter': 10000, 'other heavy-hitter': 8000} 
  
```  
  
### + Operator  
  
If A is a sketch of some stream and B is a sketch of another stream, then A + B returns the merged sketch that provides the answer to the combined stream. In other words, A = A+B is the same as A.merge(B).   
  
For example,  
  
```python  
stream = HeavyHittersFinder(delta=0.01, epsilon=0.05, seed=42)  
stream2 = HeavyHittersFinder(delta=0.01, epsilon=0.05, seed=42)  

stream.insert("heavy-hitter", 10000)  
stream.insert("lightweight", 1)

stream2.insert("other heavy-hitter", 8000)  
stream2.insert("lightweight", 1)
  
stream = stream + stream2  
print(stream.get_heavy_hitters())  
  
>>> {'heavy-hitter': 10000, 'other heavy-hitter': 8000} 
  
```  
  
### from_existing   
Create a new sketch with similar parameters so that they can be merged later.  
  
For example,  

```python
stream = HeavyHittersFinder(delta=0.01, epsilon=0.05, seed=42)  
stream2 = HeavyHittersFinder.from_existing(stream)

stream.insert("heavy-hitter", 10000)  
stream.insert("lightweight", 1)

stream2.insert("other heavy-hitter", 8000)  
stream2.insert("lightweight", 1)
  
stream = stream + stream2  
print(stream.get_heavy_hitters())  
  
>>> {'heavy-hitter': 10000, 'other heavy-hitter': 8000} 

```