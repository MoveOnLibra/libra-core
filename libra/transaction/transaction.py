from canoser import RustEnum, Uint64
from libra.transaction.signed_transaction import SignedTransaction
from libra.transaction.change_set import ChangeSet
from libra.block_metadata import BlockMetadata
from libra.hasher import LCSCryptoHash
from libra.proto_helper import ProtoHelper

Version = Uint64


class Transaction(RustEnum, LCSCryptoHash):
    _enums = [
        ('UserTransaction', SignedTransaction),
        ('WaypointWriteSet', ChangeSet),
        ('BlockMetadata', BlockMetadata)
    ]

    def to_proto(self):
        proto = ProtoHelper.new_proto_obj(self)
        proto.transaction = self.serialize()
        return proto
