from libra.proof.accumulator import InMemoryAccumulator
from libra.proof.definition import LeafCount
from libra.proof.position import FrozenSubtreeSiblingIterator, Position
from libra.proof.merkle_tree import TestAccumulatorInternalNode
from libra.hasher import HashValue, tst_only_hash, TestOnlyHasher, ACCUMULATOR_PLACEHOLDER_HASH
from typing import Mapping, List

def assert_equal(aa, bb):
    assert aa == bb

def assert_true(aa):
    assert aa == True

def next_power_of_two(num):
    for i in range(99999999):
        pow2 = pow(2, i)
        if num <= pow2:
            return pow2


def test_next_power_of_two():
    assert_equal(next_power_of_two(2), 2)
    assert_equal(next_power_of_two(3), 4)


def resize_list(alist, size, value):
    if len(alist) >= size:
        return alist[0:size]
    else:
        diff = size - len(alist)
        for _i in range(diff):
            alist.append(value)
        return alist

def test_resize_list():
    assert_equal(resize_list([1,2,3], 2, None), [1,2])
    assert_equal(resize_list([1,2,3], 6, 2), [1,2,3,2,2,2])

def compute_parent_hash(left_hash: HashValue, right_hash: HashValue) -> HashValue:
    if left_hash == ACCUMULATOR_PLACEHOLDER_HASH and right_hash == ACCUMULATOR_PLACEHOLDER_HASH:
        return ACCUMULATOR_PLACEHOLDER_HASH
    else:
        return TestAccumulatorInternalNode(left_hash, right_hash).hash()


# Given a list of leaves, constructs the smallest accumulator that has all the leaves and
# computes the hash of every node in the tree.
def compute_hashes_for_all_positions(leaves: List[HashValue]) -> Mapping[Position, HashValue]:
    if not leaves:
        return {}

    current_leaves = leaves.copy()
    current_leaves = resize_list(
        current_leaves,
        next_power_of_two(len(leaves)),
        ACCUMULATOR_PLACEHOLDER_HASH
    )
    position_to_hash = {}
    current_level = 0

    while len(current_leaves) > 1:
        #assert is_power_of_two(len(current_leaves))
        parent_leaves = []
        for index in range(0, len(current_leaves), 2):
            left_hash = current_leaves[index]
            right_hash = current_leaves[index + 1]
            parent_hash = compute_parent_hash(left_hash, right_hash)
            parent_leaves.append(parent_hash)

            left_pos = Position.from_level_and_pos(current_level, index)
            right_pos = Position.from_level_and_pos(current_level, index + 1)
            assert left_pos not in position_to_hash
            assert right_pos not in position_to_hash
            position_to_hash[left_pos] = left_hash
            position_to_hash[right_pos] = right_hash
        assert_equal(len(current_leaves), len(parent_leaves) << 1)
        current_leaves = parent_leaves
        current_level += 1
    assert Position.from_level_and_pos(current_level, 0) not in position_to_hash
    position_to_hash[Position.from_level_and_pos(current_level, 0)] = current_leaves[0]
    return position_to_hash


# Computes the root hash of an accumulator with given leaves.
def compute_root_hash_naive(leaves: List[HashValue]) -> HashValue:
    position_to_hash = compute_hashes_for_all_positions(leaves)
    if not position_to_hash:
        return ACCUMULATOR_PLACEHOLDER_HASH
    rightmost_leaf_index = len(leaves) - 1
    return position_to_hash[Position.root_from_leaf_index(rightmost_leaf_index)]



# Helper function to create a list of leaves.
def create_leaves(nums):
    usize = 8
    return [tst_only_hash(x.to_bytes(usize, byteorder="big", signed=False)) for x in range(nums)]

class TestOnlyHasherInMemoryAccumulator(InMemoryAccumulator):
    hasher = TestOnlyHasher


def test_accumulator_append():
    # expected_root_hashes[i] is the root hash of an accumulator that has the first i leaves.
    expected_root_hashes = [compute_root_hash_naive(create_leaves(x)) for x in range(100)]
    leaves = create_leaves(100)
    accumulator = TestOnlyHasherInMemoryAccumulator.default()
    # Append the leaves one at a time and check the root hashes match.
    zipped = zip(leaves, expected_root_hashes)
    for i, (leaf, expected_root_hash) in enumerate(zipped):
        assert_equal(accumulator.root_hash, expected_root_hash)
        assert_equal(accumulator.num_leaves, i)
        accumulator = accumulator.append([leaf])


# proptest! {
#     #[test]
#     def test_accumulator_append_subtrees(
#         hashes1 in vec(any.<HashValue>(), 0..100),
#         hashes2 in vec(any.<HashValue>(), 0..100),
#     ) {
#         # Construct an accumulator with hashes1.
#         accumulator = InMemoryAccumulator.<TestOnlyHasher>.from_leaves(&hashes1);

#         # Compute all the internal nodes in a bigger accumulator with combination of hashes1 and
#         # hashes2.
#         all_hashes = hashes1.clone();
#         all_hashes.extend_from_slice(&hashes2);
#         position_to_hash = compute_hashes_for_all_positions(&all_hashes);

#         subtree_hashes: Vec<_> =
#             FrozenSubtreeSiblingIterator.new(hashes1.len() as LeafCount, all_hashes.len() as LeafCount)
#                 .filter_map(|pos| position_to_hash.get(&pos).cloned())
#                 .collect();
#         new_accumulator = accumulator
#             .append_subtrees(&subtree_hashes, hashes2.len() as LeafCount)
#             .unwrap();
#         prop_assert_equal(
#             new_accumulator.root_hash(),
#             compute_root_hash_naive(&all_hashes)
#         );
#     }
# }
