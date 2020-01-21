from libra.proof.merkle_tree import MerkleTreeInternalNode
from libra.proof.definition import LeafCount, MAX_ACCUMULATOR_LEAVES
from libra.proof.anyhow import ensure
from libra.proof.position import count_ones, trailing_zeros
from libra.hasher import HashValue, ACCUMULATOR_PLACEHOLDER_HASH
from dataclasses import dataclass, field
from typing import List, Optional

# This module implements an in-memory Merkle Accumulator that is similar to what we use in
# storage. This accumulator will only store a small portion of the tree -- for any subtree that
# is full, we store only the root. Also we only store the frozen nodes, therefore this structure
# will always store up to `Log(n)` number of nodes, where `n` is the total number of leaves in
# the tree.
#
# This accumulator is immutable once constructed. If we append new leaves to the tree we will
# obtain a new accumulator instance and the old one remains unchanged.

@dataclass
class InMemoryAccumulator:
    # Represents the roots of all the full subtrees from left to right in this accumulator. For
    # example, if we have the following accumulator, this vector will have two hashes that
    # correspond to `X` and `e`.
    # ```text
    #                 root
    #                /    \
    #              /        \
    #            /            \
    #           X              o
    #         /   \           / \
    #        /     \         /   \
    #       o       o       o     placeholder
    #      / \     / \     / \
    #     a   b   c   d   e   placeholder
    # ```
    frozen_subtree_roots: List[HashValue]

    # The total number of leaves in this accumulator.
    num_leaves: LeafCount

    # The root hash of this accumulator.
    root_hash: HashValue

    #hasher: Callable[[], object]# = field(init=False)


    # Constructs a new accumulator with roots of existing frozen subtrees. Returns error if the
    # number of frozen subtree roots does not match the number of leaves.
    @classmethod
    def new(cls, frozen_subtree_roots: List[HashValue], num_leaves: LeafCount):
        ensure(
            len(frozen_subtree_roots) == count_ones(num_leaves),
            "The number of frozen subtrees does not match the number of leaves. \
             frozen_subtree_roots.len(): {}. num_leaves: {}.",
            len(frozen_subtree_roots),
            num_leaves,
        )
        root_hash = cls.compute_root_hash(frozen_subtree_roots, num_leaves)
        return cls(frozen_subtree_roots, num_leaves, root_hash)


    # Constructs a new accumulator with given leaves.
    @classmethod
    def from_leaves(cls, leaves: [HashValue]):
        return cls.default().append(leaves)


    # Appends a list of new leaves to an existing accumulator. Since the accumulator is
    # immutable, the existing one remains unchanged and a new one representing the result is
    # returned.
    def append(self, leaves: [HashValue]):
        frozen_subtree_roots = self.frozen_subtree_roots
        num_leaves = self.num_leaves
        for leaf in leaves:
            self.append_one(frozen_subtree_roots, num_leaves, leaf)
            num_leaves += 1
        return self.__class__.new(frozen_subtree_roots, num_leaves)


    # Appends one leaf. This will update `frozen_subtree_roots` to store new frozen root nodes
    # and remove old nodes if they are now part of a larger frozen subtree.
    def append_one(
        self,
        frozen_subtree_roots: List[HashValue],
        num_existing_leaves: LeafCount,
        leaf: HashValue
    ):
        # For example, this accumulator originally had N = 7 leaves. Appending a leaf is like
        # adding one to this number N: 0b0111 + 1 = 0b1000. Every time we carry a bit to the left
        # we merge the rightmost two subtrees and compute their parent.
        # ```text
        #       A
        #     /   \
        #    /     \
        #   o       o       B
        #  / \     / \     / \
        # o   o   o   o   o   o   o
        # ```

        # First just append the leaf.
        frozen_subtree_roots.append(leaf)

        # Next, merge the last two subtrees into one. If `num_existing_leaves` has N trailing
        # ones, the carry will happen N times.
        num_trailing_ones = trailing_zeros(~num_existing_leaves)

        for _i in range(num_trailing_ones):
            right_hash = frozen_subtree_roots.pop()
            left_hash = frozen_subtree_roots.pop()
            parent_hash = MerkleTreeInternalNode(left_hash, right_hash, self.__class__.hasher).hash()
            frozen_subtree_roots.append(parent_hash)


    # Appends a list of new subtrees to the existing accumulator. This is similar to
    # [`append`](Accumulator.append) except that the new leaves themselves are not known and
    # they are represented by `subtrees`. As an example, given the following accumulator that
    # currently has 10 leaves, the frozen subtree roots and the new subtrees are annotated below.
    # Note that in this case `subtrees[0]` represents two new leaves `A` and `B`, `subtrees[1]`
    # represents four new leaves `C`, `D`, `E` and `F`, `subtrees[2]` represents four new leaves
    # `G`, `H`, `I` and `J`, and the last `subtrees[3]` represents one new leaf `K`.
    #
    # ```text
    #                                                                           new_root
    #                                                                         /          \
    #                                                                       /              \
    #                                                                     /                  \
    #                                                                   /                      \
    #                                                                 /                          \
    #                                                               /                              \
    #                                                             /                                  \
    #                                                           /                                      \
    #                                                         /                                          \
    #                                                       /                                              \
    #                                                     /                                                  \
    #                                                   /                                                      \
    #                                                 /                                                          \
    #                                         old_root                                                            o
    #                                        /        \                                                          / \
    #                                      /            \                                                       /   placeholder
    #                                    /                \                                                    /
    #                                  /                    \                                                 /
    #                                /                        \                                              /
    #                              /                            \                                           o
    #                            /                                \                                        / \
    #                          /                                    \                                     /    \
    #                        /                                       o                                  /        \
    # frozen_subtree_roots[0]                                      /   \                              /            \
    #                    /   \                                    /     \                           /                \
    #                   /     \                                  /       \                        /                    \
    #                  o       o                                o         subtrees[1]  subtrees[2]                     o
    #                 / \     / \                              / \                / \          / \                    / \
    #                o   o   o   o      frozen_subtree_roots[1]   subtrees[0]    o   o        o   o                  o   placeholder
    #               / \ / \ / \ / \                         / \           / \   / \ / \      / \ / \                / \
    #               o o o o o o o o                         o o           A B   C D E F      G H I J  K (subtrees[3]) placeholder
    # ```
    def append_subtrees(
        self,
        subtrees: List[HashValue],
        num_new_leaves: LeafCount,
    ):
        ensure(
            num_new_leaves <= MAX_ACCUMULATOR_LEAVES - self.num_leaves,
            "Too many new leaves. self.num_leaves: {}. num_new_leaves: {}.",
            self.num_leaves,
            num_new_leaves
        )
        if self.num_leaves == 0:
            return cls.new(subtrees, num_new_leaves)

        current_subtree_roots = self.frozen_subtree_roots.copy()
        current_num_leaves = self.num_leaves
        remaining_new_leaves = num_new_leaves
        subtree_iter = subtrees.__iter__()

        # Check if we want to combine a new subtree with the rightmost frozen subtree. To do that
        # this new subtree needs to represent `rightmost_frozen_subtree_size` leaves, so we need
        # to have at least this many new leaves remaining.
        rightmost_frozen_subtree_size = 1 << trailing_zeros(current_num_leaves)
        while remaining_new_leaves >= rightmost_frozen_subtree_size:
            # Note that after combining the rightmost frozen subtree of size X with a new subtree,
            # we obtain a subtree of size 2X. If there was already a frozen subtree of size 2X, we
            # need to carry this process further.
            mask = rightmost_frozen_subtree_size
            current_hash = subtree_iter.__next__()
            while current_num_leaves & mask != 0:
                left_hash = current_subtree_roots.pop()
                current_hash = MerkleTreeInternalNode(left_hash, current_hash, self.__class__.hasher).hash()
                mask <<= 1
            current_subtree_roots.append(current_hash)
            current_num_leaves += rightmost_frozen_subtree_size
            remaining_new_leaves -= rightmost_frozen_subtree_size
            rightmost_frozen_subtree_size = mask

        # Now all the new subtrees are smaller than the rightmost frozen subtree. We just append
        # all of them. Note that if the number of new subtrees does not actually match the number
        # of new leaves, `Self.new` below will raise an error.
        current_num_leaves += remaining_new_leaves
        current_subtree_roots.extend(subtree_iter)
        return cls.new(current_subtree_roots, current_num_leaves)


    def version(self):
        if self.num_leaves == 0:
            return 0
        else:
            return self.num_leaves - 1


    # Computes the root hash of an accumulator given the frozen subtree roots and the number of
    # leaves in this accumulator.
    @classmethod
    def compute_root_hash(cls, frozen_subtree_roots: List[HashValue], num_leaves: LeafCount) -> HashValue:
        if len(frozen_subtree_roots) == 0:
            return ACCUMULATOR_PLACEHOLDER_HASH
        elif len(frozen_subtree_roots) == 1:
            return frozen_subtree_roots[0]

        # The trailing zeros do not matter since anything below the lowest frozen subtree is
        # already represented by the subtree roots.
        bitmap = num_leaves >> trailing_zeros(num_leaves)
        current_hash = ACCUMULATOR_PLACEHOLDER_HASH
        frozen_subtree_iter = reversed(frozen_subtree_roots)

        while bitmap > 0:
            if bitmap & 1 != 0:
                current_hash = MerkleTreeInternalNode(
                    frozen_subtree_iter.__next__(),
                    current_hash,
                    cls.hasher
                ).hash()
            else:
                current_hash = MerkleTreeInternalNode(
                    current_hash,
                    ACCUMULATOR_PLACEHOLDER_HASH,
                    cls.hasher
                ).hash()
            bitmap >>= 1
        return current_hash


    @classmethod
    def default(cls):
        return cls.new([], 0)
