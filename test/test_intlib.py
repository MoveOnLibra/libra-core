from libra.intlib import *

def assert_equal(aa, bb):
    assert aa == bb


def test_next_power_of_two():
    assert_equal(next_power_of_two(2), 2)
    assert_equal(next_power_of_two(3), 4)

def test_is_power_of_two():
    assert_equal(is_power_of_two(2), True)
    assert_equal(is_power_of_two(3), False)
    assert_equal(is_power_of_two(8), True)
    assert_equal(is_power_of_two(9), False)