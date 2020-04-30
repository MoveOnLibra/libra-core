from canoser import RustEnum
from typing import List
from libra.ledger_info import LedgerInfoWithSignatures
from libra.waypoint import Waypoint
from libra.epoch_info import EpochInfo
from libra.validator_verifier import VerifyError
from dataclasses import dataclass


class VerifierType(RustEnum):
    """
    # The verification of the validator change proof starts with some verifier that is trusted by the
    # client: could be either a waypoint (upon startup) or a known validator verifier.
    """
    _enums = [
        ('Waypoint', Waypoint),
        ('TrustedVerifier', EpochInfo)
    ]

    def verify(self, ledger_info_with_sigs):
        if self.enum_name == 'Waypoint':
            self.value.verify(ledger_info_with_sigs.ledger_info)
        else:
            if self.value.epoch != ledger_info_with_sigs.ledger_info.epoch:
                raise VerifyError("LedgerInfo has unexpected epoch: {} - {}".format(
                    self.value.epoch,
                    ledger_info_with_sigs.ledger_info.epoch
                ))
            ledger_info_with_sigs.verify_signatures(self.value.verifier)

    #  Returns true in case the given epoch is larger than the existing verifier can support.
    #  In this case the EpochChangeProof should be verified and the verifier updated.
    def epoch_change_verification_required(self, epoch):
        if self.enum_name == 'Waypoint':
            return True
        else:
            return self.value.epoch < epoch


# A vector of LedgerInfo with contiguous increasing epoch numbers to prove a sequence of
# validator changes from the first LedgerInfo's epoch.
@dataclass
class EpochChangeProof:
    ledger_info_with_sigs: List[LedgerInfoWithSignatures]  # better name is ledger_info_with_sigss
    more: bool

    #  Verify the proof is correctly chained with known epoch and validator verifier
    #  and return the LedgerInfo to start target epoch
    #  In case waypoint is present it's going to be used for verifying the very first epoch change
    #  (it's the responsibility of the caller to not pass waypoint in case it's not needed).
    def verify(self, verifier: VerifierType) -> LedgerInfoWithSignatures:
        if not self.ledger_info_with_sigs:
            raise VerifyError("Empty EpochChangeProof")
        for x in self.ledger_info_with_sigs:
            # TODO: skip stale ledger, is_ledger_info_stale
            verifier.verify(x)
            # While the original verification could've been via waypoints, all the next epoch
            # changes are verified using the (already trusted) validator sets.
            ledger_info = x.ledger_info
            if not ledger_info.has_next_epoch_info():
                raise VerifyError("LedgerInfo doesn't carry ValidatorSet")
            epoch_info = ledger_info.next_epoch_info.value
            verifier = VerifierType('TrustedVerifier', epoch_info)
        return self.ledger_info_with_sigs[-1]

    @classmethod
    def from_proto(cls, proto):
        sigss = [LedgerInfoWithSignatures.from_proto(x) for x in proto.ledger_info_with_sigs]
        return cls(sigss, proto.more)
