from libra.move_resource import MoveResource
from libra.libra_timestamp import *
import pytest

def test_move_resource():
    assert LibraTimestampResource.struct_identifier() == LibraTimestampResource.STRUCT_NAME
    assert LibraTimestampResource.type_params() == []
    assert LibraTimestampResource.struct_tag().module == LibraTimestampResource.MODULE_NAME
    assert LibraTimestampResource.struct_tag().name == LibraTimestampResource.STRUCT_NAME
