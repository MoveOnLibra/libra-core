from libra.proof.definition import TransactionProof
from libra.proof.accumulator import InMemoryAccumulator
from libra.rustlib import ensure
from libra.transaction import Transaction, Version
from libra.contract_event import ContractEvent
from libra.ledger_info import LedgerInfo
from libra.account_address import Address
from libra.hasher import EventAccumulatorHasher
from canoser import Uint64
from dataclasses import dataclass
from typing import List, Optional
from libra.proto_helper import ProtoHelper


class EventAccumulatorHasherInMemoryAccumulator(InMemoryAccumulator):
    hasher = EventAccumulatorHasher


@dataclass
class TransactionWithProof:
    version: Version
    transaction: Transaction
    events: Optional[List[ContractEvent]]
    proof: TransactionProof

    def to_proto(self):
        proto = ProtoHelper.new_proto_obj(self)
        proto.version = self.version
        proto.transaction.MergeFrom(ProtoHelper.to_proto(self.transaction))
        if self.events:
            events_list_proto = ProtoHelper.new_proto_by_name("EventsList")
            for event in self.events:
                events_list_proto.events.append(ProtoHelper.to_proto(event))
            proto.events.MergeFrom(events_list_proto)
        proto.proof.MergeFrom(ProtoHelper.to_proto(self.proof))
        return proto

    # Verifies the transaction with the proof, both carried by `self`.
    # A few things are ensured if no error is raised:
    #   1. This transaction exists in the ledger represented by `ledger_info`.
    #   2. This transaction is a `UserTransaction`.
    #   3. And this user transaction has the same `version`, `sender`, and `sequence_number` as
    #      indicated by the parameter list. If any of these parameter is unknown to the call site
    #      that is supposed to be informed via this struct, get it from the struct itself, such
    #      as version and sender.
    def verify_user_txn(
        self,
        ledger_info: LedgerInfo,
        version: Version,
        sender: Address,
        sequence_number: Uint64
    ):
        signed_transaction = self.transaction.value
        ensure(
            self.version == version,
            "Version ({}) is not expected ({}).",
            self.version,
            version,
        )
        ensure(
            bytes(signed_transaction.sender) == bytes(sender),
            "Sender ({}) not expected ({}).",
            signed_transaction.sender,
            sender,
        )
        ensure(
            signed_transaction.sequence_number == sequence_number,
            "Sequence number ({}) not expected ({}).",
            signed_transaction.sequence_number,
            sequence_number,
        )
        if self.events:
            event_hashes = [x.hash() for x in self.events]
            events_root_hash = EventAccumulatorHasherInMemoryAccumulator.from_leaves(event_hashes).root_hash
        else:
            events_root_hash = None
        self.proof.verify(
            ledger_info,
            self.transaction.hash(),
            events_root_hash,
            version
        )

    @classmethod
    def from_proto(cls, proto):
        version = proto.version
        transaction = Transaction.deserialize(proto.transaction.transaction)
        proof = TransactionProof.from_proto(proto.proof)
        events = [ContractEvent.from_proto(x) for x in proto.events.events]
        return cls(version, transaction, events, proof)
