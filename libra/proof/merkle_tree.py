from libra.hasher import (
    HashValue,
    SparseMerkleInternalHasher, TransactionAccumulatorHasher,
    EventAccumulatorHasher, TestOnlyHasher)
from libra.contract_event import ContractEvent
import more_itertools
from dataclasses import dataclass
from typing import Callable

@dataclass
class MerkleTreeInternalNode:
    hasher: Callable[[], object]
    left_child: HashValue = None
    right_child: HashValue = None


    def hash(self):
        shazer = self.hasher()
        shazer.update(self.left_child)
        shazer.update(self.right_child)
        return shazer.digest()


class SparseMerkleInternalNode(MerkleTreeInternalNode):
    hasher = SparseMerkleInternalHasher

TransactionAccumulatorInternalNode = MerkleTreeInternalNode(TransactionAccumulatorHasher)
EventAccumulatorInternalNode = MerkleTreeInternalNode(EventAccumulatorHasher)
TestAccumulatorInternalNode = MerkleTreeInternalNode(TestOnlyHasher)


def get_accumulator_root_hash(hasher, element_hashes):
    def compute_tree_hash(t):
        if len(t) == 2:
            return MerkleTreeInternalNode(t[0], t[1], hasher).hash()
        else:
            import pdb
            pdb.set_trace()
            #TODO: how to test this branch
            return MerkleTreeInternalNode(t[0], ACCUMULATOR_PLACEHOLDER_HASH, hasher).hash()
    if not element_hashes:
        return ACCUMULATOR_PLACEHOLDER_HASH
    next_level = []
    current_level = element_hashes
    while len(current_level) > 1:
        next_level = [compute_tree_hash(x) for x in more_itertools.chunked(current_level, 2)]
        current_level = next_level
    return current_level[0]

def get_event_root_hash(events):
    event_hashes = [ContractEvent.from_proto(x).hash() for x in events]
    return get_accumulator_root_hash(EventAccumulatorHasher(), event_hashes)



class SparseMerkleLeafNode:
    def __init__(self, key, value_hash):
        self.key = key
        self.value_hash = value_hash

    def hash(self):
        shazer = gen_hasher(b"SparseMerkleLeafNode::libra_types::proof")
        shazer.update(self.key)
        shazer.update(self.value_hash)
        return shazer.digest()
