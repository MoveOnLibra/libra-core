from canoser import Uint64
from collections.abc import Iterable


usize = Uint64


def next_power_of_two(num):
    for i in range(99999999):
        pow2 = pow(2, i)
        if num <= pow2:
            return pow2


def is_power_of_two(num):
    return next_power_of_two(num) == num


def trailing_zeros(longint):
    manipulandum = bin(longint)
    return len(manipulandum) - len(manipulandum.rstrip('0'))


def leading_zeros(longint, bitlen=64):
    if longint == 0:
        return bitlen
    manipulandum = bin(longint)
    assert manipulandum[0:2] == '0b'
    return bitlen + 2 - len(manipulandum)


def count_ones(num):
    return bin(num)[2:].count('1')


def resize_list(alist, size, value):
    if len(alist) >= size:
        return alist[0:size]
    else:
        diff = size - len(alist)
        for _i in range(diff):
            alist.append(value)
        return alist


def flatten(ite):
    ret = []
    for sublist in ite:
        if sublist is not None:
            if isinstance(sublist, Iterable):
                ret.extend([x for x in sublist if x is not None])
            else:
                ret.append(sublist)
    return ret


def take_n(ite, n):
    return [x for i, x in enumerate(ite) if i < n]


def nth(ite, n):
    return next(x for i, x in enumerate(ite) if i == n)

# Get an item from list with index, return None if not exsits.


def list_get(alist, n):
    if n < 0 or n > len(alist):
        return None
    return alist[n]


def position(alist, lambdaf):
    for idx, item in enumerate(alist):
        if lambdaf(item):
            return idx
    return None


def assert_equal(aa, bb):
    assert aa == bb


def assert_ne(aa, bb):
    assert aa != bb


def assert_true(aa):
    assert aa


def bail(hint, *args):
    errstr = hint.format(*args)
    raise AssertionError(errstr)


def ensure(exp, hint, *args):
    if not exp:
        bail(hint, *args)


def format_str(astr, *args, **kwargs):
    return astr.format(*args, **kwargs)


def snake_to_camel(word):
    return ''.join(x.capitalize() for x in word.split('_'))
