def next_power_of_two(num):
    for i in range(99999999):
        pow2 = pow(2, i)
        if num <= pow2:
            return pow2

def is_power_of_two(num):
    return next_power_of_two(num) == num


def trailing_zeros(longint):
  manipulandum = bin(longint)
  return len(manipulandum)-len(manipulandum.rstrip('0'))

def leading_zeros(longint, bitlen=64):
    if longint == 0:
        return bitlen
    manipulandum = bin(longint)
    assert manipulandum[0:2] == '0b'
    return bitlen + 2 - len(manipulandum)

def count_ones(num):
    return bin(num)[2:].count('1')
