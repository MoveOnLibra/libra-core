from __future__ import annotations
from canoser import Struct, Uint64, RustEnum, DelegateT
from libra.account_address import Address
from libra.language_storage import ModuleId, StructTag, ResourceKey
from typing import List, Mapping, Optional

# SEPARATOR is used as a delimiter between fields. It should not be a legal part of any identifier
# in the language
SEPARATOR = '/'


class Field(DelegateT):
    delegate_type = str  # Identifier


class Access(RustEnum):
    _enums = [
        ('Field', str),
        ('Index', Uint64)
    ]


class Accesses(DelegateT):
    delegate_type = [Access]

    @staticmethod
    def as_separated_string(obj: List[Access]) -> str:
        path = ""
        for access in obj:
            if access.Field:
                path += access.value
            elif access.Index:
                path += str(access.value)
            else:
                raise AssertionError("Unreachable")
            path += SEPARATOR
        return path

    @classmethod
    def empty(cls) -> Accesses:
        return []


class AccessPath(Struct):
    _fields = [
        ('address', Address),
        ('path', bytes)
    ]

    CODE_TAG = 0
    RESOURCE_TAG = 1

    CODE_MAP: Mapping[bytes, StructTag] = {}
    RESOURCE_MAP: Mapping[bytes, StructTag] = {}

    @classmethod
    def parse_access_path(cls, path: bytes) -> StructTag:
        if path[0] == cls.CODE_TAG:
            return cls.CODE_MAP[path]
        else:
            return cls.RESOURCE_MAP[path]

    @classmethod
    def try_parse_access_path(cls, path: bytes) -> Optional[StructTag]:
        try:
            return cls.parse_access_path(path)
        except KeyError:
            return None

    def parse_path(self) -> StructTag:
        return AccessPath.parse_access_path(self.path)

    @classmethod
    def resource_access_vec(cls, tag: StructTag, accesses: List[Access]) -> bytes:
        ret = bytes([cls.RESOURCE_TAG])
        ret += tag.hash()
        # We don't need accesses in production right now. Accesses are appended here just for
        # passing the old tests.
        astr = Accesses.as_separated_string(accesses)
        ret += str.encode(astr)
        cls.RESOURCE_MAP[ret] = tag
        return ret

    # Convert Accesses into a byte offset which would be used by the storage layer to resolve
    # where fields are stored.
    def resource_access_path(key: ResourceKey, accesses: List[Access]) -> AccessPath:
        path = AccessPath.resource_access_vec(key.type_, accesses)
        return AccessPath(key.address, path)

    @classmethod
    def code_access_path_vec(cls, key: ModuleId) -> bytes:
        ret = bytes([cls.CODE_TAG])
        ret += key.hash()
        cls.CODE_MAP[ret] = key
        return ret

    @classmethod
    def code_access_path(cls, key: ModuleId) -> AccessPath:
        path = AccessPath.code_access_path_vec(key)
        return AccessPath(key.address, path)

    def __hash__(self):
        return (self.address, self.path).__hash__()

    def __lt__(self, other):
        return self.serialize().__lt__(other.serialize())

    def to_json_serializable(self):
        amap = super().to_json_serializable()
        try:
            obj = self.parse_path()
            amap["parsed_path"] = {
                obj.__class__.__qualname__: obj.to_json_serializable()
            }
        except Exception:
            pass
        return amap
