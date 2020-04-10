import libra
from libra import Address
from libra.crypto.ed25519 import ED25519_PRIVATE_KEY_LENGTH, ED25519_SIGNATURE_LENGTH
from libra.transaction import *
from canoser import Uint64
from libra.proto.get_with_proof_pb2 import UpdateToLatestLedgerRequest
import pytest
import nacl
import pdb

def test_deser():
    blob = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\nU\x0c\x18\x01\x00\x00\x00\x00\x00\x00\x00\x02\x9c\x01\xa1\x1c\xeb\x0b\x01\x00\x06\x01=\x00\x00\x00\x04\x00\x00\x00\x03A\x00\x00\x00\n\x00\x00\x00\x05K\x00\x00\x00\x06\x00\x00\x00\x07Q\x00\x00\x00)\x00\x00\x00\x06z\x00\x00\x00\x10\x00\x00\x00\t\x8a\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x01\x01\x02\x00\x01\x00\x00\x03\x00\x01\x00\x03\x05\n\x02\x03\x00\x06<SELF>\x0cLibraAccount\x0fmint_to_address\x04main\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\xff\xff\x03\x00\x05\x00\n\x00\x0b\x01\n\x02\x12\x00\x02\x00\x03\x01\xc3 \x1aI\x94\x81q\xc3\xfe\xcb\xcb\xa0(,\x89\xb0\x02\x10\xc3 \x1aI\x94\x81q\xc3\xfe\xcb\xcb\xa0(,\x89\xb0\x00\x00\x10\x8d\xbe\x1c\x00\x00\x00\x80\x1a\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03LBR\x01T\x00\xc5\xe3\x8f^\x00\x00\x00\x00\x00 x\x154r\xe4\x80\xe0",\xe4\x9a\xc0H\xe9\xc9\x15\xbc\xfbNF\x9c\xb3\x88\x8di\xda0\xf6S\xa9\x11\xb9@\x8a;\xfc\x89\xc3\xfe\xf2\xbf#r\xf3\xa8\xd9m-\xf1\x03o\x94\x7f\x83\xbc\xc5cC\xa2\x0eE\x10/\xedCz{\xa3\\\x1b\xcf\xfa\xca\x11\xd3U\xd1\x0c\xa4\nG\xd7\xc9bx\xc7\xab7\xach*\xe8\x01i5\x9e\x01'
    stx = Transaction.deserialize(blob)
    assert stx.serialize() == blob


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
    assert script.code == Script.get_script_bytecode("peer_to_peer")
    assert script.args[0].index == 1
    assert script.args[0].Address == True
    assert script.args[0].enum_name == 'Address'
    #script.args[1] is changed to auth_key_prefix, the design is odd.
    assert script.args[2].index == 0
    assert script.args[2].U64 == True
    assert script.args[2].value == 123


def test_raw_txn_with_metadata():
    a0 = libra.Account(b'0' * ED25519_PRIVATE_KEY_LENGTH)
    a1 = libra.Account(b'1' * ED25519_PRIVATE_KEY_LENGTH)
    raw_tx = RawTransaction._gen_transfer_transaction(a0.address, 0, a1.address, 9, metadata=bytes([2,3,4]))
    assert raw_tx.payload.value_type == Script
    script = raw_tx.payload.value
    assert script.code == Script.get_script_bytecode("peer_to_peer_with_metadata")
    assert script.args[0].index == 1
    assert script.args[0].Address == True
    assert script.args[0].enum_name == 'Address'
    assert script.args[2].index == 0
    assert script.args[2].U64 == True
    assert script.args[2].value == 9
    assert script.args[3].index == 2
    assert script.args[3].U8Vector == True
    assert script.args[3].value == bytes([2,3,4])


def test_signed_txn():
    a0 = libra.Account(b'0' * ED25519_PRIVATE_KEY_LENGTH)
    a1 = libra.Account(b'1' * ED25519_PRIVATE_KEY_LENGTH)
    raw_tx = RawTransaction._gen_transfer_transaction(a0.address, 0, a1.address, 123)
    stx = SignedTransaction.gen_from_raw_txn(raw_tx, a0)
    assert len(stx.authenticator.value.signature) == ED25519_SIGNATURE_LENGTH
    stx.check_signature()
    sctx = raw_tx.sign(a0.private_key, a0.public_key)
    assert sctx.v0 == stx
    assert len(raw_tx.serialize()) == stx.raw_txn_bytes_len()
    with pytest.raises(nacl.exceptions.BadSignatureError):
        authenticator = TransactionAuthenticator.ed25519(a0.public_key, b'\0'*ED25519_SIGNATURE_LENGTH)
        stx.authenticator = authenticator
        stx.check_signature()
    tx = Transaction('UserTransaction', stx)
    assert tx.to_proto().transaction == tx.serialize()
    jstr = tx.to_json()
    print(jstr)

