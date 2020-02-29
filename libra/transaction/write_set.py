from __future__ import annotations
from canoser import Struct, Uint8, RustEnum
from libra.access_path import AccessPath


class WriteOp(RustEnum):
    _enums = [
        ('Deletion', None),
        ('Value', bytes)
    ]


class WriteSet(Struct):
    """`WriteSet` contains all access paths that one transaction modifies. Each of them is a `WriteOp`
    where `Value(val)` means that serialized representation should be updated to `val`, and
    `Deletion` means that we are going to delete this access path.
    """
    _fields = [
        ('write_set', [(AccessPath, WriteOp)])
    ]

    def freeze(self) -> WriteSet:
        # TODO: add structural validation
        return self

    def append(self, tup):
        self.write_set.append(tup)

WriteSetMut = WriteSet