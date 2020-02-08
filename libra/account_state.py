from __future__ import annotations
from canoser import Struct, Uint8, Uint64
from libra.event import EventHandle
import libra
from libra.account_config import AccountConfig
from io import StringIO
from typing import Optional


class AccountState(Struct):
    _fields = [
        ('ordered_map', {bytes: bytes})
    ]

    @classmethod
    def from_blob_or_default(cls, blob: Optional[bytes]) -> AccountState:
        if blob is None:
            return AccountState({})
        else:
            return AccountState.deserialize(blob)

    def get(self, path) -> Optional[bytes]:
        if path in self.ordered_map:
            return self.ordered_map[path]
        else:
            return None

    def get_resource(self) -> Optional[AccountResource]:
        path = AccountConfig.account_resource_path()
        resource = self.get(path)
        if resource:
            return libra.AccountResource.deserialize(resource)
        else:
            return None

    def to_json_serializable(self):
        amap = super().to_json_serializable()
        ar = self.get_resource()
        if ar:
            amap["account_resource_path"] = AccountConfig.account_resource_path().hex()
            amap["decoded_account_resource"] = ar.to_json_serializable()
        return amap
