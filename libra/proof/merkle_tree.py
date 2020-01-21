from libra.hasher import (
    HashValue, gen_hasher,
    SparseMerkleInternalHasher, TransactionAccumulatorHasher,
    EventAccumulatorHasher, TestOnlyHasher)
from libra.contract_event import ContractEvent
import more_itertools
from dataclasses import dataclass, field
from typing import Callable

@dataclass
class MerkleTreeInternalNode:
    left_child: HashValue
    right_child: HashValue
    hasher: Callable[[], object]# = field(init=False)


    def hash(self):
        shazer = self.hasher()
        shazer.update(bytes(self.left_child))
        shazer.update(bytes(self.right_child))
        return shazer.digest()

@dataclass
class SparseMerkleInternalNode(MerkleTreeInternalNode):
    #hasher = SparseMerkleInternalHasher
    hasher: Callable[[], object] = field(default=SparseMerkleInternalHasher)

@dataclass
class TransactionAccumulatorInternalNode(MerkleTreeInternalNode):
    #hasher = TransactionAccumulatorHasher
    hasher: Callable[[], object] = field(default=TransactionAccumulatorHasher)

@dataclass
class EventAccumulatorInternalNode(MerkleTreeInternalNode):
    #hasher = EventAccumulatorHasher
    hasher: Callable[[], object] = field(default=EventAccumulatorHasher)

@dataclass
class TestAccumulatorInternalNode(MerkleTreeInternalNode):
    #hasher = TestOnlyHasher
    hasher: Callable[[], object] = field(default=TestOnlyHasher)



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


@dataclass
class SparseMerkleLeafNode:
    key: HashValue
    value_hash: HashValue

    def hash(self):
        shazer = gen_hasher(b"SparseMerkleLeafNode::libra_types::proof")
        shazer.update(bytes(self.key))
        shazer.update(bytes(self.value_hash))
        return shazer.digest()
