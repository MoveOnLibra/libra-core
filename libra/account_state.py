from __future__ import annotations
from canoser import Struct, Uint8, Uint64
from libra.event import EventHandle
import libra
from libra.account_config import AccountConfig
from libra.account_resource import AccountResource, BalanceResource
from libra.block_metadata import NEW_BLOCK_EVENT_PATH
from libra.discovery_set import DiscoverySetResource, DiscoverySet
from libra.validator_set import ValidatorSetResource, ValidatorSet
# from libra.validator_config import ValidatorConfigResource

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

    def get_resource(self, path=None, T=AccountResource) -> Optional[obj]:
        if path is None:
            path = AccountConfig.account_resource_path()
        resource = self.get(path)
        if resource:
            return T.deserialize(resource)
        else:
            return None

    def to_json_serializable(self):
        amap = super().to_json_serializable()
        ar = self.get_resource()
        if ar:
            amap["account_resource_path"] = AccountConfig.account_resource_path().hex()
            amap["decoded_account_resource"] = ar.to_json_serializable()
        return amap


    def get_account_resource(self) -> Optional[AccountResource]:
        path = AccountConfig.account_resource_path()
        return self.get_resource(path)


    def get_balance_resource(self) -> Optional[BalanceResource]:
        path = AccountConfig.balance_resource_path()
        return self.get_resource(path, BalanceResource)


    def get_discovery_set_resource(self) -> Optional[DiscoverySetResource]:
        return self.get_resource(DISCOVERY_SET_RESOURCE_PATH, DiscoverySetResource)


    def get_libra_timestamp_resource(self) -> Optional[LibraTimestampResource]:
        return self.get_resource(LIBRA_TIMESTAMP_RESOURCE_PATH, LibraTimestampResource)


    def get_validator_config_resource(self) -> Optional[ValidatorConfigResource]:
        return self.get_resource(VALIDATOR_CONFIG_RESOURCE_PATH, ValidatorConfigResource)


    def get_validator_set_resource(self) -> Optional[ValidatorSetResource]:
        return self.get_resource(VALIDATOR_SET_RESOURCE_PATH, ValidatorSetResource)


    def get_libra_block_resource(self) -> Optional[LibraBlockResource]:
        return self.get_resource(LIBRA_BLOCK_RESOURCE_PATH, LibraBlockResource)


    def get_event_handle_by_query_path(self, query_path: bytes) -> EventHandle:
        if AccountConfig.account_received_event_path() == query_path:
            return self.get_account_resource().received_events

        elif AccountConfig.account_sent_event_path() == query_path:
            return self.get_account_resource().sent_events

        elif DISCOVERY_SET_CHANGE_EVENT_PATH == query_path:
            return self.get_discovery_set_resource().change_events

        elif VALIDATOR_SET_CHANGE_EVENT_PATH == query_path:
            return self.get_validator_set_resource().change_events

        elif NEW_BLOCK_EVENT_PATH == query_path:
            return self.get_libra_block_resource().new_block_events

        else:
            bail("Unrecognized query path: {}", query_path)


    def insert(self, key: bytes, value: bytes) -> None:
        self.ordered_map[key] = value


    def remove(self, key: bytes) -> Optional[bytes]:
        return self.ordered_map.pop(key)


    def is_empty(self) -> bool:
        return not self.ordered_map


    def try_from(
        account_resource: AccountResource,
        balance_resource:BalanceResource,
    ) -> AccountState:
        btree_map = {}
        btree_map[ACCOUNT_RESOURCE_PATH] = account_resource.serialize()
        btree_map[BALANCE_RESOURCE_PATH] = balance_resource.serialize()
        return cls(btree_map)
