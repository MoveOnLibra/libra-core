from canoser import DelegateT, Struct
from libra.account_config import AccountConfig
from libra.event import EventKey, EventHandle
from libra.discovery_info import DiscoveryInfo
from libra.validator_set import ValidatorSet
from libra.access_path import AccessPath

class DiscoverySet(DelegateT):
    delegate_type = [DiscoveryInfo]

    DISCOVERY_SET_STRUCT_NAME = "DiscoverySet"

    @classmethod
    def tag(cls):
        return StructTag(
            cls.core_code_address_bytes(),
            ValidatorSet.LIBRA_SYSTEM_MODULE_NAME,
            cls.DISCOVERY_SET_STRUCT_NAME,
            []
        )

    @classmethod
    def resource_path(cls):
        return bytes(AccessPath.resource_access_vec(cls.tag(), []))

    @classmethod
    def change_event_path(cls) -> bytes:
        return cls.resource_path() + b"/change_events_count/"

    @classmethod
    def global_change_event_path(cls) -> AccessPath:
        return AccessPath.resource_access_vec(cls.tag(), [])

    @classmethod
    def change_event_key(cls):
        return EventKey.new_from_address(AccountConfig.discovery_set_address(), 2)


class DiscoverySetResource(Struct):
    _fields = [
        # The current discovery set. Updated only at epoch boundaries via reconfiguration.
        ('discovery_set', DiscoverySet),
        # Handle where discovery set change events are emitted
        ('change_events', EventHandle),
    ]

