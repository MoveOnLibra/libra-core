from libra.hasher import *
from canoser import DelegateT, Uint32, BytesT

def assert_equal(aa, bb):
    assert aa == bb

def assert_true(aa):
    assert aa == True


class Foo(DelegateT):
    delegate_type = Uint32

def test_default_hasher():
    # assert_equal(
    #     tst_only_hash(3, Foo),
    #     b""
    # )
    assert_equal(
        tst_only_hash(b"hello").hex(),
        "3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392"
    )
    assert_equal(
        tst_only_hash(b"world").hex(),
        "420baf620e3fcd9b3715b42b92506e9304d56e02d3a103499a3a292560cb66b2"
    )


def test_placeholder_hash():
    assert ACCUMULATOR_PLACEHOLDER_HASH == [65, 67, 67, 85, 77, 85, 76, 65, 84, 79, 82, 95, 80, 76, 65, 67, 69, 72, 79, 76, 68, 69, 82, 95, 72, 65, 83, 72, 0, 0, 0, 0]
    assert SPARSE_MERKLE_PLACEHOLDER_HASH == [83, 80, 65, 82, 83, 69, 95, 77, 69, 82, 75, 76, 69, 95, 80, 76, 65, 67, 69, 72, 79, 76, 68, 69, 82, 95, 72, 65, 83, 72, 0, 0]
    assert PRE_GENESIS_BLOCK_ID == [80, 82, 69, 95, 71, 69, 78, 69, 83, 73, 83, 95, 66, 76, 79, 67, 75, 95, 73, 68, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def test_common_prefix_nibbles_len():
    assert uint8_to_bits(b'hello'[0]) == '01101000'
    assert uint8_to_bits(b"HELLO"[0]) == '01001000'
    bits = bytes_to_bits(b'hello')
    assert len(bits) == 5*8
    assert bits == '0110100001100101011011000110110001101111'
    assert common_prefix_bits_len(b"hello", b"HELLO") == 2
    assert common_prefix_bits_len(b"h2", b"\xff2") == 0
    assert common_prefix_bits_len(b"hello", b"hello") == 40
