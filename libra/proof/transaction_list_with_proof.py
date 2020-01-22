from libra.proof.definition import TransactionListProof
from libra.proof.accumulator import InMemoryAccumulator
from libra.hasher import EventAccumulatorHasher
from libra.proof.anyhow import ensure, bail
from libra.transaction import Transaction, Version
from libra.contract_event import ContractEvent
from libra.ledger_info import LedgerInfo
from canoser import Uint64
from dataclasses import dataclass, field
from typing import List, Optional


class EventAccumulatorHasherInMemoryAccumulator(InMemoryAccumulator):
    hasher = EventAccumulatorHasher

# The list may have three states:
# 1. The list is empty. Both proofs must be `None`.
# 2. The list has only 1 transaction/transaction_info. Then `proof_of_first_transaction`
# must exist and `proof_of_last_transaction` must be `None`.
# 3. The list has 2+ transactions/transaction_infos. The both proofs must exist.
@dataclass
class TransactionListWithProof:
    transactions: List[Transaction]
    events: Optional[List[List[ContractEvent]]]
    first_transaction_version: Optional[Version]
    proof: TransactionListProof


    # Creates an empty transaction list.
    @classmethod
    def new_empty(cls):
        return cls([], None, None, TransactionListProof.new_empty())
    
    # Verifies the transaction list with the proofs, both carried on `self`.
    #
    # Two things are ensured if no error is raised:
    #   1. All the transactions exist on the ledger represented by `ledger_info`.
    #   2. And the transactions in the list has consecutive versions starting from
    # `first_transaction_version`. When `first_transaction_version` is None, ensures the list is
    # empty.
    def verify(
        self,
        ledger_info: LedgerInfo,
        first_transaction_version: Optional[Version]
    ):
        ensure(
            self.first_transaction_version == first_transaction_version,
            "First transaction version ({}) not expected ({}).",
            self.first_transaction_version,
            first_transaction_version,
        )

        txn_hashes = [x.hash() for x in self.transactions]
        self.proof.verify(ledger_info, self.first_transaction_version, txn_hashes)

        # Verify the events if they exist.
        event_lists = self.events
        if event_lists:
            ensure(
                len(event_lists) == len(self.transactions),
                "The length of event_lists ({}) does not match the number of transactions ({}).",
                len(event_lists),
                len(self.transactions),
            )
            zipped = zip(event_lists, self.proof.transaction_infos)
            for events, txn_info in zipped:
                event_hashes = [x.hash() for x in events]
                event_root_hash = EventAccumulatorHasherInMemoryAccumulator.from_leaves(event_hashes).root_hash
                ensure(
                    bytes(event_root_hash) == bytes(txn_info.event_root_hash),
                    "Some event root hash calculated doesn't match that carried on the \
                     transaction info.",
                )


    def is_empty(self) -> bool:
        return len(self.transactions) == 0

    def len(self):
        return len(self.transactions)

    @classmethod
    def from_proto(cls, proto):
        transactions = [Transaction.deserialize(x.transaction) for x in proto.transactions]
        if proto.HasField("events_for_versions"):
            event_lists = proto.events_for_versions.events_for_version
            events = [[ContractEvent.from_proto(y) for y in x.events] for x in event_lists]
        else:
            events = None
        if len(proto.first_transaction_version.__str__()) > 0:
            first_transaction_version = proto.first_transaction_version.value
        else:
            if len(transactions) > 0:
                #Maybe bug of protobuf of py
                first_transaction_version = 0
            else:
                first_transaction_version = None
        proof = TransactionListProof.from_proto(proto.proof)
        return cls(transactions, events, first_transaction_version, proof)
