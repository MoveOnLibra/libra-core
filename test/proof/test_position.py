from libra.proof.position import *
from libra.proof import ensure
from canoser import Uint64
from typing import List
import pytest

def assert_equal(aa, bb):
    assert aa == bb

def assert_true(aa):
    assert aa == True

def test_position_hash():
    v = Position.from_inorder_index(9).__hash__()
    assert v == 9

# Position is marked with in-order-traversal sequence.

# For example
# ```text
#     0
# ```

# Another example
# ```text
#      3
#     /  \
#    /    \
#   1      5
#  / \    / \
# 0   2  4   6
# ```

def test_position_parent():
    position = Position.from_inorder_index(5)
    target = position.parent()
    assert target == Position.from_inorder_index(3)


def test_position_sibling_right():
    position = Position.from_inorder_index(5)
    target = position.sibling()
    assert target == Position.from_inorder_index(1)


def test_position_sibling_left():
    position = Position.from_inorder_index(4)
    target = position.sibling()
    assert target == Position.from_inorder_index(6)


def test_position_left_child():
    position = Position.from_inorder_index(5)
    target = position.left_child()
    assert target == Position.from_inorder_index(4)


def test_position_right_child():
    position = Position.from_inorder_index(5)
    target = position.right_child()
    assert target == Position.from_inorder_index(6)


def test_position_left_child_from_leaf():
    position = Position.from_inorder_index(0)
    with pytest.raises(AssertionError):
        _target = position.left_child()


def test_position_right_child_from_leaf():
    position = Position.from_inorder_index(0)
    with pytest.raises(AssertionError):
        _target = position.right_child()


def test_position_level():
    position = Position.from_inorder_index(5)
    level = position.level()
    assert level == 1
    position = Position.from_inorder_index(0)
    level = position.level()
    assert level == 0
    position = Position.from_inorder_index(3)
    level = position.level()
    assert level == 2

def test_position_is_left_child():
    assert Position.from_inorder_index(1).is_left_child() == True
    assert Position.from_inorder_index(0).is_left_child() == True
    assert Position.from_inorder_index(3).is_left_child() == True
    assert Position.from_inorder_index(7).is_left_child() == True
    assert Position.from_inorder_index(8).is_left_child() == True
    assert Position.from_inorder_index(12).is_left_child() == True


def test_position_is_right_child():
    assert Position.from_inorder_index(5).is_right_child() == True
    assert Position.from_inorder_index(6).is_right_child() == True
    assert Position.from_inorder_index(2).is_right_child() == True
    assert Position.from_inorder_index(11).is_right_child() == True
    assert Position.from_inorder_index(13).is_right_child() == True
    assert Position.from_inorder_index(14).is_right_child() == True
    assert Position.from_inorder_index(10).is_right_child() == True


def test_position_root_from_leaf_index():
    target = Position.root_from_leaf_index(6)
    assert target == Position.from_inorder_index(7)

    target = Position.root_from_leaf_index(0)
    assert target == Position.from_inorder_index(0)

    target = Position.root_from_leaf_index(3)
    assert target == Position.from_inorder_index(3)



def test_root_level_from_leaf_count():
    assert Position.root_level_from_leaf_count(1) == 0
    assert Position.root_level_from_leaf_count(2) == 1
    assert Position.root_level_from_leaf_count(3) == 2
    assert Position.root_level_from_leaf_count(4) == 2
    for i in range(1,100):
        assert Position.root_level_from_leaf_count(i) == Position.root_from_leaf_count(i).level()


def test_is_freezable():
    position = Position.from_inorder_index(5)
    assert position.is_freezable(2) == False
    assert position.is_freezable(3) == True
    assert position.is_freezable(4) == True

    position = Position.from_inorder_index(0)
    assert position.is_freezable(0) == True
    assert position.is_freezable(3) == True
    assert position.is_freezable(4) == True

    # Testing a root
    position = Position.from_inorder_index(7)
    assert position.is_freezable(6) == False
    assert position.is_freezable(7) == True
    assert position.is_freezable(8) == True

    # Testing a leaf
    position = Position.from_inorder_index(10)
    assert position.is_freezable(5) == True


