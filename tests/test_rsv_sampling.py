from streamsketchlib.rsv_sampling import RsvSampling


def test_rsv_sampling_1():
    n = 100000
    k = 5000
    sampler = RsvSampling(k)
    total = 0
    for i in range(n):
        sampler.insert(i)
        total += i
    
    sum = 0
    for i in sampler.reservoir():
        sum += i

    # test that the sum of the sample sum concerntrate around k/n * total
    assert (sum > 0.9 * (k/n) * total) and (sum < 1.1 * (k/n) * total)

def test_rsv_sampling_2():
    n = 100000
    k = 5000
    sampler = RsvSampling(k)
    sampler2 = RsvSampling.from_existing(sampler)

    total = 0
    for i in range(n):
        sampler.insert(i)
        total += i
    for i in range(2*n):
        sampler2.insert(i)
        total += i

    sampler.merge(sampler2)

    sum = 0
    for i in sampler.reservoir():
        sum += i

    # test that the sum of the sample sum concerntrate around k/n * total
    assert (sum > 0.9 * (k/n) * total) and (sum < 1.1 * (k/n) * total)

if __name__ == '__main__':
    test_rsv_sampling_1()