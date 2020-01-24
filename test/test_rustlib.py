from libra.rustlib import *

def assert_equal(aa, bb):
    assert aa == bb


def test_next_power_of_two():
    assert_equal(next_power_of_two(0), 1)
    assert_equal(next_power_of_two(1), 1)
    assert_equal(next_power_of_two(2), 2)
    assert_equal(next_power_of_two(3), 4)

def test_is_power_of_two():
    assert_equal(is_power_of_two(0), False)
    assert_equal(is_power_of_two(1), True)
    assert_equal(is_power_of_two(2), True)
    assert_equal(is_power_of_two(3), False)
    assert_equal(is_power_of_two(8), True)
    assert_equal(is_power_of_two(9), False)


def test_resize_list():
    assert_equal(resize_list([1,2,3], 2, None), [1,2])
    assert_equal(resize_list([1,2,3], 6, 2), [1,2,3,2,2,2])