def test_is_freezable_out_of_boundary():
    # Testing out of boundary
    position = Position.from_inorder_index(10)
    assert position.is_freezable(2) == False


def test_is_placeholder():
    assert Position.from_inorder_index(5).is_placeholder(0) == True
    assert Position.from_inorder_index(5).is_placeholder(1) == True
    assert Position.from_inorder_index(5).is_placeholder(2) == False
    assert Position.from_inorder_index(5).is_placeholder(3) == False
    assert Position.from_inorder_index(13).is_placeholder(5) == True
    assert Position.from_inorder_index(13).is_placeholder(6) == False


def test_is_placeholder_out_of_boundary():
    assert Position.from_inorder_index(7).is_placeholder(2) == False
    assert Position.from_inorder_index(11).is_placeholder(2) == True
    assert Position.from_inorder_index(14).is_placeholder(2) == True



def test_sibling_sequence():
    it = Position.from_inorder_index(0).iter_ancestor_sibling()
    sibling_sequence1 = []
    for i, x in enumerate(it):
        if i >= 20:
            break
        sibling_sequence1.append(Position.to_inorder_index(x))
    assert_equal(
        sibling_sequence1,
        [
            2, 5, 11, 23, 47, 95, 191, 383, 767, 1535, 3071, 6143, 12287, 24575, 49151, 98303,
            196_607, 393_215, 786_431, 1_572_863
        ]
    )

    it = Position.from_inorder_index(6).iter_ancestor_sibling()
    sibling_sequence2 = []
    for i, x in enumerate(it):
        if i >= 20:
            break
        sibling_sequence2.append(Position.to_inorder_index(x))
    assert_equal(
        sibling_sequence2,
        [
            4, 1, 11, 23, 47, 95, 191, 383, 767, 1535, 3071, 6143, 12287, 24575, 49151, 98303,
            196_607, 393_215, 786_431, 1_572_863
        ]
    )

    it = Position.from_inorder_index(7).iter_ancestor_sibling()
    sibling_sequence3 = []
    for i, x in enumerate(it):
        if i >= 20:
            break
        sibling_sequence3.append(Position.to_inorder_index(x))
    assert_equal(
        sibling_sequence3,
        [
            23, 47, 95, 191, 383, 767, 1535, 3071, 6143, 12287, 24575, 49151, 98303, 196_607,
            393_215, 786_431, 1_572_863, 3_145_727, 6_291_455, 12_582_911
        ]
    )


def test_parent_sequence():
    it = Position.from_inorder_index(0).iter_ancestor()
    parent_sequence1 = []
    for i, x in enumerate(it):
        if i >= 20:
            break
        parent_sequence1.append(Position.to_inorder_index(x))
    assert_equal(
        parent_sequence1,
        [
            0, 1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 16383, 32767, 65535,
            131_071, 262_143, 524_287
        ]
    )
    it = Position.from_inorder_index(12).iter_ancestor()
    parent_sequence2 = []
    for i, x in enumerate(it):
        if i >= 20:
            break
        parent_sequence2.append(Position.to_inorder_index(x))
    assert_equal(
        parent_sequence2,
        [
            12, 13, 11, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 16383, 32767, 65535,
            131_071, 262_143, 524_287
        ]
    )


def slow_get_frozen_subtree_roots_impl(root: Position, max_leaf_index: Uint64) -> List[Position]:
    if root.is_freezable(max_leaf_index):
        return [root]
    elif root.is_placeholder(max_leaf_index):
        return []
    else:
        roots = slow_get_frozen_subtree_roots_impl(root.left_child(), max_leaf_index)
        roots.extend(slow_get_frozen_subtree_roots_impl(
            root.right_child(),
            max_leaf_index,
        ))
        return roots


