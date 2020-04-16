from libra.libra_timestamp import *
from canoser import Uint64
import pytest

def test_libra_timestamp():
    time = LibraTimestampResource.deserialize(Uint64.encode(3))
    assert time.libra_timestamp.microseconds == 3
