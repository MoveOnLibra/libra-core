from canoser import Struct, Uint64, Uint8, BytesT
from libra.hasher import HashValue
from libra.account_address import Address
from libra.account_config import AccountConfig
from libra.event import EventKey, EventHandle
from libra.access_path import AccessPath, Accesses
from libra.language_storage import StructTag
from libra.crypto.ed25519 import ED25519_SIGNATURE_LENGTH
from typing import List

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


LIBRA_BLOCK_MODULE_NAME = "LibraBlock"
BLOCK_STRUCT_NAME = "BlockMetadata"

def libra_block_module_name():
    return LIBRA_BLOCK_MODULE_NAME


def block_struct_name():
    return BLOCK_STRUCT_NAME


def libra_block_tag() -> StructTag:
    return StructTag(
        AccountConfig.core_code_address_bytes(),
        LIBRA_BLOCK_MODULE_NAME,
        BLOCK_STRUCT_NAME,
        []
    )


# The access path where the BlockMetadata resource is stored.
LIBRA_BLOCK_RESOURCE_PATH = AccessPath.resource_access_vec(libra_block_tag(), Accesses.empty())

# The path to the new block event handle under a LibraBlock.BlockMetadata resource.
NEW_BLOCK_EVENT_PATH = LIBRA_BLOCK_RESOURCE_PATH + b"/new_block_event/"


class LibraBlockResource(Struct):
    _fields = [
        ('height', Uint64),
        ('new_block_events', EventHandle),
    ]

class NewBlockEvent(Struct):
    _fields = [
        ('round', Uint64),
        ('proposer', Address),
        ('votes', [Address]),
        ('timestamp', Uint64),
    ]