def slow_get_frozen_subtree_roots(num_leaves: LeafCount) -> List[Position]:
    if num_leaves == 0:
        return []
    else:
        max_leaf_index = num_leaves - 1
        root = Position.root_from_leaf_count(num_leaves)
        return slow_get_frozen_subtree_roots_impl(root, max_leaf_index)


def test_frozen_subtree_iterator():
    for n in range(10000):
        assert_equal(
            [x for x in FrozenSubTreeIterator(n)],
            slow_get_frozen_subtree_roots(n)
        )


def collect_all_positions(num_leaves: LeafCount, num_new_leaves: LeafCount) -> List[Uint64]:
    it = FrozenSubtreeSiblingIterator(num_leaves, num_new_leaves)
    return [Position.to_inorder_index(x) for x in it]


def test_frozen_subtree_sibling_iterator():
    assert_true(collect_all_positions(0, 0) == [])
    assert_equal(collect_all_positions(0, 1), [0])
    assert_equal(collect_all_positions(0, 2), [1])
    assert_equal(collect_all_positions(0, 7), [3, 9, 12])
    assert_equal(collect_all_positions(0, 1 << 63), [(1 << 63) - 1])

    assert_true(collect_all_positions(1, 1) == [])
    assert_equal(collect_all_positions(1, 2), [2])
    assert_equal(collect_all_positions(1, 3), [2, 4])
    assert_equal(collect_all_positions(1, 4), [2, 5])
    assert_equal(collect_all_positions(1, 5), [2, 5, 8])
    assert_equal(len(collect_all_positions(1, 1 << 63)), 63)

    assert_true(collect_all_positions(2, 2) == [])
    assert_equal(collect_all_positions(2, 3), [4])
    assert_equal(collect_all_positions(2, 4), [5])
    assert_equal(collect_all_positions(2, 5), [5, 8])
    assert_equal(collect_all_positions(2, 6), [5, 9])
    assert_equal(collect_all_positions(2, 7), [5, 9, 12])
    assert_equal(len(collect_all_positions(2, 1 << 63)), 62)

    assert_true(collect_all_positions(3, 3) == [])
    assert_equal(collect_all_positions(3, 4), [6])
    assert_equal(collect_all_positions(3, 5), [6, 8])
    assert_equal(collect_all_positions(3, 8), [6, 11])
    assert_equal(len(collect_all_positions(3, 1 << 63)), 62)

    assert_true(collect_all_positions(6, 6) == [])
    assert_equal(collect_all_positions(6, 7), [12])
    assert_equal(collect_all_positions(6, 8), [13])
    assert_equal(collect_all_positions(6, 16), [13, 23])
    assert_equal(len(collect_all_positions(6, 1 << 63)), 61)


# Returns the number of children a node `level` nodes high in a perfect
# binary tree has.

# Recursively,

# children_from_level(0) = 0
# children_from_level(n) = 2 * (1 + children(n-1))

# But expanding the series this can be computed non-recursively
# sum 2^n, n=1 to x = 2^(x+1) - 2
def children_from_level(level):
    return (1 << (level + 1)) - 2


def slow_nodes_to_left_of(pos: Position) -> Uint64:
    if pos == pos.parent().right_child():
        ret_add = children_from_level(pos.level()) + 1
    else:
        ret_add = 0

    if pos.pos_counting_from_left() == 0:
        parent_add = 0
    else:
        parent_add = nodes_to_left_of(pos.parent().to_inorder_index())
    return ret_add + parent_add



def tst_invariant(invariant_fn):
    for x in range(300):
        position = Position.from_inorder_index(x)
        ensure(
            invariant_fn(position),
            "position = {}",
            position.to_inorder_index()
        )


