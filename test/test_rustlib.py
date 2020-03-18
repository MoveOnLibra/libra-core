from libra.rustlib import *
import pytest


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


def test_ensure():
    ensure(1==1, "{} != {}", 1, 1)
    with pytest.raises(AssertionError):
        ensure(1==2, "{} != {}", 1, 2)
    with pytest.raises(AssertionError):
        ensure(1==2, "1 != 2")

def test_flatten():
    assert flatten([]) == []
    assert flatten([None]) == []
    assert flatten([[]]) == []
    assert flatten([[None]]) == []
    assert flatten([[], None]) == []
    assert flatten([[1],[],[None]]) == [1]
    assert flatten([[None, 1], [None]]) == [1]
    assert flatten([[[2]]]) == [[2]]
    #not support 3 level nested.
    assert flatten(["alpha", "beta", "gamma"]) == ['a', 'l', 'p', 'h', 'a', 'b', 'e', 't', 'a', 'g', 'a', 'm', 'm', 'a']
    #not same result as rust: "alphabetagamma"
    assert flatten([1, 2]) == [1, 2]
    assert flatten([1, [2, 3], [4]]) == [1, 2, 3, 4]

def test_position():
    out = 'c'
    alist = ['a', 'b', 'c', 'd']
    lambdaf = lambda x: x == out
    assert position(alist, lambdaf) == 2
    assert position(alist, lambda x: x=='e') == None

def test_format_str():
    assert format_str("x{}{}", 2, 3) == "x23"
    assert format_str("x{}", 2) == "x2"
    assert format_str("x{name}", name=3) == "x3"
    assert format_str("x{}{key}{value}", 1, key=2, value=3) == "x123"