from __future__ import annotations
from canoser import Struct, Uint8, BytesT
from nacl.signing import VerifyKey
from libra.hasher import gen_hasher, HashValue
from libra.transaction.raw_transaction import RawTransaction
from libra.crypto.ed25519 import ED25519_PUBLIC_KEY_LENGTH, ED25519_SIGNATURE_LENGTH
from dataclasses import dataclass

class SignedTransaction(Struct):
    """A transaction that has been signed.
    A `SignedTransaction` is a single transaction that can be atomically executed. Clients submit
    these to validator nodes, and the validator and executor submits these to the VM.
    """
    _fields = [
        ('raw_txn', RawTransaction),
        ('public_key', BytesT(ED25519_PUBLIC_KEY_LENGTH)),
        ('signature', BytesT(ED25519_SIGNATURE_LENGTH))
#        ('transaction_length', Uint64)
    ]


    def to_json_serializable(self):
        amap = super().to_json_serializable()
        if hasattr(self, 'transaction_info'):
            amap["transaction_info"] = self.transaction_info.to_json_serializable()
        if hasattr(self, 'events'):
            amap["events"] = [x.to_json_serializable() for x in self.events]
        if hasattr(self, 'version'):
            amap["version"] = self.version
        if hasattr(self, 'success'):
            amap["success"] = self.success
        return amap

    @classmethod
    def gen_from_raw_txn(cls, raw_tx, sender_account):
        """Signs the given `RawTransaction`and return a `SignedTransaction`.
        For a transaction that has just been signed, its signature is expected to be valid.
        """
        tx_hash = raw_tx.hash()
        signature = sender_account.sign(tx_hash)[:64]
        return SignedTransaction(raw_tx,
                sender_account.public_key,
                signature
            )

    def hash(self):
        shazer = gen_hasher(b"SignedTransaction::libra_types::transaction")
        shazer.update(self.serialize())
        return shazer.digest()

    @classmethod
    def from_proto(cls, proto):
        return cls.deserialize(proto.txn_bytes)

    def check_signature(self) -> SignatureCheckedTransaction:
        message = self.raw_txn.hash()
        vkey = VerifyKey(self.public_key)
        vkey.verify(message, self.signature)
        return SignatureCheckedTransaction(self)

    @property
    def sender(self):
        return self.raw_txn.sender

    @property
    def sequence_number(self):
        return self.raw_txn.sequence_number

    @property
    def payload(self):
        return self.raw_txn.payload

    @property
    def max_gas_amount(self):
        return self.raw_txn.max_gas_amount

    @property
    def gas_unit_price(self):
        return self.raw_txn.gas_unit_price

    @property
    def expiration_time(self):
        return self.raw_txn.expiration_time

    def raw_txn_bytes_len(self):
        return len(self.raw_txn.serialize())

@dataclass
class SignatureCheckedTransaction:
    v0: SignedTransaction

    def into_inner(self) -> SignedTransaction:
        return self.v0

    def into_raw_transaction(self) -> RawTransaction:
        return self.v0.raw_txn
