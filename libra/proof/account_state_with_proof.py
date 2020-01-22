from libra.account_address import Address
from libra.account_state_blob import AccountStateBlob
from libra.transaction import Version
from libra.proof.definition import AccountStateProof
from libra.proof.anyhow import ensure, bail
from dataclasses import dataclass, field
from typing import List, Optional

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
