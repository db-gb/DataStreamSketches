from streamsketchlib.count_min import CountMin

def test_countmin():
    mincounter = CountMin()
    mincounter.process('a', 10)
    mincounter.process('b', 7)
    mincounter.process('a', -3)
    mincounter.process('d', 1)
    mincounter.process('e', 7)
    mincounter.process('c', -1)

    test = mincounter.estimate_frequency('a')
    assert test >= 7