def tst_invariant_non_leaf(invariant_fn):
    for x in range(300):
        position = Position.from_inorder_index(x)
        ensure(
            position.level() == 0 or invariant_fn(position),
            "position = {}",
            position.to_inorder_index()
        )



def test_basic_invariants():
    tst_invariant_non_leaf(lambda pos : pos == pos.right_child().parent())
    tst_invariant_non_leaf(lambda pos : pos == pos.left_child().parent())

    tst_invariant(lambda pos : pos.level() == pos.parent().level() - 1)
    tst_invariant(lambda pos :
        Position.from_level_and_pos(pos.level(), pos.pos_counting_from_left()) == pos
    )
    tst_invariant(lambda pos :
        Position.from_inorder_index(postorder_to_inorder(inorder_to_postorder(
            pos.to_inorder_index(),
        ))) == pos
    )

    tst_invariant_non_leaf(lambda pos :
        pos.right_child().pos_counting_from_left() == pos.left_child().pos_counting_from_left() + 1
    )

    tst_invariant_non_leaf(lambda pos : pos.left_child().to_inorder_index() < pos.to_inorder_index())
    tst_invariant_non_leaf(lambda pos : pos.to_inorder_index() < pos.right_child().to_inorder_index())
    tst_invariant_non_leaf(lambda pos :
        inorder_to_postorder(pos.left_child().to_inorder_index())
            < inorder_to_postorder(pos.to_inorder_index())
    )
    tst_invariant_non_leaf(lambda pos :
        inorder_to_postorder(pos.right_child().to_inorder_index())
            < inorder_to_postorder(pos.to_inorder_index())
    )

    tst_invariant_non_leaf(lambda pos :
        inorder_to_postorder(pos.right_child().to_inorder_index()) + 1
            == inorder_to_postorder(pos.to_inorder_index())
    )

    tst_invariant_non_leaf(lambda pos : pos.right_child() == pos.left_child().sibling())
    tst_invariant_non_leaf(lambda pos : pos.right_child().sibling() == pos.left_child())

    tst_invariant_non_leaf(lambda pos : pos.right_child() == pos.child(NodeDirection.Right))
    tst_invariant_non_leaf(lambda pos : pos.left_child() == pos.child(NodeDirection.Left))



