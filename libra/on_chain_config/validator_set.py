from canoser import RustEnum, Struct
from libra.validator_info import ValidatorInfo
from libra.account_config import AccountConfig
from libra.language_storage import StructTag
from libra.access_path import AccessPath
from libra.event import EventKey
from libra.on_chain_config.on_chain_config import OnChainConfig


class ConsensusScheme(RustEnum):
    _enums = [
        ('Ed25519', None),
    ]


class ValidatorSet(Struct, OnChainConfig):
    _fields = [
        ('scheme', ConsensusScheme),
        ('payload', [ValidatorInfo])
    ]

    # validator_set_address
    ADDRESS: str = "0x1D8"
    IDENTIFIER: str = "LibraSystem"

    LIBRA_SYSTEM_MODULE_NAME = "LibraSystem"
    VALIDATOR_SET_STRUCT_NAME = "ValidatorSet"

    VALIDATOR_SET_MODULE_NAME = LIBRA_SYSTEM_MODULE_NAME

    @classmethod
    def tag(cls) -> StructTag:
        return StructTag(
            AccountConfig.core_code_address_bytes(),
            cls.VALIDATOR_SET_MODULE_NAME,
            cls.VALIDATOR_SET_STRUCT_NAME,
            []
        )

    @classmethod
    def resource_path(cls):
        return bytes(AccessPath.resource_access_vec(cls.tag(), []))

    @classmethod
    def change_event_path(cls) -> bytes:
        return cls.resource_path() + b"/change_events_count/"

    @classmethod
    def change_event_key(cls):
        return EventKey.new_from_address(AccountConfig.validator_set_address(), 2)

    @classmethod
    def from_proto(cls, proto):
        return ValidatorSet.deserialize(proto.bytes)
