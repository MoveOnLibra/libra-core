from libra.move_resource import MoveResource
from libra.libra_timestamp import *
import pytest

def test_move_resource():
    assert LibraTimestampResource.struct_identifier() == LibraTimestampResource.STRUCT_NAME
    assert LibraTimestampResource.type_params() == []
    assert LibraTimestampResource.struct_tag().module == LibraTimestampResource.MODULE_NAME
    assert LibraTimestampResource.struct_tag().name == LibraTimestampResource.STRUCT_NAME
    assert LibraTimestampResource.resource_path().hex() == '01be88f89b98ec9dc840cee32763bf9d155987bab54273367b671e29a66dba7825'
