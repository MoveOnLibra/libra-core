from libra.hasher import (
    HashValue, ACCUMULATOR_PLACEHOLDER_HASH,SPARSE_MERKLE_PLACEHOLDER_HASH,
    TransactionAccumulatorHasher, EventAccumulatorHasher, TestOnlyHasher,
    bytes_to_bits, common_prefix_bits_len)
from libra.proof.merkle_tree import MerkleTreeInternalNode, SparseMerkleLeafNode, SparseMerkleInternalNode
from libra.validator_verifier import VerifyError
from libra.proof.anyhow import ensure, bail
from libra.proof.mod import verify_transaction_info
from libra.account_state_blob import AccountStateBlob
from libra.transaction import TransactionInfo, Version
from libra.ledger_info import LedgerInfo
from canoser import Uint64, Uint8
from dataclasses import dataclass, field
from typing import List, Optional, Callable, Tuple
import more_itertools

# Converts sibling nodes from Protobuf format to Rust format, using the fact that empty byte
# arrays represent placeholder hashes.
def from_proto_siblings(siblings: List[List[Uint8]], placeholder: HashValue) -> List[HashValue]:
    ensure(
        placeholder == ACCUMULATOR_PLACEHOLDER_HASH or placeholder == SPARSE_MERKLE_PLACEHOLDER_HASH,
        "Placeholder can only be ACCUMULATOR_PLACEHOLDER_HASH or SPARSE_MERKLE_PLACEHOLDER_HASH.",
    )
    def hash_bytes_transform(hash_bytes):
        if not hash_bytes:
            return placeholder
        else:
            return hash_bytes
    return [hash_bytes_transform(x) for x in siblings]

# Converts sibling nodes from Rust format to Protobuf format. The placeholder hashes are
# converted to empty byte arrays.
def into_proto_siblings(siblings: List[HashValue], placeholder: HashValue) -> List[List[Uint8]]:
    ensure(
        placeholder == ACCUMULATOR_PLACEHOLDER_HASH or placeholder == SPARSE_MERKLE_PLACEHOLDER_HASH,
        "Placeholder can only be ACCUMULATOR_PLACEHOLDER_HASH or SPARSE_MERKLE_PLACEHOLDER_HASH.",
    )
    def hash_bytes_transform(sibling):
        if sibling != placeholder:
            return sibling
        else:
            return []
    return [hash_bytes_transform(x) for x in siblings]


# Because leaves can only take half the space in the tree, any numbering of the tree leaves must
# not take the full width of the total space.  Thus, for a 64-bit ordering, our maximumm proof
# depth is limited to 63.

LeafCount = Uint64
MAX_ACCUMULATOR_PROOF_DEPTH = 63
MAX_ACCUMULATOR_LEAVES = 1 << MAX_ACCUMULATOR_PROOF_DEPTH



# A proof that can be used authenticate an element in an accumulator given trusted root hash. For
# example, both `LedgerInfoToTransactionInfoProof` and `TransactionInfoToEventProof` can be
# constructed on top of this structure.
@dataclass
class AccumulatorProof:
    # All siblings in this proof, including the default ones. Siblings are ordered from the bottom
    # level to the root level.
    siblings: List[HashValue]
    #hasher: Callable[[], object] = field(init=False)


    # Verifies an element whose hash is `element_hash` and version is `element_version` exists in
    # the accumulator whose root hash is `expected_root_hash` using the provided proof.
    def verify(
        self,
        expected_root_hash: HashValue,
        element_hash: HashValue,
        element_index: Uint64,
    ):
        ensure(
            len(self.siblings) <= MAX_ACCUMULATOR_PROOF_DEPTH,
            "Accumulator proof has more than {} ({}) siblings.",
            MAX_ACCUMULATOR_PROOF_DEPTH,
            len(self.siblings)
        )
        index = element_index
        hashv = element_hash
        for sibling_hash in self.siblings:
            if index % 2 == 0:
                # the current node is a left child.
                hashv = MerkleTreeInternalNode(hashv, sibling_hash, self.__class__.hasher).hash()
            else:
                # the current node is a right child.
                hashv = MerkleTreeInternalNode(sibling_hash, hashv, self.__class__.hasher).hash()
            index //= 2
        ensure(
            hashv == bytes(expected_root_hash),
            "Root hashes do not match. Actual root hash: {}. Expected root hash: {}.",
            hashv,
            expected_root_hash
        )


    @classmethod
    def from_proto(cls, proto):
        siblings = from_proto_siblings(proto.siblings, ACCUMULATOR_PLACEHOLDER_HASH)
        return cls(siblings)

