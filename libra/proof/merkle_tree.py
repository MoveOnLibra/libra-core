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
class TstAccumulatorInternalNode(MerkleTreeInternalNode):
    #hasher = TestOnlyHasher
    hasher: Callable[[], object] = field(default=TestOnlyHasher)


@dataclass
class SparseMerkleLeafNode:
    key: HashValue
    value_hash: HashValue

    def hash(self):
        shazer = gen_hasher(b"SparseMerkleLeafNode::libra_types::proof")
        shazer.update(bytes(self.key))
        shazer.update(bytes(self.value_hash))
        return shazer.digest()
