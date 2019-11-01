from canoser import *
from libra.hasher import gen_hasher
from libra.language_storage import TypeTag
from libra.account_config import AccountEvent

EVENT_KEY_LENGTH = 32

class EventKey(DelegateT):
    delegate_type = [Uint8, EVENT_KEY_LENGTH]


class EventHandle(Struct):
    _fields = [
        ('count', Uint64),
        ('key', EventKey)
    ]


class ContractEvent(Struct):
    _fields = [
        ('key', EventKey),
        ('sequence_number', Uint64),
        ('type_tag', TypeTag),
        ('event_data', [Uint8])
    ]

    @classmethod
    def from_proto(cls, event_proto):
        ret = cls()
        ret.key = bytes_to_int_list(event_proto.key)
        ret.sequence_number = event_proto.sequence_number
        ret.type_tag = TypeTag.deserialize(event_proto.type_tag)
        ret.event_data = bytes_to_int_list(event_proto.event_data)
        try:
            ret.event_data_decode = AccountEvent.deserialize(event_proto.event_data)
        except Execption:
            pass
        return ret

    @classmethod
    def from_proto_event_with_proof(cls, event_with_proof):
        ret = cls.from_proto(event_with_proof.event)
        ret.transaction_version = event_with_proof.transaction_version
        ret.event_index = event_with_proof.event_index
        return ret

    def to_json_serializable(self):
        amap = super().to_json_serializable()
        if hasattr(self, 'transaction_version'):
            amap["transaction_version"] = self.transaction_version
        if hasattr(self, 'event_index'):
            amap["event_index"] = self.event_index
        if hasattr(self, 'event_data_decode'):
            amap["event_data_decode"] = self.event_data_decode.to_json_serializable()
        return amap

    def hash(self):
        shazer = gen_hasher(b"ContractEvent")
        shazer.update(self.serialize())
        return shazer.digest()