@dataclass
class TransactionAccumulatorProof(AccumulatorProof):
    hasher = TransactionAccumulatorHasher

@dataclass
class EventAccumulatorProof(AccumulatorProof):
    hasher = EventAccumulatorHasher

@dataclass
class TestAccumulatorProof(AccumulatorProof):
    hasher = TestOnlyHasher



# A proof that can be used to authenticate an element in a Sparse Merkle Tree given trusted root
# hash. For example, `TransactionInfoToAccountProof` can be constructed on top of this structure.
@dataclass
class SparseMerkleProof:
    # This proof can be used to authenticate whether a given leaf exists in the tree or not.
    #     - If this is `Some(HashValue, HashValue)`
    #         - If the first `HashValue` equals requested key, this is an inclusion proof and the
    #           second `HashValue` equals the hash of the corresponding account blob.
    #         - Otherwise this is a non-inclusion proof. The first `HashValue` is the only key
    #           that exists in the subtree and the second `HashValue` equals the hash of the
    #           corresponding account blob.
    #     - If this is `None`, this is also a non-inclusion proof which indicates the subtree is
    #       empty.
    leaf: Optional[Tuple[HashValue, HashValue]]

    # All siblings in this proof, including the default ones. Siblings are ordered from the bottom
    # level to the root level.
    siblings: List[HashValue]


    @classmethod
    def from_proto(cls, proto_proof):
        proto_leaf = proto_proof.leaf
        if proto_leaf:
            if len(proto_leaf) == HashValue.LENGTH * 2:
                key = proto_leaf[0:HashValue.LENGTH]
                value_hash = proto_leaf[HashValue.LENGTH:HashValue.LENGTH*2]
                leaf = (key, value_hash)
            else:
                bail(
                    "Mailformed proof. Leaf has {} bytes. Expect 0 or {} bytes.",
                    len(proto_leaf),
                    HashValue.LENGTH * 2
                )
        else:
            leaf = None
        siblings = from_proto_siblings(proto_proof.siblings, SPARSE_MERKLE_PLACEHOLDER_HASH)
        return cls(leaf, siblings)


    # If `element_blob` is present, verifies an element whose key is `element_key` and value is
    # `element_blob` exists in the Sparse Merkle Tree using the provided proof. Otherwise
    # verifies the proof is a valid non-inclusion proof that shows this key doesn't exist in the
    # tree.
    def verify(
        self,
        expected_root_hash: HashValue,
        element_key: HashValue,
        element_blob: Optional[AccountStateBlob]
    ):
        ensure(
            len(self.siblings) <= HashValue.LENGTH_IN_BITS,
            "Sparse Merkle Tree proof has more than {} ({}) siblings.",
            HashValue.LENGTH_IN_BITS,
            len(self.siblings),
        )
        if self.leaf is not None:
            if element_blob is not None:
                proof_key, proof_value_hash = self.leaf
                # This is an inclusion proof, so the key and value hash provided in the proof should
                # match element_key and element_value_hash.
                # `siblings` should prove the route from the leaf node to the root.
                ensure(
                    element_key == proof_key,
                    "Keys do not match. Key in proof: {}. Expected key: {}.",
                    proof_key,
                    element_key
                )
                hashv = element_blob.hash()
                ensure(
                    hashv == proof_value_hash,
                    "Value hashes do not match. Value hash in proof: {}. Expected value hash: {}",
                    proof_value_hash,
                    hashv
                )
            else:
                proof_key, _proof_value_hash = self.leaf
                # This is a non-inclusion proof.
                # The proof intends to show that if a leaf node representing `element_key` is inserted,
                # it will break a currently existing leaf node represented by `proof_key` into a
                # branch.
                # `siblings` should prove the route from that leaf node to the root.
                ensure(
                    element_key != proof_key,
                    "Expected non-inclusion proof, but key exists in proof."
                )
                ensure(
                    common_prefix_bits_len(element_key, proof_key) >= len(self.siblings),
                    "Key would not have ended up in the subtree where the provided key in proof is \
                     the only existing key, if it existed. So this is not a valid non-inclusion proof."
                )
        else:
            if element_blob is not None:
                raise VerifyError("Expected inclusion proof. Found non-inclusion proof.")
            else:
                # This is a non-inclusion proof. The proof intends to show that if a leaf node
                # representing `element_key` is inserted, it will show up at a currently empty
                # position. `sibling` should prove the route from this empty position to the root.
                pass
        if self.leaf is not None:
            key, value_hash = self.leaf
            current_hash = SparseMerkleLeafNode(key, value_hash).hash()
        else:
            current_hash = bytes(SPARSE_MERKLE_PLACEHOLDER_HASH)
        iter_bits = bytes_to_bits(element_key)[0:len(self.siblings)]
        zipped = zip(self.siblings, reversed(iter_bits))
        for sibling_hash, bit in zipped:
            if bit == '1':
                current_hash = SparseMerkleInternalNode(sibling_hash, current_hash).hash()
            else:
                current_hash = SparseMerkleInternalNode(current_hash, sibling_hash).hash()
        ensure(
            current_hash == bytes(expected_root_hash),
            "Root hashes do not match. Actual root hash: {}. Expected root hash: {}.",
            current_hash,
            bytes(expected_root_hash)
        )



