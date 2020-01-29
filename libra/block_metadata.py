from canoser import Struct, Uint64, Uint8, BytesT
from libra.hasher import HashValue
from libra.account_address import Address
from libra.crypto.ed25519 import ED25519_SIGNATURE_LENGTH


class BlockMetadata(Struct):
    _fields = [
        ('id', HashValue),
        ('timestamp_usecs', Uint64),
        ('previous_block_votes', {Address: BytesT(ED25519_SIGNATURE_LENGTH)}),
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