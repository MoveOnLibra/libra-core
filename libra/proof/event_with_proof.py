from libra.proof.anyhow import ensure, bail
from libra.proof.definition import EventProof
from libra.contract_event import ContractEvent
from libra.hasher import EventAccumulatorHasher
from libra.ledger_info import LedgerInfo
from libra.event import EventKey
from libra.transaction import Version
from canoser import Uint64
from dataclasses import dataclass


@dataclass
class EventWithProof:
    transaction_version: Uint64 # Should be `Version`
    event_index: Uint64
    event: ContractEvent
    proof: EventProof

    # Verifies the event with the proof, both carried by `self`.
    #
    # Two things are ensured if no error is raised:
    #   1. This event exists in the ledger represented by `ledger_info`.
    #   2. And this event has the same `event_key`, `sequence_number`, `transaction_version`,
    # and `event_index` as indicated in the parameter list. If any of these parameter is unknown
    # to the call site and is supposed to be informed by this struct, get it from the struct
    # itself, such as: `event_with_proof.event.access_path()`, `event_with_proof.event_index()`,
    # etc.
    def verify(
        self,
        ledger_info: LedgerInfo,
        event_key: EventKey,
        sequence_number: Uint64,
        transaction_version: Version,
        event_index: Uint64,
    ):
        ensure(
            bytes(self.event.key) == bytes(event_key),
            "Event key ({}) not expected ({}).",
            self.event.key,
            event_key,
        )
        ensure(
            self.event.event_seq_num == sequence_number,
            "Sequence number ({}) not expected ({}).",
            self.event.event_seq_num,
            sequence_number,
        )
        ensure(
            self.transaction_version == transaction_version,
            "Transaction version ({}) not expected ({}).",
            self.transaction_version,
            transaction_version,
        )
        ensure(
            self.event_index == event_index,
            "Event index ({}) not expected ({}).",
            self.event_index,
            event_index,
        )

        self.proof.verify(
            ledger_info,
            self.event.hash(),
            transaction_version,
            event_index,
        )


    @classmethod
    def from_proto(cls, event_with_proof):
        ce = ContractEvent.from_proto(event_with_proof.event)
        proof = EventProof.from_proto(event_with_proof.proof)
        return cls(event_with_proof.transaction_version, event_with_proof.event_index, ce, proof)

