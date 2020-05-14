from canoser import Struct, Uint64, RustEnum
from libra.hasher import gen_hasher
from libra.language_storage import TypeTag
from libra.account_config import SentPaymentEvent, ReceivedPaymentEvent
from libra.event import EventKey
from libra.proto_helper import ProtoHelper


class ContractEventV0(Struct):
    _fields = [
        ('key', EventKey),
        ('sequence_number', Uint64),  # better name is 'event_seq_num'
        ('type_tag', TypeTag),
        ('event_data', bytes)
    ]


class ContractEvent(RustEnum):
    _enums = [
        ('V0', ContractEventV0),
    ]

    @property
    def key(self):
        return self.value.key

    @property
    def sequence_number(self):
        return self.value.sequence_number

    @property
    def type_tag(self):
        return self.value.type_tag

    @property
    def event_data(self):
        return self.value.event_data

    def hash(self):
        shazer = gen_hasher(b"libra_types::contract_event::ContractEvent")
        shazer.update(self.serialize())
        return shazer.digest()

    def to_proto(self):
        proto = ProtoHelper.new_proto_by_name("Event")
        proto.key = self.value.key
        proto.sequence_number = self.value.sequence_number
        proto.type_tag = self.value.type_tag.serialize()
        proto.event_data = self.value.event_data
        return proto

    @classmethod
    def from_proto(cls, event_proto):
        ret = ContractEventV0()
        ret.key = event_proto.key
        ret.sequence_number = event_proto.sequence_number
        ret.type_tag = TypeTag.deserialize(event_proto.type_tag)
        ret.event_data = event_proto.event_data
        if ret.type_tag.Struct and ret.type_tag.value.is_pay_tag():
            if ret.type_tag.value.name == "SentPaymentEvent":
                ret.event_data_decode = SentPaymentEvent.deserialize(event_proto.event_data)
            elif ret.type_tag.value.name == "ReceivedPaymentEvent":
                ret.event_data_decode = ReceivedPaymentEvent.deserialize(event_proto.event_data)
            else:
                raise AssertionError(f"Unknown event: {ret.type_tag.value}")
        return cls('V0', ret)

    @classmethod
    def from_proto_event_with_proof(cls, event_with_proof):
        ret = cls.from_proto(event_with_proof.event)
        ret.value.transaction_version = event_with_proof.transaction_version
        ret.value.event_index = event_with_proof.event_index
        return ret

    def to_json_serializable(self):
        amap = self.value.to_json_serializable()
        if hasattr(self.value, 'transaction_version'):
            amap["transaction_version"] = self.value.transaction_version
        if hasattr(self.value, 'event_index'):
            amap["event_index"] = self.value.event_index
        if hasattr(self.value, 'event_data_decode'):
            amap["event_data_decode"] = self.value.event_data_decode.to_json_serializable()
        return amap
