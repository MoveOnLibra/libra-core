from canoser import DelegateT, Struct, Uint64
from libra.validator_public_keys import ValidatorPublicKeys
from libra.account_config import AccountConfig
from libra.account_address import Address
from libra.language_storage import StructTag
from libra.access_path import AccessPath
from libra.event import EventKey, EventHandle

class ValidatorSet(DelegateT):
    delegate_type = [ValidatorPublicKeys]

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
    def from_proto(cls, next_validator_set_proto):
        ret = []
        for keys in next_validator_set_proto.validator_public_keys:
            ret.append(ValidatorPublicKeys.from_proto(keys))
        return ret


class ValidatorSetResource(Struct):
    _fields = [
        ('validator_set', ValidatorSet),
        ('last_reconfiguration_time', Uint64),
        ('change_events', EventHandle)
    ]
