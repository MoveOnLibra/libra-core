from libra.hasher import gen_hasher
from canoser import Struct, Uint8


class AccountStateBlob(Struct):
    _fields = [
        ('blob', bytes)
    ]


    @classmethod
    def from_proto(cls, proto):
        return cls(proto.blob)

    def hash(self):
        shazer = gen_hasher(b"AccountStateBlob::libra_types::account_state_blob")
        shazer.update(self.blob)
        return shazer.digest()