# A proof that can be used to show that two Merkle accumulators are consistent -- the big one can
# be obtained by appending certain leaves to the small one. For example, at some point in time a
# client knows that the root hash of the ledger at version 10 is `old_root` (it could be a
# waypoint). If a server wants to prove that the new ledger at version `N` is derived from the
# old ledger the client knows, it can show the subtrees that represent all the new leaves. If
# the client can verify that it can indeed obtain the new root hash by appending these new
# leaves, it can be convinced that the two accumulators are consistent.

# See [`crate::proof::accumulator::Accumulator::append_subtrees`] for more details.
@dataclass
class AccumulatorConsistencyProof:
    # The subtrees representing the newly appended leaves.
    subtrees: List[HashValue]

    @classmethod
    def from_proto(cls, proto):
        return cls(proto.subtrees)


# A proof that is similar to `AccumulatorProof`, but can be used to authenticate a range of
# leaves. For example, given the following accumulator:
#
# ```text
#                 root
#                /     \
#              /         \
#            /             \
#           o               o
#         /   \           /   \
#        /     \         /     \
#       X       o       o       Y
#      / \     / \     / \     / \
#     o   o   a   b   c   Z   o   o
# ```
#
# if the proof wants to show that `[a, b, c]` exists in the accumulator, it would need `X` on the
# left and `Y` and `Z` on the right.
@dataclass
class AccumulatorRangeProof:
    # The siblings on the left of the path from the first leaf to the root. Siblings near the root
    # are at the beginning of the vector.
    left_siblings: List[HashValue]
    # The sliblings on the right of the path from the last leaf to the root. Siblings near the root
    # are at the beginning of the vector.
    right_siblings: List[HashValue]
    #hasher: Callable[[], object] = field(init=False)

    @classmethod
    def new_empty(cls):
        return cls([], [])


    # Verifies the proof is correct. The verifier needs to have `expected_root_hash`, the index
    # of the first leaf and all of the leaves in possession.
    def verify(
        self,
        expected_root_hash: HashValue,
        first_leaf_index: Uint64,
        leaf_hashes: List[HashValue],
    ):
        if first_leaf_index is None:
            ensure(
                not leaf_hashes,
                "first_leaf_index indicated empty list while leaf_hashes is not empty.",
            )
            ensure(
                not self.left_siblings and not self.right_siblings,
                "No siblings are needed.",
            )
            return

        ensure(
            len(self.left_siblings) <= MAX_ACCUMULATOR_PROOF_DEPTH,
            "Proof has more than {} ({}) left siblings.",
            MAX_ACCUMULATOR_PROOF_DEPTH,
            len(self.left_siblings)
        )
        ensure(
            len(self.right_siblings) <= MAX_ACCUMULATOR_PROOF_DEPTH,
            "Proof has more than {} ({}) right siblings.",
            MAX_ACCUMULATOR_PROOF_DEPTH,
            len(self.right_siblings)
        )
        ensure(
            len(leaf_hashes) > 0,
            "leaf_hashes is empty while first_leaf_index indicated non-empty list.",
        )

        left_sibling_iter = 0
        right_sibling_iter = 0

        from libra.proof.position import Position
        first_pos = Position.from_leaf_index(first_leaf_index)
        current_hashes = leaf_hashes.copy()
        parent_hashes = []

        # Keep reducing the list of hashes by combining all the children pairs, until there is
        # only one hash left.
        while len(current_hashes) > 1 \
            or len(self.left_siblings) > left_sibling_iter \
            or len(self.right_siblings) > right_sibling_iter:
            children_iter = current_hashes.__iter__()

            # If the first position on the current level is a right child, it needs to be combined
            # with a sibling on the left.
            if first_pos.is_right_child():
                left_hash = self.left_siblings[left_sibling_iter]
                left_sibling_iter += 1
                right_hash = children_iter.__next__()
                hashv = MerkleTreeInternalNode(left_hash, right_hash, self.__class__.hasher).hash()
                parent_hashes.append(hashv)


            # Next we take two children at a time and compute their parents.
            for chunk in more_itertools.chunked(children_iter, 2):
                if len(chunk) == 2:
                    left_hash = chunk[0]
                    right_hash = chunk[1]
                    hashv = MerkleTreeInternalNode(left_hash, right_hash, self.__class__.hasher).hash()
                    parent_hashes.append(hashv)
                else:
                    # Similarly, if the last position is a left child, it needs to be combined with a
                    # sibling on the right.
                    left_hash = chunk[0]
                    right_hash = self.right_siblings[right_sibling_iter]
                    right_sibling_iter += 1
                    hashv = MerkleTreeInternalNode(left_hash, right_hash, self.__class__.hasher).hash()
                    parent_hashes.append(hashv)

            first_pos = first_pos.parent()
            current_hashes = parent_hashes
            parent_hashes = []

        ensure(
            current_hashes[0] == bytes(expected_root_hash),
            "Root hashes do not match. Actual root hash: {}. Expected root hash: {}.",
            current_hashes[0],
            expected_root_hash
        )

    @classmethod
    def from_proto(cls, proto):
        left_siblings = from_proto_siblings(proto.left_siblings, ACCUMULATOR_PLACEHOLDER_HASH)
        right_siblings = from_proto_siblings(proto.right_siblings, ACCUMULATOR_PLACEHOLDER_HASH)
        return cls(left_siblings, right_siblings)


