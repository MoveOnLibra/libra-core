import pytest
import libra
from libra import Address
from libra.validator_info import ValidatorInfo
from libra.proto_helper import *
from libra.proof import *
from libra.get_with_proof import GetEventsByEventAccessPathResponse
from dataclasses import fields

def test_simple():
    assert "a" == ProtoHelper.to_proto("a")
    assert b"a" == ProtoHelper.to_proto(b"a")
    assert 123 == ProtoHelper.to_proto(123)

def test_canoser():
    vkeys = ValidatorInfo()
    zero = ProtoHelper.to_proto(vkeys)
    with pytest.raises(TypeError):
        ValidatorInfo.from_proto(zero)
    vkeys.account_address = b'\x01' * Address.LENGTH
    vkeys.consensus_public_key = b'\x02' * 32
    vkeys.consensus_voting_power = 3
    vkeys.network_signing_public_key = b''
    vkeys.network_identity_public_key = b'\x05' * 32
    proto = ProtoHelper.to_proto(vkeys)
    assert proto.account_address == b'\x01' * Address.LENGTH
    assert proto.consensus_public_key == b'\x02' * 32
    assert proto.consensus_voting_power == 3
    assert proto.network_signing_public_key == b''
    assert proto.network_identity_public_key == b'\x05' * 32
    v2 = ValidatorInfo.from_proto(proto)
    assert vkeys == v2


def test_tnxs_with_proof():
    fs = [(x.name, x.type) for x in fields(TransactionListWithProof)]
    assert fs[0] == ('transactions', typing.List[libra.transaction.transaction.Transaction])
    assert isinstance(fs[0][1], typing._GenericAlias)
    tproof = TransactionListWithProof.new_empty()
    proto = ProtoHelper.to_proto(tproof)
    assert isinstance(proto, libra.proto.transaction_pb2.TransactionListWithProof)
    print(proto)

def test_events_by_access_path():
    fs = [(x.name, x.type) for x in fields(GetEventsByEventAccessPathResponse)]
    assert fs[0] == ('events_with_proof', 'List[EventWithProof]')
    assert isinstance(fs[0][1], str) #TODO: This is Weird, why not typing class???
    resp = GetEventsByEventAccessPathResponse([], None)
    proto = ProtoHelper.to_proto(resp)
    assert isinstance(proto, libra.proto.get_with_proof_pb2.GetEventsByEventAccessPathResponse)
    print(proto)
