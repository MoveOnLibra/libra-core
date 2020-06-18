from __future__ import annotations
from libra.access_path import AccessPath, Accesses
from libra.account_address import Address
from libra.account_config import CORE_CODE_ADDRESS
from libra.event import EventHandle
from libra.language_storage import StructTag, TypeTag
from libra.move_resource import MoveResource
from libra.rustlib import bail
from canoser import Struct, Uint64
from typing import Optional

# To register an on-chain config in Rust:
# 1. Implement the `OnChainConfig` trait for the Rust representation of the config
# 2. Add the config's `ConfigID` to `ON_CHAIN_CONFIG_REGISTRY`


class ConfigID(Struct):
    _fields = [
        ('v0', str),
        ('v1', str),
    ]

    def access_path(self) -> AccessPath:
        return access_path_for_config(
            Address.from_hex_literal(self.v0),
            self.v1,
        )


class OnChainConfigPayload(Struct):
    _fields = [
        ('epoch', Uint64),
        ('configs', {ConfigID: bytes}),
    ]

    def get(self, T: OnChainConfig) -> OnChainConfig:
        if T.CONFIG_ID not in self.configs:
            bail("[on-chain cfg] config not in payload")

        bytes = self.configs[T.CONFIG_ID]
        return T.deserialize_into_config(bytes)


# Trait to be implemented by a storage type from which to read on-chain configs
class ConfigStorage:
    def fetch_config(self, access_path: AccessPath) -> Optional[bytes]:
        bail("unimplemented!")


# Trait to be implemented by a Rust struct representation of an on-chain config
# that is stored in storage as a deserialized byte array
class OnChainConfig:
    # association_address
    ADDRESS: str = "0xA550C18"
    IDENTIFIER: str

    @classmethod
    def get_config_id(cls):
        return ConfigID(cls.ADDRESS, cls.IDENTIFIER)

    # Single-round LCS deserialization from bytes to `Self`
    # This is the expected deserialization pattern for most Rust representations,
    # but sometimes `deserialize_into_config` may need an extra customized round of deserialization
    # (e.g. enums like `VMPublishingOption`)
    # In the override, we can reuse this default logic via this function
    # Note: we cannot directly call the default `deserialize_into_config` implementation
    # in its override - this will just refer to the override implementation itself
    @classmethod
    def deserialize_default_impl(cls, v: bytes) -> OnChainConfig:
        return cls.deserialize(v)

    # Function for deserializing bytes to `Self`
    # It will by default try one round of LCS deserialization directly to `Self`
    # The implementation for the concrete type should override this function if this
    # logic needs to be customized
    @classmethod
    def deserialize_into_config(cls, v: bytes) -> OnChainConfig:
        return cls.deserialize_default_impl(v)

    @classmethod
    def fetch_config(cls, storage: ConfigStorage) -> Optional[OnChainConfig]:
        path = cls.get_config_id().access_path()
        v = storage.fetch_config(path)
        return cls.deserialize_into_config(v)


def access_path_for_config(address: Address, config_name: str) -> AccessPath:
    ty = TypeTag('Struct', StructTag(
        CORE_CODE_ADDRESS,
        config_name,
        config_name,
        [],
    ))
    tag = StructTag(
        CORE_CODE_ADDRESS,
        "LibraConfig",
        "LibraConfig",
        [ty],
    )
    return AccessPath(
        address,
        AccessPath.resource_access_vec(tag, Accesses.empty())
    )


class ConfigurationResource(Struct, MoveResource):
    _fields = [
        ('epoch', Uint64),
        ('last_reconfiguration_time', Uint64),
        ('events', EventHandle),
    ]

    MODULE_NAME: str = "LibraConfig"
    STRUCT_NAME: str = "Configuration"