class TransactionAccumulatorRangeProof(AccumulatorRangeProof):
    hasher = TransactionAccumulatorHasher

class TestAccumulatorRangeProof(AccumulatorRangeProof):
    hasher = TestOnlyHasher


# A proof that can be used authenticate a range of consecutive leaves, from the leftmost leaf to
# a certain one, in a sparse Merkle tree. For example, given the following sparse Merkle tree:
#
# ```text
#                   root
#                  /     \
#                 /       \
#                /         \
#               o           o
#              / \         / \
#             a   o       o   h
#                / \     / \
#               o   d   e   X
#              / \         / \
#             b   c       f   g
# ```
#
# if the proof wants show that `[a, b, c, d, e]` exists in the tree, it would need the siblings
# `X` and `h` on the right.
@dataclass
class SparseMerkleRangeProof:
    # The vector of siblings on the right of the path from root to last leaf. The ones near the
    # bottom are at the beginning of the vector. In the above example, it's `[X, h]`.
    right_siblings: List[HashValue]


    @classmethod
    def from_proto(cls, proto):
        right_siblings = from_proto_siblings(proto.right_siblings, SPARSE_MERKLE_PLACEHOLDER_HASH)
        return cls(right_siblings)



# The complete proof used to authenticate a `Transaction` object.  This structure consists of an
# `AccumulatorProof` from `LedgerInfo` to `TransactionInfo` the verifier needs to verify the
# correctness of the `TransactionInfo` object, and the `TransactionInfo` object that is supposed
# to match the `Transaction`.

