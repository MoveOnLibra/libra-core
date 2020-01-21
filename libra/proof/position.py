from __future__ import annotations
from libra.hasher import HashValue
from libra.proof.definition import LeafCount, MAX_ACCUMULATOR_LEAVES, MAX_ACCUMULATOR_PROOF_DEPTH
from libra.proof.mod import ensure
from canoser import DelegateT, Uint64, Uint32
from enum import Enum
from dataclasses import dataclass

def trailing_zeros(longint):
  manipulandum = bin(longint)
  return len(manipulandum)-len(manipulandum.rstrip('0'))

def leading_zeros(longint, bitlen=64):
    if longint == 0:
        return bitlen
    manipulandum = bin(longint)
    assert manipulandum[0:2] == '0b'
    return bitlen + 2 - len(manipulandum)

def count_ones(num):
    return bin(num)[2:].count('1')


# This module provides an abstraction for positioning a node in a binary tree,
# A `Position` uniquely identifies the location of a node

# In this implementation, `Position` is represented by the in-order-traversal sequence number
# of the node.  The process of locating a node and jumping between nodes is done through
# in-order position calculation, which can be done with bit manipulation.

# For example
# ```text
#      3
#     /  \
#    /    \
#   1      5 <-[Node index, a.k.a, Position]
#  / \    / \
# 0   2  4   6

# 0   1  2   3 <[Leaf index]
# ```
# Note1: The in-order-traversal counts from 0
# Note2: The level of tree counts from leaf level, start from 0
# Note3: The leaf index starting from left-most leaf, starts from 0

class NodeDirection(Enum):
    Left = 0
    Right = 1

@dataclass#(unsafe_hash=True)
class Position:
    value : Uint64
    # invariant Position.0 < Uint64::max_value() - 1

    def __hash__(self):
        return self.value.__hash__()

    # What level is this node in the tree, 0 if the node is a leaf,
    # 1 if the level is one above a leaf, etc.
    def level(self) -> Uint32:
        return trailing_zeros(~self.value)


    def is_leaf(self) -> bool:
        return self.value & 1 == 0

    # What position is the node within the level? i.e. how many nodes
    # are to the left of this node at the same level
    def pos_counting_from_left(self) -> Uint64:
        return self.value >> (self.level() + 1)


    # pos count start from 0 on each level
    @staticmethod
    def from_level_and_pos(level: Uint32, pos: Uint64) -> Position:
        assert level < 63
        assert (1 << level) > 0
        level_one_bits = (1 << level) - 1
        shifted_pos = pos << (level + 1)
        return Position(shifted_pos | level_one_bits)

    @staticmethod
    def from_inorder_index(index: Uint64) -> Position:
        return Position(index)


    def to_inorder_index(self) -> Uint64:
        return self.value


    @staticmethod
    def from_postorder_index(index: Uint64) -> Position:
        return Position(postorder_to_inorder(index))


    def to_postorder_index(self) -> Uint64:
        return inorder_to_postorder(self.to_inorder_index())


    # What is the parent of this node?
    def parent(self) -> Position:
        assert self.value < Uint64.max_value - 1    #invariant
        return Position(
            (self.value | isolate_rightmost_zero_bit(self.value))
                & ~(isolate_rightmost_zero_bit(self.value) << 1)
        )



    # What is the left node of this node? Will overflow if the node is a leaf
    def left_child(self) -> Position:
        assert self.is_leaf() == False
        return Position.child(self, NodeDirection.Left)



    # What is the right node of this node? Will overflow if the node is a leaf
    def right_child(self) -> Position:
        assert self.is_leaf() == False
        return Position.child(self, NodeDirection.Right)



    def child(self, dir: NodeDirection) -> Position:
        assert self.is_leaf() == False
        assert self.value < Uint64.max_value - 1    #invariant

        if dir == NodeDirection.Left:
            direction_bit = 0
        else:
            direction_bit = isolate_rightmost_zero_bit(self.value)
        return Position((self.value | direction_bit) & ~(isolate_rightmost_zero_bit(self.value) >> 1))



    # Whether this position is a left child of its parent.  The observation is that,
    # after stripping out all right-most 1 bits, a left child will have a bit pattern
    # of xxx00(11..), while a right child will be represented by xxx10(11..)
    def is_left_child(self) -> bool:
        assert self.value < Uint64.max_value - 1    #invariant
        return self.value & (isolate_rightmost_zero_bit(self.value) << 1) == 0


    def is_right_child(self) -> bool:
        return not self.is_left_child()


    # Opposite of get_left_node_count_from_position.
    @staticmethod
    def from_leaf_index(leaf_index: Uint64) -> Position:
        return Position.from_level_and_pos(0, leaf_index)


    # This method takes in a node position and return its sibling position

    # The observation is that, after stripping out the right-most common bits,
    # two sibling nodes flip the the next right-most bits with each other.
    # To find out the right-most common bits, first remove all the right-most ones
    # because they are corresponding to level's indicator. Then remove next zero right after.
    def sibling(self) -> Position:
        assert self.value < Uint64.max_value - 1    #invariant
        return Position(self.value ^ (isolate_rightmost_zero_bit(self.value) << 1))


    # Given a leaf index, calculate the position of a minimum root which contains this leaf
    # This method calculates the index of the smallest root which contains this leaf.
    # Observe that, the root position is composed by a "height" number of ones

    # For example
    # ```text
    #     0010010(node)
    #     0011111(smearing)
    #     -------
    #     0001111(root)
    # ```
    def root_from_leaf_index(leaf_index: Uint64) -> Position:
        leaf = Position.from_leaf_index(leaf_index)
        return Position(smear_ones_for_u64(leaf.value) >> 1)


    def root_from_leaf_count(leaf_count: LeafCount) -> Position:
        assert leaf_count > 0
        return Position.root_from_leaf_index((leaf_count - 1))


    def root_level_from_leaf_count(leaf_count: LeafCount) -> Uint32:
        assert leaf_count > 0
        index = (leaf_count - 1)
        return MAX_ACCUMULATOR_PROOF_DEPTH + 1 - leading_zeros(index)


    # Given a node, find its right most child in its subtree.
    # Right most child is a Position, could be itself, at level 0
    def right_most_child(self) -> Position:
        level = self.level()
        return Position(self.value + (1 << level) - 1)


    # Given a node, find its left most child in its subtree
    # Left most child is a node, could be itself, at level 0
    def left_most_child(self) -> Position:
        # Turn off its right most x bits. while x=level of node
        level = self.level()
        return Position(turn_off_right_most_n_bits(self.value, level))


