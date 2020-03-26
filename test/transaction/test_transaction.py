import libra
from libra import Address
from libra.crypto.ed25519 import ED25519_PRIVATE_KEY_LENGTH, ED25519_SIGNATURE_LENGTH
from libra.transaction import *
from canoser import Uint64
from libra.proto.get_with_proof_pb2 import UpdateToLatestLedgerRequest
import pytest
import nacl
import pdb


def test_raw_txn():
    a0 = libra.Account(b'0' * ED25519_PRIVATE_KEY_LENGTH)
    a1 = libra.Account(b'1' * ED25519_PRIVATE_KEY_LENGTH)
    assert RawTransaction.__doc__.startswith("RawTransaction is the portion of a transaction that a client signs")
    raw_tx = RawTransaction._gen_transfer_transaction(a0.address, 0, a1.address, 123)
    assert raw_tx.max_gas_amount == 400_000
    assert raw_tx.gas_unit_price == 0
    assert bytes(raw_tx.sender) == a0.address
    assert raw_tx.payload.enum_name == "Script"
    assert raw_tx.payload.index == 2
    assert raw_tx.payload.value_type == Script
    script = raw_tx.payload.value
    assert script.code == Script.get_script_bytecode("peer_to_peer_transfer")
    assert script.args[0].index == 1
    assert script.args[0].Address == True
    assert script.args[0].enum_name == 'Address'
    assert script.args[1].index == 0
    assert script.args[1].U64 == True
    assert script.args[1].value == 123


def test_raw_txn_with_metadata():
    a0 = libra.Account(b'0' * ED25519_PRIVATE_KEY_LENGTH)
    a1 = libra.Account(b'1' * ED25519_PRIVATE_KEY_LENGTH)
    raw_tx = RawTransaction._gen_transfer_transaction(a0.address, 0, a1.address, 9, metadata=bytes([2,3,4]))
    assert raw_tx.payload.value_type == Script
    script = raw_tx.payload.value
    assert script.code == Script.get_script_bytecode("peer_to_peer_transfer_with_metadata")
    assert script.args[0].index == 1
    assert script.args[0].Address == True
    assert script.args[0].enum_name == 'Address'
    assert script.args[1].index == 0
    assert script.args[1].U64 == True
    assert script.args[1].value == 9
    assert script.args[2].index == 2
    assert script.args[2].U8Vector == True
    assert script.args[2].value == bytes([2,3,4])


def test_signed_txn():
    a0 = libra.Account(b'0' * ED25519_PRIVATE_KEY_LENGTH)
    a1 = libra.Account(b'1' * ED25519_PRIVATE_KEY_LENGTH)
    raw_tx = RawTransaction._gen_transfer_transaction(a0.address, 0, a1.address, 123)
    stx = SignedTransaction.gen_from_raw_txn(raw_tx, a0)
    assert len(stx.signature) == ED25519_SIGNATURE_LENGTH
    stx.check_signature()
    sctx = raw_tx.sign(a0.private_key, a0.public_key)
    assert sctx.v0 == stx
    assert len(raw_tx.serialize()) == stx.raw_txn_bytes_len()
    with pytest.raises(nacl.exceptions.BadSignatureError):
        stx.signature = b'\0'*ED25519_SIGNATURE_LENGTH
        stx.check_signature()
    tx = Transaction('UserTransaction', stx)
    assert tx.to_proto().transaction == tx.serialize()