@dataclass
class TransactionProof:
    # The accumulator proof from ledger info root to leaf that authenticates the hash of the
    # `TransactionInfo` object.
    ledger_info_to_transaction_info_proof: TransactionAccumulatorProof

    # The `TransactionInfo` object at the leaf of the accumulator.
    transaction_info: TransactionInfo


    # Verifies that a `Transaction` with hash value of `transaction_hash` is the version
    # `transaction_version` transaction in the ledger using the provided proof.  If
    # `event_root_hash` is provided, it's also verified against the proof.
    def verify(
        self,
        ledger_info: LedgerInfo,
        transaction_hash: HashValue,
        event_root_hash: Optional[HashValue],
        transaction_version: Version,
    ):
        ensure(
            bytes(transaction_hash) == bytes(self.transaction_info.transaction_hash),
            "The hash of transaction does not match the transaction info in proof. \
             Transaction hash: {}. Transaction hash provided by proof: {}.",
            transaction_hash,
            self.transaction_info.transaction_hash
        )
        if event_root_hash is not None:
            ensure(
                bytes(event_root_hash) == bytes(self.transaction_info.event_root_hash),
                "Event root hash ({}) doesn't match that in the transaction info ({}).",
                event_root_hash,
                self.transaction_info.event_root_hash
            )
        verify_transaction_info(
            ledger_info,
            transaction_version,
            self.transaction_info,
            self.ledger_info_to_transaction_info_proof,
        )

    @classmethod
    def from_proto(cls, proto_proof):
        ledger_info_to_transaction_info_proof = TransactionAccumulatorProof.from_proto(proto_proof.
            ledger_info_to_transaction_info_proof)
        transaction_info = TransactionInfo.from_proto(proto_proof.transaction_info)
        return cls(ledger_info_to_transaction_info_proof, transaction_info)



# The complete proof used to authenticate the state of an account. This structure consists of the
# `AccumulatorProof` from `LedgerInfo` to `TransactionInfo`, the `TransactionInfo` object and the
# `SparseMerkleProof` from state root to the account.
@dataclass
class AccountStateProof:
    # The accumulator proof from ledger info root to leaf that authenticates the hash of the
    # `TransactionInfo` object.
    ledger_info_to_transaction_info_proof: TransactionAccumulatorProof

    # The `TransactionInfo` object at the leaf of the accumulator.
    transaction_info: TransactionInfo

    # The sparse merkle proof from state root to the account state.
    transaction_info_to_account_proof: SparseMerkleProof

    # Verifies that the state of an account at version `state_version` is correct using the
    # provided proof. If `account_state_blob` is present, we expect the account to exist,
    # otherwise we expect the account to not exist.
    def verify(
        self,
        ledger_info: LedgerInfo,
        state_version: Version,
        account_address_hash: HashValue,
        account_state_blob: Optional[AccountStateBlob]
    ):
        self.transaction_info_to_account_proof.verify(
            self.transaction_info.state_root_hash,
            account_address_hash,
            account_state_blob,
        )
        verify_transaction_info(
            ledger_info,
            state_version,
            self.transaction_info,
            self.ledger_info_to_transaction_info_proof
        )

    @classmethod
    def from_proto(cls, proto_proof):
        ledger_info_to_transaction_info_proof = TransactionAccumulatorProof.from_proto(proto_proof.
            ledger_info_to_transaction_info_proof)
        transaction_info = TransactionInfo.from_proto(proto_proof.transaction_info)
        transaction_info_to_account_proof = SparseMerkleProof.from_proto(proto_proof
            .transaction_info_to_account_proof)
        return cls(ledger_info_to_transaction_info_proof, transaction_info, transaction_info_to_account_proof)