# The following part of the position implementation is logically separate and
# depends on our notion of freezable.  It should probably move to another module.

    # Given index of right most leaf, calculate if a position is the root
    # of a perfect subtree that does not contain any placeholder nodes.

    # First find its right most child
    # the right most child of any node will be at leaf level, which will be a either placeholder
    # node or leaf node. if right most child is a leaf node, then it is freezable.
    # if right most child is larger than max_leaf_node, it is a placeholder node, and not
    # freezable.
    def is_freezable(self, leaf_index: Uint64) -> bool:
        leaf = Position.from_leaf_index(leaf_index)
        right_most_child = self.right_most_child()
        return right_most_child.value <= leaf.value


    # Given index of right most leaf, calculate if a position should contain
    # a placeholder node at this moment
    # A node is a placeholder if both two conditions below are true:
    # 1, the node's in order traversal seq > max_leaf_node's, and
    # 2, the node does not have left child or right child.
    def is_placeholder(self, leaf_index: Uint64) -> bool:
        leaf = Position.from_leaf_index(leaf_index)
        if self.value <= leaf.value:
            return False
        if self.left_most_child().value <= leaf.value:
            return False
        return True

    # Creates an `AncestorIterator` using this position.
    def iter_ancestor(self) -> AncestorIterator:
        return AncestorIterator(self)


    # Creates an `AncestorSiblingIterator` using this position.
    def iter_ancestor_sibling(self) -> AncestorSiblingIterator:
        return AncestorSiblingIterator(self)




# `AncestorSiblingIterator` generates current sibling position and moves itself to its parent
# position for each iteration.
@dataclass
class AncestorSiblingIterator:
    position: Position

    def __iter__(self):
        return self

    def __next__(self):
        current_sibling_position = self.position.sibling()
        self.position = self.position.parent()
        return current_sibling_position


