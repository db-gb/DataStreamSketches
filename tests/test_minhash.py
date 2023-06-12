import pytest
from streamsketchlib.minhash import MinHash
from math import floor

def test_minhash_small():
    minhash_1 = MinHash()
    minhash_2 = MinHash.from_existing(minhash_1)

    start_range = 0
    end_range = 200
    overlap = 45

    set_1 = [i for i in range(start_range, floor(end_range/2))]
    set_2 = [i for i in range(floor(end_range/2)-overlap, end_range)]

    for num in set_1:
        minhash_1.insert(str(num))

    for num in set_2:
        minhash_2.insert(str(num))

    intersection = [i for i in range(start_range, end_range) if i in set_1 and i in set_2]
    union = set()
    for i in set_1:
        union.add(i)
    for j in set_2:
        union.add(j)

    true_JS = len(intersection)/len(union)

    estimate_JS = minhash_1.estimate_jaccard_similarity(minhash_2)

    assert abs(true_JS - estimate_JS) <= 0.05

def test_minhash_small_2():
    minhash_1 = MinHash()
    minhash_2 = MinHash.from_existing(minhash_1)

    start_range = 5000
    end_range = 6000
    intersection_size = 100


    set_1 = [i for i in range(start_range, end_range)] + list(range(1,intersection_size))
    set_2 = list(range(1,floor(start_range/2)))

    for num in set_1:
        minhash_1.insert(str(num))

    for num in set_2:
        minhash_2.insert(str(num))

    union = set()
    for i in set_1:
        union.add(i)
    for j in set_2:
        union.add(j)

    true_JS = 100/len(union)

    estimate_JS = minhash_1.estimate_jaccard_similarity(minhash_2)

    assert abs(true_JS - estimate_JS) <= 0.05

def test_minhash_merge():
    minhash_1 = MinHash()
    minhash_2 = MinHash.from_existing(minhash_1)
    minhash_3 = MinHash.from_existing(minhash_1)

    start_range = 4000
    end_range = 6000
    offset = 500
    intersection_size = 100

    set_1 = [i for i in range(start_range, floor(end_range/2))] + list(range(1,intersection_size))
    set_2 = [i for i in range(start_range+offset, end_range)] 
    set_3 = list(range(1,start_range))

    for num in set_1:
        minhash_1.insert(str(num))

    for num in set_2:
        minhash_2.insert(str(num))
        
    for num in set_3:
        minhash_3.insert(str(num))

    minhash_1 += minhash_2

    union = set()
    for i in set_1:
        union.add(i)
    for j in set_2:
        union.add(j)
    for j in set_3:
        union.add(j)

    true_JS = 100/len(union)

    estimate_JS = minhash_1.estimate_jaccard_similarity(minhash_3)

    assert abs(true_JS - estimate_JS) <= 0.05