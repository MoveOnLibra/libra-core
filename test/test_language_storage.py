from libra.language_storage import *
from libra import Address
from canoser import Uint32
#import pdb


def test_struct_tag():
    tag1 = StructTag(b'1'*Address.LENGTH, 'm1', 'n1', [])
    tag2 = StructTag(b'2'*Address.LENGTH, 'm2', 'n2', [])
    tag1 = TypeTag('Struct' ,tag1)
    tag2 = TypeTag('Struct' ,tag2)
    tag3 = StructTag(b'3'*Address.LENGTH, 'm3', 'n3', [tag1, tag2])
    tag1s = tag1.serialize()
    tag2s = tag2.serialize()
    arrs = Uint32.serialize_uint32_as_uleb128(2) + tag1s + tag2s
    tag3s = tag3.serialize()
    assert tag3s.endswith(arrs)
    assert StructTag.deserialize(tag3s) == tag3