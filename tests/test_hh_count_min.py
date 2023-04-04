from streamsketchlib.heavy_hitters_cm import HeavyHittersCM
import pandas as pd


def test_bidict_small():
    test_hh_cm = HeavyHittersCM(phi=0.01, epsilon=0.2)

    test_hh_cm.insert("This", 1)
    test_hh_cm.insert("is", 1)
    test_hh_cm.insert("is", 3)
    test_hh_cm.insert("only", 1)
    test_hh_cm.insert("a", 1)
    test_hh_cm.insert("a", 2)
    test_hh_cm.insert("test.", 10000)
    test_hh_cm.insert("b", 1)
    test_hh_cm.insert("c", 1)
    test_hh_cm.insert("d", 1)
    assert test_hh_cm._token_label == 8

    test = test_hh_cm.get_heavy_hitters()
    assert test == ['test.']


def test_bidict_large():
    test_hh_cm = HeavyHittersCM(n=4000, phi=0.005)

    try:
        test_data = pd.read_csv('item_sales_filtered.csv')

    except FileNotFoundError as e:
        print('Test files not found. Skipping test.')
        return

    item_sales = test_data.values.tolist()
    for item in item_sales:
        test_hh_cm.insert(str(item[0]), item[1])

    test = test_hh_cm.get_heavy_hitters()
    assert '1503844' in test
    assert '1473471' in test
    assert '2042941' in test
    assert '2042947' in test
    assert '819932' not in test
    assert test_hh_cm._token_label == 3940
