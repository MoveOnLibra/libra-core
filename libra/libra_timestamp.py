from __future__ import annotations
from libra.move_resource import MoveResource
from canoser import Struct, Uint64


class LibraTimestamp(Struct):
    _fields = [
        ('microseconds', Uint64),
    ]


class LibraTimestampResource(Struct, MoveResource):
    _fields = [
        ('libra_timestamp', LibraTimestamp),
    ]

    MODULE_NAME: str = "LibraTimestamp"
    STRUCT_NAME: str = "CurrentTimeMicroseconds"
