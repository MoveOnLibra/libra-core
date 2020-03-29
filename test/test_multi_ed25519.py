from libra.crypto.multi_ed25519 import *

def test_bitmap():
    bitmap = [0b0100_0000 , 0b1111_1111, 0 , 0b1000_0000 ]
    assert (not bitmap_get_bit(bitmap, 0))
    assert (bitmap_get_bit(bitmap, 1))
    for i in range(8,16):
        assert (bitmap_get_bit(bitmap, i))

    for i in range(16,24):
        assert (not bitmap_get_bit(bitmap, i))

    assert (bitmap_get_bit(bitmap, 24))
    assert (not bitmap_get_bit(bitmap, 31))
    assert bitmap_last_set_bit(bitmap) == 24

    bitmap_set_bit(bitmap, 30)
    assert (bitmap_get_bit(bitmap, 30))
    assert bitmap_last_set_bit(bitmap) == 30

