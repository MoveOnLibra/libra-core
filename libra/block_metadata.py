from canoser import Struct, Uint64
from libra.hasher import HashValue
from libra.account_address import Address
from libra.account_config import AccountConfig
from libra.event import EventKey, EventHandle
from libra.move_resource import MoveResource
from typing import List


class LibraBlockResource(Struct, MoveResource):
    _fields = [
        ('height', Uint64),
        ('new_block_events', EventHandle),
    ]

    MODULE_NAME: str = "LibraBlock"
    STRUCT_NAME: str = "BlockMetadata"


class BlockMetadata(Struct):
    _fields = [
        ('id', HashValue),
        ('round', Uint64),
        ('timestamp_usecs', Uint64),
        ('previous_block_votes', [Address]),
        ('proposer', Address)
    ]

    def to_json_serializable(self):
        amap = super().to_json_serializable()
        if hasattr(self, 'transaction_info'):
            amap["transaction_info"] = self.transaction_info.to_json_serializable()
        if hasattr(self, 'events'):
            amap["events"] = [x.to_json_serializable() for x in self.events]
        if hasattr(self, 'version'):
            amap["version"] = self.version
        if hasattr(self, 'success'):
            amap["success"] = self.success
        return amap

    def voters(self) -> List[Address]:
        return self.previous_block_votes


def new_block_event_key() -> EventKey:
    return EventKey.new_from_address(AccountConfig.association_address(), 2)


# The path to the new block event handle under a LibraBlock.BlockMetadata resource.
NEW_BLOCK_EVENT_PATH = LibraBlockResource.resource_path() + b"/new_block_event/"


class NewBlockEvent(Struct):
    _fields = [
        ('round', Uint64),
        ('proposer', Address),
        ('votes', [Address]),
        ('timestamp', Uint64),
    ]
