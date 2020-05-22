from __future__ import annotations
from canoser import Struct
from libra.event import EventHandle
from libra.account_config import AccountConfig
from libra.account_resource import AccountResource, BalanceResource
from libra.block_metadata import NEW_BLOCK_EVENT_PATH
from libra.discovery_set import DiscoverySetResource, DiscoverySet
from libra.move_resource import MoveResource
from libra.on_chain_config import ConfigurationResource, ValidatorSet
from libra.validator_config import ValidatorConfigResource
from libra.libra_timestamp import LibraTimestampResource
from libra.block_metadata import LibraBlockResource
from libra.rustlib import bail
from typing import Optional, Any, List, Mapping


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

    def get_resource(self, path: bytes, T: Any) -> Optional[Any]:
        resource = self.get(path)
        if resource:
            return T.deserialize(resource)
        else:
            return None

    def get_move_resource(self, T: MoveResource) -> MoveResource:
        return self.get_resource(T.resource_path(), T)

    def to_json_serializable(self):
        amap = super().to_json_serializable()
        ar = self.get_account_resource()
        if ar:
            amap["account_resource_path"] = AccountResource.resource_path().hex()
            amap["decoded_account_resource"] = ar.to_json_serializable()
        return amap

    def get_account_resource(self) -> Optional[AccountResource]:
        return self.get_move_resource(AccountResource)

    def get_balance_resource(self, code: str) -> Optional[BalanceResource]:
        tag = AccountConfig.type_tag_for_currency_code(code)
        path = BalanceResource.access_path_for(tag)
        return self.get_resource(path, BalanceResource)

    def get_balance_resources(self, currency_codes: List[str]) -> Mapping[str, BalanceResource]:
        # TODO: update this to use BalanceResource::resource_path once that takes type
        # parameters
        return {code: self.get_balance_resource(code) for code in currency_codes}




    def get_configuration_resource(self) -> Optional[ConfigurationResource]:
        return self.get_move_resource(ConfigurationResource)

    def get_discovery_set_resource(self) -> Optional[DiscoverySetResource]:
        return self.get_move_resource(DiscoverySetResource)

    def get_libra_timestamp_resource(self) -> Optional[LibraTimestampResource]:
        return self.get_move_resource(LibraTimestampResource)

    def get_validator_config_resource(self) -> Optional[ValidatorConfigResource]:
        return self.get_move_resource(ValidatorConfigResource)

    def get_validator_set(self) -> Optional[ValidatorSet]:
        return self.get_resource(
            ValidatorSet.get_config_id().access_path().path,
            ValidatorSet,
        )

    def get_libra_block_resource(self) -> Optional[LibraBlockResource]:
        return self.get_move_resource(LibraBlockResource)

    def get_event_handle_by_query_path(self, query_path: bytes) -> EventHandle:
        if AccountConfig.account_received_event_path() == query_path:
            return self.get_account_resource().received_events

        elif AccountConfig.account_sent_event_path() == query_path:
            return self.get_account_resource().sent_events

        elif DiscoverySet.change_event_path() == query_path:
            return self.get_discovery_set_resource().change_events

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

    @classmethod
    def try_from(cls,
                 account_resource: AccountResource,
                 balance_resource: BalanceResource,
                 ) -> AccountState:
        btree_map = {}
        btree_map[AccountResource.resource_path()] = account_resource.serialize()
        btree_map[BalanceResource.resource_path()] = balance_resource.serialize()
        return cls(btree_map)
