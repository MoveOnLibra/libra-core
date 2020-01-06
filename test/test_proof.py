import libra.proto.proof_pb2 as proof_pb2, events_pb2

import libra
from libra.transaction import TransactionInfo
from libra.hasher import TransactionAccumulatorHasher
from libra.proof import *
from libra.get_with_proof import gen_events_resp_idxs
from canoser import Uint64
import pytest
#import pdb

def test_zero_accumulator_proof():
    proof = proof_pb2.AccumulatorProof()
    ap = AccumulatorProof.from_proto(proof)
    assert len(ap.siblings) == 0


def test_ensure():
    ensure(1==1, "{} != {}", 1, 1)
    with pytest.raises(AssertionError):
        ensure(1==2, "{} != {}", 1, 2)
    with pytest.raises(AssertionError):
        ensure(1==2, "1 != 2")

def test_gen_events_resp_idxs():
    assert [] == gen_events_resp_idxs(2, 3, True, 1)
    assert [] == gen_events_resp_idxs(3, 3, True, 1)
    assert [2] == gen_events_resp_idxs(3, 2, True, 1)
    assert [2] == gen_events_resp_idxs(3, 2, True, 2)
    assert [0, 1] == gen_events_resp_idxs(3, 0, True, 2)
    assert [0, 1, 2] == gen_events_resp_idxs(3, 0, True, 4)
    assert [] == gen_events_resp_idxs(2, 3, False, 1)
    assert [] == gen_events_resp_idxs(3, 3, False, 1)
    assert [0] == gen_events_resp_idxs(3, 0, False, 2)
    assert [] == gen_events_resp_idxs(3, 3, False, 1)
    assert [2] == gen_events_resp_idxs(3, 2, False, 1)
    assert [2, 1] == gen_events_resp_idxs(3, 2, False, 2)
    assert [2, 1, 0] == gen_events_resp_idxs(3, 2, False, 3)
    assert [2, 1, 0] == gen_events_resp_idxs(3, 2, False, 4)
    assert [2] == gen_events_resp_idxs(3, Uint64.max_value, False, 1)
    assert [2, 1] == gen_events_resp_idxs(3, Uint64.max_value, False, 2)
    assert [2, 1, 0] == gen_events_resp_idxs(3, Uint64.max_value, False, 3)
    assert [2, 1, 0] == gen_events_resp_idxs(3, Uint64.max_value, False, 4)
