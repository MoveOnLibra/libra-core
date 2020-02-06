from canoser import RustEnum, Uint64
from libra.transaction.signed_transaction import SignedTransaction
from libra.transaction.write_set import WriteSet
from libra.block_metadata import BlockMetadata
from libra.hasher import gen_hasher
from libra.proto_helper import ProtoHelper

Version = Uint64

class Transaction(RustEnum):
    _enums = [
        ('UserTransaction', SignedTransaction),
        ('WriteSet', WriteSet),
        ('BlockMetadata', BlockMetadata)
    ]

    def hash(self):
        shazer = gen_hasher(b"Transaction::libra_types::transaction")
        shazer.update(self.serialize())
        return shazer.digest()

    def to_proto(self):
        proto = ProtoHelper.new_proto_obj(self)
        proto.transaction = self.serialize()
        return proto
