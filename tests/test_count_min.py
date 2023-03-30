from streamsketchlib.count_min import CountMin

def test_countmin():
    mincounter = CountMin()
    mincounter.insert('a', 10)
    mincounter.insert('b', 7)
    mincounter.insert('a', 3)
    mincounter.insert('d', 1)
    mincounter.insert('e', 7)
    mincounter.insert('c', 11)

    assert mincounter.estimate_frequency('a') >= 13
    assert mincounter.estimate_frequency('b') >= 7
    assert mincounter.estimate_frequency('c') >= 11
    assert mincounter.estimate_frequency('d') >= 1
    assert mincounter.estimate_frequency('e') >= 7


def test_merge():
    mincounter1 = CountMin()
    mincounter2 = CountMin.from_existing(mincounter1)

    mincounter1.insert('a', 10)
    mincounter1.insert('b', 7)
    mincounter1.insert('a', 3)
    mincounter1.insert('d', 1)
    mincounter1.insert('e', 7)
    mincounter1.insert('c', 11)

    mincounter2.insert('a', 5)
    mincounter2.insert('b', 9)
    mincounter2.insert('a', 6)
    mincounter2.insert('d', 14)
    mincounter2.insert('e', 10)
    mincounter2.insert('c', 13)

    mincounter1.merge(mincounter2)

    assert mincounter1.estimate_frequency('a') >= 24
    assert mincounter1.estimate_frequency('b') >= 16
    assert mincounter1.estimate_frequency('c') >= 24
    assert mincounter1.estimate_frequency('d') >= 15
    assert mincounter1.estimate_frequency('e') >= 17

