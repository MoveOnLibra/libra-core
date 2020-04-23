from __future__ import annotations
from libra.access_path import AccessPath, Accesses
from libra.account_config import AccountConfig
from libra.language_storage import StructTag, TypeTag
# from move_core_types.identifier import IdentStr, Identifier
from typing import List

Identifier = str


class MoveResource:
    MODULE_NAME: str
    STRUCT_NAME: str

    @classmethod
    def module_identifier(cls) -> Identifier:
        return cls.MODULE_NAME

    @classmethod
    def struct_identifier(cls) -> Identifier:
        return cls.STRUCT_NAME

    @classmethod
    def type_params(cls) -> List[TypeTag]:
        return []

    @classmethod
    def struct_tag(cls) -> StructTag:
        return StructTag(
            AccountConfig.core_code_address_bytes(),
            cls.module_identifier(),
            cls.struct_identifier(),
            cls.type_params()
        )

    @classmethod
    def resource_path(cls) -> bytes:
        return AccessPath.resource_access_vec(cls.struct_tag(), Accesses.empty())
