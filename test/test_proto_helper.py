import pytest
import libra
from libra.validator_public_keys import ValidatorPublicKeys
from libra.proto_helper import *
from libra.proof import *


def test_simple():
    assert "a" == ProtoHelper.to_proto("a")
    assert b"a" == ProtoHelper.to_proto(b"a")
    assert 123 == ProtoHelper.to_proto(123)

def test_canoser():
    vkeys = ValidatorPublicKeys()
    zero = ProtoHelper.to_proto(vkeys)
    with pytest.raises(TypeError):
        ValidatorPublicKeys.from_proto(zero)
    vkeys.account_address = b'\x01' * 32
    vkeys.consensus_public_key = b'\x02' * 32
    vkeys.consensus_voting_power = 3
    vkeys.network_signing_public_key = b''
    vkeys.network_identity_public_key = b'\x05' * 32
    proto = ProtoHelper.to_proto(vkeys)
    assert proto.account_address == b'\x01' * 32
    assert proto.consensus_public_key == b'\x02' * 32
    assert proto.consensus_voting_power == 3
    assert proto.network_signing_public_key == b''
    assert proto.network_identity_public_key == b'\x05' * 32
    v2 = ValidatorPublicKeys.from_proto(proto)
    assert vkeys == v2


def test_tnxs_with_proof():
    tproof = TransactionListWithProof.new_empty()
    proto = ProtoHelper.to_proto(tproof)
    assert isinstance(proto, libra.proto.transaction_pb2.TransactionListWithProof)
    print(proto)