def test_position_extended():
    for x in range(300):
        pos = Position.from_inorder_index(x)
        assert_equal(slow_nodes_to_left_of(pos), nodes_to_left_of(x))
        pos = Position.from_inorder_index(x)
        assert_equal(
            Position.from_level_and_pos(pos.level(), pos.pos_counting_from_left()),
            pos
        )

    for x in [1 << 33, 1 << 63]:
        pos = Position.from_inorder_index(x)
        assert_equal(slow_nodes_to_left_of(pos), nodes_to_left_of(x))
        pos = Position.from_inorder_index(x)
        assert_equal(
            Position.from_level_and_pos(pos.level(), pos.pos_counting_from_left()),
            pos
        )

    assert_equal(children_from_level(0), 0)
    assert_equal(children_from_level(1), 2)
    assert_equal(children_from_level(2), 6)
    assert_equal(children_from_level(3), 14)
    assert_equal(children_from_level(4), 30)
    assert_equal(children_from_level(5), 62)
    assert_equal(children_from_level(6), 126)
    assert_equal(children_from_level(7), 254)
    assert_equal(children_from_level(8), 510)
    assert_equal(children_from_level(9), 1022)
    # Test for level > 32 to discover overflow bugs
    assert_equal(children_from_level(50), 2_251_799_813_685_246)
    assert_equal(Position.from_inorder_index(0).level(), 0)
    assert_equal(Position.from_inorder_index(0).pos_counting_from_left(), 0)
    assert_equal(inorder_to_postorder(0), 0)
    assert_equal(postorder_to_inorder(0), 0)
    assert_equal(
        Position.from_inorder_index(0).parent(),
        Position.from_inorder_index(1)
    )

    assert_equal(Position.from_inorder_index(1).level(), 1)
    assert_equal(Position.from_inorder_index(1).pos_counting_from_left(), 0)
    assert_equal(inorder_to_postorder(1), 2)
    assert_equal(postorder_to_inorder(2), 1)
    assert_equal(
        Position.from_inorder_index(1).parent(),
        Position.from_inorder_index(3)
    )
    assert_equal(
        Position.from_inorder_index(1).left_child(),
        Position.from_inorder_index(0)
    )
    assert_equal(
        Position.from_inorder_index(1).right_child(),
        Position.from_inorder_index(2)
    )

    assert_equal(Position.from_inorder_index(2).level(), 0)
    assert_equal(Position.from_inorder_index(2).pos_counting_from_left(), 1)
    assert_equal(inorder_to_postorder(2), 1)
    assert_equal(postorder_to_inorder(1), 2)
    assert_equal(
        Position.from_inorder_index(2).parent(),
        Position.from_inorder_index(1)
    )

    assert_equal(Position.from_inorder_index(3).level(), 2)
    assert_equal(Position.from_inorder_index(3).pos_counting_from_left(), 0)
    assert_equal(inorder_to_postorder(3), 6)
    assert_equal(postorder_to_inorder(6), 3)
    assert_equal(
        Position.from_inorder_index(3).parent(),
        Position.from_inorder_index(7)
    )
    assert_equal(
        Position.from_inorder_index(3).left_child(),
        Position.from_inorder_index(1)
    )
    assert_equal(
        Position.from_inorder_index(3).right_child(),
        Position.from_inorder_index(5)
    )

    assert_equal(Position.from_inorder_index(4).level(), 0)
    assert_equal(Position.from_inorder_index(4).pos_counting_from_left(), 2)
    assert_equal(inorder_to_postorder(4), 3)
    assert_equal(postorder_to_inorder(3), 4)
    assert_equal(
        Position.from_inorder_index(4).parent(),
        Position.from_inorder_index(5)
    )

    assert_equal(Position.from_inorder_index(5).level(), 1)
    assert_equal(Position.from_inorder_index(5).pos_counting_from_left(), 1)
    assert_equal(inorder_to_postorder(5), 5)
    assert_equal(postorder_to_inorder(5), 5)
    assert_equal(
        Position.from_inorder_index(5).parent(),
        Position.from_inorder_index(3)
    )
    assert_equal(
        Position.from_inorder_index(5).left_child(),
        Position.from_inorder_index(4)
    )
    assert_equal(
        Position.from_inorder_index(5).right_child(),
        Position.from_inorder_index(6)
    )

    assert_equal(Position.from_inorder_index(6).level(), 0)
    assert_equal(Position.from_inorder_index(6).pos_counting_from_left(), 3)
    assert_equal(inorder_to_postorder(6), 4)
    assert_equal(postorder_to_inorder(4), 6)
    assert_equal(
        Position.from_inorder_index(6).parent(),
        Position.from_inorder_index(5)
    )

    assert_equal(Position.from_inorder_index(7).level(), 3)
    assert_equal(Position.from_inorder_index(7).pos_counting_from_left(), 0)
    assert_equal(inorder_to_postorder(7), 14)
    assert_equal(postorder_to_inorder(14), 7)
    assert_equal(
        Position.from_inorder_index(7).parent(),
        Position.from_inorder_index(15)
    )
    assert_equal(
        Position.from_inorder_index(7).left_child(),
        Position.from_inorder_index(3)
    )
    assert_equal(
        Position.from_inorder_index(7).right_child(),
        Position.from_inorder_index(11)
    )

    assert_equal(Position.from_inorder_index(8).level(), 0)
    assert_equal(Position.from_inorder_index(8).pos_counting_from_left(), 4)
    assert_equal(inorder_to_postorder(8), 7)
    assert_equal(postorder_to_inorder(7), 8)
    assert_equal(
        Position.from_inorder_index(8).parent(),
        Position.from_inorder_index(9)
    )

    assert_equal(Position.from_inorder_index(9).level(), 1)
    assert_equal(Position.from_inorder_index(9).pos_counting_from_left(), 2)
    assert_equal(inorder_to_postorder(9), 9)
    assert_equal(postorder_to_inorder(9), 9)
    assert_equal(
        Position.from_inorder_index(9).parent(),
        Position.from_inorder_index(11)
    )
    assert_equal(
        Position.from_inorder_index(9).left_child(),
        Position.from_inorder_index(8)
    )
    assert_equal(
        Position.from_inorder_index(9).right_child(),
        Position.from_inorder_index(10)
    )

    assert_equal(Position.from_inorder_index(10).level(), 0)
    assert_equal(Position.from_inorder_index(10).pos_counting_from_left(), 5)
    assert_equal(inorder_to_postorder(10), 8)
    assert_equal(postorder_to_inorder(8), 10)
    assert_equal(
        Position.from_inorder_index(10).parent(),
        Position.from_inorder_index(9)
    )

    assert_equal(Position.from_inorder_index(11).level(), 2)
    assert_equal(Position.from_inorder_index(11).pos_counting_from_left(), 1)
    assert_equal(inorder_to_postorder(11), 13)
    assert_equal(postorder_to_inorder(13), 11)
    assert_equal(
        Position.from_inorder_index(11).parent(),
        Position.from_inorder_index(7)
    )
    assert_equal(
        Position.from_inorder_index(11).left_child(),
        Position.from_inorder_index(9)
    )
    assert_equal(
        Position.from_inorder_index(11).right_child(),
        Position.from_inorder_index(13)
    )

    assert_equal(Position.from_inorder_index(12).level(), 0)
    assert_equal(Position.from_inorder_index(12).pos_counting_from_left(), 6)
    assert_equal(inorder_to_postorder(12), 10)
    assert_equal(postorder_to_inorder(10), 12)
    assert_equal(
        Position.from_inorder_index(12).parent(),
        Position.from_inorder_index(13)
    )

    assert_equal(Position.from_inorder_index(13).level(), 1)
    assert_equal(Position.from_inorder_index(13).pos_counting_from_left(), 3)
    assert_equal(inorder_to_postorder(13), 12)
    assert_equal(postorder_to_inorder(12), 13)
    assert_equal(
        Position.from_inorder_index(13).parent(),
        Position.from_inorder_index(11)
    )
    assert_equal(
        Position.from_inorder_index(13).left_child(),
        Position.from_inorder_index(12)
    )
    assert_equal(
        Position.from_inorder_index(13).right_child(),
        Position.from_inorder_index(14)
    )

    assert_equal(Position.from_inorder_index(14).level(), 0)
    assert_equal(Position.from_inorder_index(14).pos_counting_from_left(), 7)
    assert_equal(inorder_to_postorder(14), 11)
    assert_equal(postorder_to_inorder(11), 14)
    assert_equal(
        Position.from_inorder_index(14).parent(),
        Position.from_inorder_index(13)
    )

    assert_equal(Position.from_inorder_index(15).level(), 4)
    assert_equal(Position.from_inorder_index(15).pos_counting_from_left(), 0)
    assert_equal(inorder_to_postorder(15), 30)
    assert_equal(postorder_to_inorder(30), 15)
    assert_equal(
        Position.from_inorder_index(15).parent(),
        Position.from_inorder_index(31)
    )
    assert_equal(
        Position.from_inorder_index(15).left_child(),
        Position.from_inorder_index(7)
    )
    assert_equal(
        Position.from_inorder_index(15).right_child(),
        Position.from_inorder_index(23)
    )

    assert_equal(Position.from_inorder_index(16).level(), 0)
    assert_equal(Position.from_inorder_index(16).pos_counting_from_left(), 8)
    assert_equal(inorder_to_postorder(16), 15)
    assert_equal(postorder_to_inorder(15), 16)
    assert_equal(
        Position.from_inorder_index(16).parent(),
        Position.from_inorder_index(17)
    )

    assert_equal(Position.from_inorder_index(17).level(), 1)
    assert_equal(Position.from_inorder_index(17).pos_counting_from_left(), 4)
    assert_equal(inorder_to_postorder(17), 17)
    assert_equal(postorder_to_inorder(17), 17)
    assert_equal(
        Position.from_inorder_index(17).parent(),
        Position.from_inorder_index(19)
    )
    assert_equal(
        Position.from_inorder_index(17).left_child(),
        Position.from_inorder_index(16)
    )
    assert_equal(
        Position.from_inorder_index(17).right_child(),
        Position.from_inorder_index(18)
    )

    assert_equal(Position.from_inorder_index(18).level(), 0)
    assert_equal(Position.from_inorder_index(18).pos_counting_from_left(), 9)
    assert_equal(inorder_to_postorder(18), 16)
    assert_equal(postorder_to_inorder(16), 18)
    assert_equal(
        Position.from_inorder_index(18).parent(),
        Position.from_inorder_index(17)
    )

    assert_equal(Position.from_inorder_index(19).level(), 2)
    assert_equal(Position.from_inorder_index(19).pos_counting_from_left(), 2)
    assert_equal(inorder_to_postorder(19), 21)
    assert_equal(postorder_to_inorder(21), 19)
    assert_equal(
        Position.from_inorder_index(19).parent(),
        Position.from_inorder_index(23)
    )
    assert_equal(
        Position.from_inorder_index(19).left_child(),
        Position.from_inorder_index(17)
    )
    assert_equal(
        Position.from_inorder_index(19).right_child(),
        Position.from_inorder_index(21)
    )



