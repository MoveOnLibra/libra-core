from libra.hasher import gen_hasher

class AccountStateBlob:
    def __init__(self, blob):
        self.blob = blob

    @classmethod
    def from_proto(cls, proto):
        return cls(proto.blob)

    def hash(self):
        shazer = gen_hasher(b"AccountStateBlob::libra_types::account_state_blob")
        shazer.update(self.blob)
        return shazer.digest()
