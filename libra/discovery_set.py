from canoser import DelegateT, Struct
from libra.account_config import AccountConfig
from libra.event import EventKey, EventHandle
from libra.discovery_info import DiscoveryInfo
from libra.access_path import AccessPath
from libra.move_resource import MoveResource


class DiscoverySet(DelegateT):
    delegate_type = [DiscoveryInfo]

    @classmethod
    def change_event_path(cls) -> bytes:
        return DiscoverySetResource.resource_path() + b"/change_events_count/"

    @classmethod
    def global_change_event_path(cls) -> AccessPath:
        return AccessPath(
            AccountConfig.discovery_set_address_bytes(),
            DiscoverySet.change_event_path()
        )

    @classmethod
    def change_event_key(cls):
        return EventKey.new_from_address(AccountConfig.discovery_set_address(), 2)


class DiscoverySetResource(Struct, MoveResource):
    _fields = [
        # The current discovery set. Updated only at epoch boundaries via reconfiguration.
        ('discovery_set', DiscoverySet),
        # Handle where discovery set change events are emitted
        ('change_events', EventHandle),
    ]

    MODULE_NAME: str = "LibraSystem"
    STRUCT_NAME: str = "DiscoverySet"