# `AncestorIterator` generates current position and moves itself to its parent position for each
# iteration.
@dataclass
class AncestorIterator:
    position: Position

    def __iter__(self):
        return self

    def __next__(self):
        current_position = self.position
        self.position = self.position.parent()
        return current_position



# Traverse leaves from left to right in groups that forms full subtrees, yielding root positions
# of such subtrees.
# Note that each 1-bit in num_leaves corresponds to a full subtree.
# For example, in the below tree of 5=0b101 leaves, the two 1-bits corresponds to Fzn2 and L4
# accordingly.

# ```text
#            Non-fzn
#           /       \
#          /         \
#         /           \
#       Fzn2         Non-fzn
#      /   \           /   \
#     /     \         /     \
#    Fzn1    Fzn3  Non-fzn  [Placeholder]
#   /  \    /  \    /    \
#  L0  L1  L2  L3 L4   [Placeholder]
# ```
@dataclass
class FrozenSubTreeIterator:
    bitmap: Uint64
    seen_leaves: Uint64 = 0
    # invariant seen_leaves < Uint64::max_value() - bitmap

    def __iter__(self):
        return self

    def __next__(self):
        assert self.seen_leaves < Uint64.max_value - self.bitmap # invariant
        if self.bitmap == 0:
            raise StopIteration

        # Find the remaining biggest full subtree.
        # The MSB of the bitmap represents it. For example for a tree of 0b1010=10 leaves, the
        # biggest and leftmost full subtree has 0b1000=8 leaves, which can be got by smearing all
        # bits after MSB with 1-bits (got 0b1111), right shift once (got 0b0111) and add 1 (got
        # 0b1000=8). At the same time, we also observe that the in-order numbering of a full
        # subtree root is (num_leaves - 1) greater than that of the leftmost leaf, and also
        # (num_leaves - 1) less than that of the rightmost leaf.
        root_offset = smear_ones_for_u64(self.bitmap) >> 1
        assert root_offset < self.bitmap # relate bit logic to integer logic
        num_leaves = root_offset + 1
        leftmost_leaf = Position.from_leaf_index(self.seen_leaves)
        root = Position.from_inorder_index(leftmost_leaf.to_inorder_index() + root_offset)

        # Mark it consumed.
        self.bitmap &= ~num_leaves
        self.seen_leaves += num_leaves
        return root

# Given an accumulator of size `current_num_leaves`, `FrozenSubtreeSiblingIterator` yields the
# positions of required subtrees if we want to append these subtrees to the existing accumulator
# to generate a bigger one of size `new_num_leaves`.

# See [`crate::proof::accumulator::Accumulator::append_subtrees`] for more details.
@dataclass
class FrozenSubtreeSiblingIterator:
    current_num_leaves: LeafCount
    remaining_new_leaves: LeafCount


    # Constructs a new `FrozenSubtreeSiblingIterator` given the size of current accumulator and
    # the size of the bigger accumulator.
    def __init__(self, current_num_leaves: LeafCount, new_num_leaves: LeafCount):
        ensure(
            new_num_leaves <= MAX_ACCUMULATOR_LEAVES,
            "An accumulator can have at most 2^{} leaves. Provided num_leaves: {}.",
            MAX_ACCUMULATOR_PROOF_DEPTH,
            new_num_leaves,
        )
        ensure(
            current_num_leaves <= new_num_leaves,
            "Number of leaves needs to be increasing: current_num_leaves: {}, new_num_leaves: {}",
            current_num_leaves,
            new_num_leaves
        )
        self.current_num_leaves = current_num_leaves
        self.remaining_new_leaves = new_num_leaves - current_num_leaves


    # Helper function to return the next set of leaves that form a complete subtree.  For
    # example, if there are 5 leaves (..0101), 2 ^ (63 - 61 leading zeros) = 4 leaves should be
    # taken next.
    def next_new_leaf_batch(self) -> LeafCount:
        zeros = leading_zeros(self.remaining_new_leaves)
        return 1 << (MAX_ACCUMULATOR_PROOF_DEPTH - zeros)


    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining_new_leaves == 0:
            raise StopIteration

        # Now we compute the size of the next subtree. If there is a rightmost frozen subtree, we
        # may combine it with a subtree of the same size, or append a smaller one on the right. In
        # case self.current_num_leaves is zero and there is no rightmost frozen subtree, the
        # largest possible one is appended.
        def get_next_subtree_leaves():
            if self.current_num_leaves > 0:
                rightmost_frozen_subtree_leaves = 1 << trailing_zeros(self.current_num_leaves)
                if self.remaining_new_leaves >= rightmost_frozen_subtree_leaves:
                    return rightmost_frozen_subtree_leaves
                else:
                    return self.next_new_leaf_batch()
            else:
                return self.next_new_leaf_batch()
        next_subtree_leaves = get_next_subtree_leaves()
        # Now that the size of the next subtree is known, we compute the leftmost and rightmost
        # leaves in this subtree. The root of the subtree is then the middle of these two leaves.
        first_leaf_index = self.current_num_leaves
        last_leaf_index = first_leaf_index + next_subtree_leaves - 1
        self.current_num_leaves += next_subtree_leaves
        self.remaining_new_leaves -= next_subtree_leaves

        return Position.from_inorder_index(
            (first_leaf_index + last_leaf_index) #as Uint64,
        )