# The complete proof used to authenticate a contract event. This structure consists of the
# `AccumulatorProof` from `LedgerInfo` to `TransactionInfo`, the `TransactionInfo` object and the
# `AccumulatorProof` from event accumulator root to the event.
@dataclass
class EventProof:
    # The accumulator proof from ledger info root to leaf that authenticates the hash of the
    # `TransactionInfo` object.
    ledger_info_to_transaction_info_proof: TransactionAccumulatorProof

    # The `TransactionInfo` object at the leaf of the accumulator.
    transaction_info: TransactionInfo

    # The accumulator proof from event root to the actual event.
    transaction_info_to_event_proof: EventAccumulatorProof


    # Verifies that a given event is correct using provided proof.
    def verify(
        self,
        ledger_info: LedgerInfo,
        event_hash: HashValue,
        transaction_version: Version,
        event_version_within_transaction: Version
    ):
        self.transaction_info_to_event_proof.verify(
            self.transaction_info.event_root_hash,
            event_hash,
            event_version_within_transaction,
        )
        verify_transaction_info(
            ledger_info,
            transaction_version,
            self.transaction_info,
            self.ledger_info_to_transaction_info_proof,
        )

    @classmethod
    def from_proto(cls, proto_proof):
        ledger_info_to_transaction_info_proof = TransactionAccumulatorProof.from_proto(proto_proof.
            ledger_info_to_transaction_info_proof)
        transaction_info = TransactionInfo.from_proto(proto_proof.transaction_info)
        transaction_info_to_event_proof = EventAccumulatorProof.from_proto(proto_proof
            .transaction_info_to_event_proof)
        return cls(ledger_info_to_transaction_info_proof, transaction_info, transaction_info_to_event_proof)


# The complete proof used to authenticate a list of consecutive transactions.
@dataclass
class TransactionListProof:
    # The accumulator range proof from ledger info root to leaves that authenticates the hashes
    # of all `TransactionInfo` objects.
    ledger_info_to_transaction_infos_proof: TransactionAccumulatorRangeProof

    # The `TransactionInfo` objects that correspond to all the transactions.
    transaction_infos: List[TransactionInfo]

    @classmethod
    def new_empty(cls):
        return cls(AccumulatorRangeProof.new_empty(), [])


    # Verifies the list of transactions are correct using the proof. The verifier needs to have
    # the ledger info and the version of the first transaction in possession.
    def verify(
        self,
        ledger_info: LedgerInfo,
        first_transaction_version: Optional[Version],
        transaction_hashes: [HashValue]
    ):
        ensure(
            len(self.transaction_infos) == len(transaction_hashes),
            "The number of TransactionInfo objects ({}) does not match the number of \
             transactions ({}).",
            len(self.transaction_infos),
            len(transaction_hashes)
        )
        zipped = zip(transaction_hashes, self.transaction_infos)
        for txn_hash, txn_info in zipped:
            ensure(
                bytes(txn_hash) == bytes(txn_info.transaction_hash),
                "The hash of transaction does not match the transaction info in proof. \
                 Transaction hash: {}. Transaction hash in txn_info: {}.",
                txn_hash,
                txn_info.transaction_hash
            )
        txn_info_hashes = [x.hash() for x in self.transaction_infos]
        self.ledger_info_to_transaction_infos_proof.verify(
            ledger_info.transaction_accumulator_hash,
            first_transaction_version,
            txn_info_hashes
        )


    @classmethod
    def from_proto(cls, proto_proof):
        ledger_info_to_transaction_infos_proof = TransactionAccumulatorRangeProof.from_proto(proto_proof.
            ledger_info_to_transaction_infos_proof)
        transaction_infos = [TransactionInfo.from_proto(x) for x in proto_proof.transaction_infos]
        return cls(ledger_info_to_transaction_infos_proof, transaction_infos)