def test_right_most_child():
    assert_equal(
        Position.from_inorder_index(0).right_most_child(),
        Position.from_inorder_index(0)
    )
    assert_equal(
        Position.from_inorder_index(1).right_most_child(),
        Position.from_inorder_index(2)
    )
    assert_equal(
        Position.from_inorder_index(5).right_most_child(),
        Position.from_inorder_index(6)
    )
    assert_equal(
        Position.from_inorder_index(7).right_most_child(),
        Position.from_inorder_index(14)
    )
    assert_equal(
        Position.from_inorder_index(3).right_most_child(),
        Position.from_inorder_index(6)
    )
    assert_equal(
        Position.from_inorder_index(11).right_most_child(),
        Position.from_inorder_index(14)
    )
    assert_equal(
        Position.from_inorder_index(12).right_most_child(),
        Position.from_inorder_index(12)
    )
    assert_equal(
        Position.from_inorder_index(14).right_most_child(),
        Position.from_inorder_index(14)
    )



def test_left_most_child():
    assert_equal(
        Position.from_inorder_index(0).left_most_child(),
        Position.from_inorder_index(0)
    )
    assert_equal(
        Position.from_inorder_index(1).left_most_child(),
        Position.from_inorder_index(0)
    )
    assert_equal(
        Position.from_inorder_index(5).left_most_child(),
        Position.from_inorder_index(4)
    )
    assert_equal(
        Position.from_inorder_index(7).left_most_child(),
        Position.from_inorder_index(0)
    )
    assert_equal(
        Position.from_inorder_index(3).left_most_child(),
        Position.from_inorder_index(0)
    )
    assert_equal(
        Position.from_inorder_index(11).left_most_child(),
        Position.from_inorder_index(8)
    )
    assert_equal(
        Position.from_inorder_index(12).left_most_child(),
        Position.from_inorder_index(12)
    )
    assert_equal(
        Position.from_inorder_index(14).left_most_child(),
        Position.from_inorder_index(14)
    )

