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



# Verifies an element whose hash is `element_hash` and version is `element_version` exists in the
# accumulator whose root hash is `expected_root_hash` using the provided proof.
def verify_accumulator_element(
        hash_func,
        expected_root_hash,
        element_hash,
        element_index,
        accumulator_proof):
    siblings = AccumulatorProof.from_proto(accumulator_proof).siblings
    assert len(siblings) <= MAX_ACCUMULATOR_PROOF_DEPTH
    index = element_index
    hashv = element_hash
    for sibling_hash in reversed(siblings):
        hasher = hash_func()
        if index % 2 == 0:
            hashv = MerkleTreeInternalNode(hashv, sibling_hash, hasher).hash()
        else:
            hashv = MerkleTreeInternalNode(sibling_hash, hashv, hasher).hash()
        index //= 2
    assert hashv == bytes(expected_root_hash)



def verify_transaction_list(txn_list_with_proof, ledger_info):
    #TODO:change repeated SignedTransaction transactions = 1; to repeated Transaction transactions = 1;
    #TODO: all transactions should be same epoch
    transactions = txn_list_with_proof.transactions
    infos = txn_list_with_proof.infos
    len_tx = len(transactions)
    len_info = len(infos)
    if len_tx != len_info:
        raise VerifyError(f"transactions and infos mismatch:{len_tx}, {len_info}.")
    if txn_list_with_proof.HasField("events_for_versions"):
        event_lists = txn_list_with_proof.events_for_versions.events_for_version
        verify_event_root_hash(event_lists, infos)
    check_txn_list_sig_with_infos(txn_list_with_proof)
    #Get the hashes of all nodes at the accumulator leaf level.
    hashes = [TransactionInfo.from_proto(x).hash() for x in infos]
    hashes = collections.deque(hashes)
    firstp = AccumulatorProof.from_proto(txn_list_with_proof.proof_of_first_transaction)
    first = firstp.siblings
    if txn_list_with_proof.HasField("proof_of_last_transaction"):
        lastp = AccumulatorProof.from_proto(txn_list_with_proof.proof_of_last_transaction)
        last = lastp.siblings
    else:
        last = first
    first_idx = txn_list_with_proof.first_transaction_version.value
    zipped = zip(first, last)
    ite = reversed(list(zipped))
    for first_sibling, last_sibling in ite:
        num_nodes = len(hashes)
        if num_nodes > 1:
            last_idx = first_idx + num_nodes - 1
            if last_idx % 2 == 0:
                hashes.append(last_sibling)
            else:
                assert hashes[num_nodes - 2] == last_sibling
            if first_idx % 2 == 0:
                assert hashes[1] == first_sibling
            else:
                hashes.appendleft(first_sibling)
        else:
            assert first_sibling == last_sibling
            if first_idx % 2 == 0:
                hashes.append(first_sibling)
            else:
                hashes.appendleft(first_sibling)
        parent_hashes = collections.deque()
        for pair in more_itertools.chunked(hashes, 2):
            assert len(pair) == 2
            hasher = TransactionAccumulatorHasher()
            hash_value = MerkleTreeInternalNode(pair[0], pair[1], hasher).hash()
            parent_hashes.append(hash_value)
        hashes = parent_hashes
        first_idx //= 2
    assert len(hashes) == 1
    assert hashes[0] == bytes(ledger_info.transaction_accumulator_hash)




def check_txn_list_sig_with_infos(txn_list_with_proof):
    zipped = zip(txn_list_with_proof.transactions, txn_list_with_proof.infos)
    for tx, info in zipped:
        stx = SignedTransaction.from_proto(tx)
        if stx.hash() != info.transaction_hash:
            raise VerifyError(f"transaction hash mismatch:{stx}.")

#Verify event root hashes match what is carried on the transaction infos.
def verify_event_root_hash(event_lists, infos):
    len_event = len(event_lists)
    len_info = len(infos)
    if len_info != len_event:
        raise VerifyError(f"transactions and events mismatch:{len_info}, {len_event}.")
    zipped = zip(event_lists, infos)
    for events, info in zipped:
        eroot_hash = get_event_root_hash(events.events)
        if bytes(eroot_hash) != info.event_root_hash:
            raise VerifyError(f"event_root_hash mismatch.")

