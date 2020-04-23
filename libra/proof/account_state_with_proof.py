from libra.account_address import Address
from libra.account_state import AccountState
from libra.account_state_blob import AccountStateBlob
from libra.event import EventKey
from libra.transaction import Version
from libra.proof.definition import AccountStateProof
from libra.rustlib import ensure
from dataclasses import dataclass
from typing import Optional, Tuple
from canoser import Uint64


@dataclass
class AccountStateWithProof:
    # The transaction version at which this account state is seen.
    version: Version
    # Blob value representing the account state. If this field is not set, it
    # means the account does not exist.
    blob: Optional[AccountStateBlob]
    # The proof the client can use to authenticate the value.
    proof: AccountStateProof

    @classmethod
    def from_proto(cls, proto):
        proof = AccountStateProof.from_proto(proto.proof)
        if len(proto.blob.__str__()) > 0:
            blob = AccountStateBlob.from_proto(proto.blob)
        else:
            blob = None
        return cls(proto.version, blob, proof)

    def verify(
        self,
        ledger_info,
        version,
        address
    ):
        ensure(
            self.version == version,
            "State version ({}) is not expected ({}).",
            self.version,
            version
        )
        self.proof.verify(ledger_info, version, Address.hash(address), self.blob)

    # Returns the `EventKey` (if existent) and number of total events for
    # an event stream specified by a query path.
    #
    # If the resource referred by the path that is supposed to hold the `EventHandle`
    # doesn't exist, returns (None, 0). While if the path is invalid, raises error.
    #
    # For example:
    #   1. if asked for DiscoverySetChange event from an ordinary user account,
    # this returns (None, 0)
    #   2. but if asked for a random path that we don't understand, it's an error.
    def get_event_key_and_count_by_query_path(
        self,
        path: bytes,
    ) -> Tuple[Optional[EventKey], Uint64]:
        if self.blob is not None:
            state = AccountState.deserialize(self.blob.blob)
            try:
                event_handle = state.get_event_handle_by_query_path(path)
                if event_handle is not None:
                    return (event_handle.key, event_handle.count)
            except AttributeError:
                return (None, 0)
        else:
            return (None, 0)
