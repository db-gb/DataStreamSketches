from streamsketchlib.f2_estimate import F2Estimate

def test_f2_estimate_1():
    epsilon = 0.1
    delta = 0.01

    S = F2Estimate(epsilon = epsilon, delta = delta)

    S.insert('a', 10)
    S.insert('b', 5)
    S.insert('a', -2)
    S.insert('d', 1)
    S.insert('e', 30)
    S.insert('c', 20)
    S.insert('a', 40)
    S.insert('b', 25)

    assert S.estimator() >= (1-epsilon)*4505 and S.estimator() <= (1+epsilon)*4505

def test_f2_estimate_2():
    epsilon = 0.1
    delta = 0.01

    S1 = F2Estimate(epsilon = epsilon, delta = delta)
    S2 = F2Estimate.from_existing(S1)

    S1.insert('a', 10)
    S1.insert('b', 5)
    S1.insert('a', -2)
    S1.insert('d', 1)
    S1.insert('e', 30)
    S1.insert('c', 20)
    S1.insert('a', 40)
    S1.insert('b', 25)

    S2.insert('a', 50)
    S2.insert('b', -5)
    S2.insert('a', -10)

    S1.merge(S2)
    assert S1.estimator() >= (1-epsilon)*9670 and S1.estimator() <= (1+epsilon)*9670

def test_f2_estimate_3():
    epsilon = 0.1
    delta = 0.01

    S1 = F2Estimate(epsilon = epsilon, delta = delta)
    S2 = F2Estimate.from_existing(S1)

    S1.insert('a', 10)
    S1.insert('b', 5)
    S1.insert('a', -2)
    S1.insert('d', 1)
    S1.insert('e', 30)
    S1.insert('c', 20)
    S1.insert('a', 40)
    S1.insert('b', 25)

    S2.insert('a', 50)
    S2.insert('b', -5)
    S2.insert('a', -10)

    S1 = S1 + S2
    assert S1.estimator() >= (1-epsilon)*9670 and S1.estimator() <= (1+epsilon)*9670


def test_f2_estimate_4():
    epsilon = 0.1
    delta = 0.01
    n = 10000
    S1 = F2Estimate(epsilon = epsilon, delta = delta)
    S2 = F2Estimate.from_existing(S1)
    f = {}

    for i in range(n):
        S1.insert(str(i), 10)
        f[str(i)] = 10
     
    for i in range(int(n/2), int(3*n/2)):
        S2.insert(str(i), 20)
        if str(i) not in f:
            f[str(i)] = 20
        else:
            f[str(i)] += 20

    ans = 0
    for s in f:
        ans += f[s]*f[s]

    S3 = S1 + S2
    assert S3.estimator() >= (1-epsilon)*ans and S3.estimator() <= (1+epsilon)*ans
    S1.merge(S2)
    assert S1.estimator() >= (1-epsilon)*ans and S1.estimator() <= (1+epsilon)*ans


if __name__ == '__main__':
    test_f2_estimate_1()
    test_f2_estimate_2()
    test_f2_estimate_3()
    test_f2_estimate_4()

