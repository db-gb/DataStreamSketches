from streamsketchlib.bloom_filter import BloomFilter


def test_bloom_filter():
    test_n = 1000000

    test_bf = BloomFilter(n=test_n)

    for i in range(test_n):
        test_bf.insert(str(i))

    for i in range(test_n):
        assert test_bf.membership(str(i))

    false_positives = []

    for i in range(test_n, 2*test_n):
        if test_bf.membership(str(i)):
            false_positives.append(i)

    false_pos_count = len(false_positives)
    assert false_pos_count < (test_n * 0.012)