def children_of_node(node: Uint64) -> Uint64:
    return (isolate_rightmost_zero_bit(node) << 1) - 2


# In a post-order tree traversal, how many nodes are traversed before `node`
# not including nodes that are children of `node`.
def nodes_to_left_of(node: Uint64) -> Uint64:
    # If node = 0b0100111, ones_up_to_level = 0b111
    ones_up_to_level = isolate_rightmost_zero_bit(node) - 1
    # Unset all the 1s due to the level
    unset_level_zeros = node ^ ones_up_to_level

    # What remains is a 1 bit set every time a node navigated right
    # For example, consider node=5=0b101. unset_level_zeros=0b100.
    # the 1 bit in unset_level_zeros at position 2 represents the
    # fact that 5 is the right child at the level 1. At this level
    # there are 2^2 - 1 children on the left hand side.

    # So what we do is subtract the count of one bits from unset_level_zeros
    # to account for the fact that if the node is the right child at level
    # n that there are 2^n - 1 children.
    return unset_level_zeros - count_ones(unset_level_zeros)


# Given `node`, an index in an in-order traversal of a perfect binary tree,
# what order would the node be visited in in post-order traversal?
# For example, consider this tree of in-order nodes.
#
# ```text
#      3
#     /  \
#    /    \
#   1      5
#  / \    / \
# 0   2  4   6
# ```
#
# The post-order ordering of the nodes is:
# ```text
#      6
#     /  \
#    /    \
#   2      5
#  / \    / \
# 0   1  3   4
# ```
#
# post_order_index(1) == 2
# post_order_index(4) == 3
def inorder_to_postorder(node: Uint64) -> Uint64:
    children = children_of_node(node)
    left_nodes = nodes_to_left_of(node)
    return children + left_nodes


def postorder_to_inorder(node: Uint64) -> Uint64:
    # The number of nodes in a full binary tree with height `n` is `2^n - 1`.
    full_binary_size = Uint64.max_value
    bitmap = 0
    for i in range(63, -1, -1):
        if node >= full_binary_size:
            node -= full_binary_size
            bitmap |= 1 << i
        full_binary_size >>= 1
    level = node # as u32
    pos = bitmap >> level
    return Position.from_level_and_pos(level, pos).to_inorder_index()





# Some helper functions to perform general bit manipulation

# Smearing all the bits starting from MSB with ones
def smear_ones_for_u64(v: Uint64) -> Uint64:
    n = v
    n |= n >> 1;
    n |= n >> 2;
    n |= n >> 4;
    n |= n >> 8;
    n |= n >> 16;
    n |= n >> 32;
    return n


# Turn off n right most bits
# For example
# ```text
#     00010010101
#     -----------
#     00010010100 n=1
#     00010010000 n=3
# ```
def turn_off_right_most_n_bits(v: Uint64, n: u32) -> Uint64:
    assert n < 64
    return (v >> n) << n


# Finds the rightmost 0-bit, turns off all bits, and sets this bit to 1 in
# the result. For example:
# ```text
#     01110111  (x)
#     --------
#     10001000  (~x)
# &   01111000  (x+1)
#     --------
#     00001000
# ```
# http://www.catonmat.net/blog/low-level-bit-hacks-you-absolutely-must-know/
def isolate_rightmost_zero_bit(v: Uint64) -> Uint64:
    return ~v & (v + 1)
