import collections
import more_itertools
from libra.ledger_info import LedgerInfo
from libra.transaction import Version, TransactionInfo
from libra.proof.anyhow import ensure, bail


# Verifies that a given `transaction_info` exists in the ledger using provided proof.
def verify_transaction_info(
    ledger_info: LedgerInfo,
    transaction_version: Version,
    transaction_info: TransactionInfo,
    ledger_info_to_transaction_info_proof#: TransactionAccumulatorProof
):
    ensure(
        transaction_version <= ledger_info.version,
        "Transaction version {} is newer than LedgerInfo version {}.",
        transaction_version,
        ledger_info.version,
    )
    transaction_info_hash = transaction_info.hash()
    ledger_info_to_transaction_info_proof.verify(
        ledger_info.transaction_accumulator_hash,
        transaction_info_hash,
        transaction_version
    )

