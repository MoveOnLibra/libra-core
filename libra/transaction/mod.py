from dataclasses import dataclass
from libra.vm_error import VMStatus, StatusCode, StatusType
from libra.transaction.write_set import WriteSet
from libra.transaction.transaction import Transaction
from libra.account_address import Address
from libra.account_state_blob import AccountStateBlob
from libra.contract_event import ContractEvent
from canoser import Uint64
from typing import List, Mapping
from enum import IntEnum


class TransactionStatusTag(IntEnum):
    Discard = 0  # Discard the transaction output
    Keep = 1
    Retry = 2

# The status of executing a transaction. The VM decides whether or not we should `Keep` the
# transaction output or `Discard` it based upon the execution of the transaction. We wrap these
# decisions around a `VMStatus` that provides more detail on the final execution state of the VM.
@dataclass
class TransactionStatus:
    tag: TransactionStatusTag
    vm_status: VMStatus

    Discard = TransactionStatusTag.Discard
    Keep = TransactionStatusTag.Keep
    Retry = TransactionStatusTag.Retry

    def vm_status(self) -> VMStatus:
        if self.tag == TransactionStatusTag.Retry:
            return VMStatus(StatusCode.UNKNOWN_VALIDATION_STATUS)
        else:
            return self.vm_status

    @classmethod
    def from_vm_status(cls, vm_status: VMStatus):
        mapping = {
            # Any unknown error should be discarded
            StatusType.Unknown: True,
            # Any error that is a validation status (i.e. an error arising from the prologue)
            # causes the transaction to not be included.
            StatusType.Validation: True,
            # If the VM encountered an invalid internal state, we should discard the transaction.
            StatusType.InvariantViolation: True,
            # A transaction that publishes code that cannot be verified will be charged.
            StatusType.Verification: False,
            # Even if we are unable to decode the transaction, there should be a charge made to
            # that user's account for the gas fees related to decoding, running the prologue etc.
            StatusType.Deserialization: False,
            # Any error encountered during the execution of the transaction will charge gas.
            StatusType.Execution: False,
        }

        should_discard = mapping[vm_status.status_type()]

        if should_discard:
            return TransactionStatus(TransactionStatus.Discard, vm_status)
        else:
            return TransactionStatus(TransactionStatus.Keep, vm_status)


# The output of executing a transaction.
@dataclass
class TransactionOutput:
    # The list of writes this transaction intends to do.
    write_set: WriteSet

    # The list of events emitted during this transaction.
    events: List[ContractEvent]

    # The amount of gas used during execution.
    gas_used: Uint64

    # The execution status.
    status: TransactionStatus


@dataclass
class TransactionToCommit:
    transaction: Transaction
    account_states: Mapping[Address, AccountStateBlob]
    events: List[ContractEvent]
    gas_used: Uint64
    major_status: StatusCode


# impl TryFrom<crate.proto.types.TransactionToCommit> for TransactionToCommit {
#     type Error = Error

#     def try_from(proto: crate.proto.types.TransactionToCommit) -> Self {
#         transaction = proto
#             .transaction
#             .ok_or_else(|| format_err!("Missing signed_transaction"))
#             .try_into()
#         num_account_states = proto.account_states.__len__()
#         account_states = proto
#             .account_states
#             .into_iter()
#             .map(|x| {
#                 (
#                     AccountAddress.try_from(x.address?,
#                     AccountStateBlob.from(x.blob),
#                 ))
#             })
#             .collect.<Mapping[_, _]>()
#         ensure(
#             account_states.__len__() == num_account_states,
#             "account_states should have no duplication."
#         )
#         events = proto
#             .events
#             .into_iter()
#             .map(ContractEvent.try_from)
#             .collect.<List[_]>()
#         gas_used = proto.gas_used
#         major_status =
#             StatusCode.try_from(proto.major_status).unwrap_or(StatusCode.UNKNOWN_STATUS)

#         TransactionToCommit {
#             transaction,
#             account_states,
#             events,
#             gas_used,
#             major_status,
#         }
#     }
# }

# impl From<TransactionToCommit> for crate.proto.types.TransactionToCommit {
#     def from(txn: TransactionToCommit) -> Self {
#         Self {
#             transaction: Some(txn.transaction.into()),
#             account_states: txn
#                 .account_states
#                 .into_iter()
#                 .map(|(address, blob)| crate.proto.types.AccountState {
#                     address: address,
#                     blob: blob.into(),
#                 })
#                 .collect(),
#             events: txn.events.into_iter().map(Into.into).collect(),
#             gas_used: txn.gas_used,
#             major_status: txn.major_status.into(),
#         }
#     }
# }
