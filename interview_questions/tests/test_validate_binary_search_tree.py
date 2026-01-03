import pytest
from validate_binary_tree_search.validate_binary_search_tree import is_valid_bst, TreeNode



def make_2_level_bst() -> TreeNode:
    left_node = TreeNode(0)
    right_node = TreeNode(2)
    root = TreeNode(1, left_node, right_node)
    return root

def make_1000_level_bst() -> TreeNode:
    root = TreeNode(0)
    for i in range(1, 1000):
        root = TreeNode(i, root)
    return root

def make_invalid_bst() -> TreeNode:
    left_node = TreeNode(2)
    right_node = TreeNode(0)
    root = TreeNode(1, left_node, right_node)
    return root

@pytest.mark.parametrize(
    "tree",
    [TreeNode(10),
     make_2_level_bst(),
     make_1000_level_bst()
     ]
)
def test_does_isValidBST_return_true_for_true_bst(tree) -> None:
    assert is_valid_bst(tree)


@pytest.mark.parametrize(
    "tree",
    [make_invalid_bst()]
)
def test_does_isValidBST_return_false_for_invalid_bst(tree) -> None:
    assert not is_valid_bst(tree)

