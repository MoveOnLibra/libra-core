import libra
from libra import Address
from libra.crypto.ed25519 import ED25519_PRIVATE_KEY_LENGTH, ED25519_SIGNATURE_LENGTH
from libra.transaction import *
from canoser import Uint64
import pytest
import nacl
import pdb

# def test_deserialize_multi_ed25519():
#     data = '004fa2be7ad55936c5702e8b7e3fdedb05000000000000000002ef01a11ceb0b010007014600000004000000034a0000001700000004610000000400000005650000001400000007790000004800000008c10000001000000009d10000001e0000000000000101020001010101030203000104040101010005050101010006020602050a02000105010102050303050a0203010900063c53454c463e0c4c696272614163636f756e74176372656174655f756e686f737465645f6163636f756e74066578697374730f7061795f66726f6d5f73656e646572046d61696e00000000000000000000000000000000030000050c000a001101200305000508000a000a013d000a000a023d0102010600000000000000000000000000000000034c42520154000301b3f7e8e38f8c8393f281a2f0792a28490210c0c19d6b1d48371ea28f0cdc5f74bba70040420f000000000080a903000000000000000000000000005a4aa35e00000000014185c582f99e99edca5417802e108f4cd47c362d352992d616ef30608ee36759553f277edec12f11e182cec2f8eecd7411ba636e9d6e4c8e66ff07e289e9cd3dae02840112b2da9c9c73f48e0b3079de3c0acd2644173efe31a3a9761dfeeaef9c75fb39b9fe7d624c6407d8ba53b7ea7c4ed39cf4cfe1bf06da78c72d75faf4df41260c4f2527d546b02cb357199d6cd4c78f8e840e7c52ae33bc2aa72024b92c712378c2610ab0710b35fd60b134d921dad7d6de2db0c5ced477d18a5b2eb2086edc0fc0000000'
#     data = bytes.fromhex(data)
#     auth = data[361:]
#     arr = [1, 1, 32, 32, 1, 2, 64, 64, 4]
#     cur = 361
#     for x in arr:
#         print(data[cur:cur+x])
#         cur += x
#     tauth = TransactionAuthenticator.deserialize(auth)
#     assert tauth.serialize() == auth
#     tx = Transaction.deserialize(data)



def test_raw_txn():
    a0 = libra.Account(b'0' * ED25519_PRIVATE_KEY_LENGTH)
    a1 = libra.Account(b'1' * ED25519_PRIVATE_KEY_LENGTH)
    assert RawTransaction.__doc__.startswith("RawTransaction is the portion of a transaction that a client signs")
    raw_tx = RawTransaction._gen_transfer_transaction(a0.address, 0, a1.address, 123)
    assert raw_tx.max_gas_amount == 1_000_000
    assert raw_tx.gas_unit_price == 0
    assert raw_tx.gas_currency_code == "LBR"
    assert bytes(raw_tx.sender) == a0.address
    assert raw_tx.payload.enum_name == "Script"
    assert raw_tx.payload.index == 1
    assert raw_tx.payload.value_type == Script
    script = raw_tx.payload.value
    assert script.code == Script.get_script_bytecode("peer_to_peer_with_metadata")
    assert script.args[0].index == 3
    assert script.args[0].Address == True
    assert script.args[0].enum_name == 'Address'
    #script.args[1] is changed to auth_key_prefix, the design is odd.
    assert script.args[2].index == 1
    assert script.args[2].U64 == True
    assert script.args[2].value == 123


def test_raw_txn_with_metadata():
    a0 = libra.Account(b'0' * ED25519_PRIVATE_KEY_LENGTH)
    a1 = libra.Account(b'1' * ED25519_PRIVATE_KEY_LENGTH)
    raw_tx = RawTransaction._gen_transfer_transaction(a0.address, 0, a1.address, 9, metadata=bytes([2,3,4]))
    assert raw_tx.payload.value_type == Script
    script = raw_tx.payload.value
    assert script.code == Script.get_script_bytecode("peer_to_peer_with_metadata")
    assert script.args[0].index == 3
    assert script.args[0].Address == True
    assert script.args[0].enum_name == 'Address'
    assert script.args[2].index == 1
    assert script.args[2].U64 == True
    assert script.args[2].value == 9
    assert script.args[3].index == 4
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
    jstr = tx.to_json()
    print(jstr)

