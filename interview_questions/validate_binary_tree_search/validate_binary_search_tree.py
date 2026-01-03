from __future__ import annotations

class TreeNode:
    def __init__(self, val: float, left: TreeNode | None = None, right: TreeNode | None = None):
        self.value: float = val
        self.left: TreeNode = left
        self.right: TreeNode = right

def is_valid_bst_recursion(root: TreeNode, max_value: float = None, min_value: float = None) -> bool:
    """
    Checks if the binary tree is valid
    A valid tree is a binary tree has:
     - the value all left nodes strictly less than the value root and
     - the value of the right nodes strictly greater than the root
     - each subtree is a binary tree
    :param root:
    :param max_value: the maximum value allowed in the tree
    :param min_value: the minimum value allowed in the tree
    :return: True iff the tree is valid
    """
    if max_value is not None and root.value >= max_value:
        return False

    if min_value is not None and root.value <= min_value:
        return False

    if root.left is not None:
        if not is_valid_bst(root.left, root.value, min_value):
            return False
    if root.right is not None:
        if not is_valid_bst(root.right, max_value, root.value):
            return False
    return True

def is_valid_bst(root: TreeNode) -> bool:
    """
    Checks if the binary tree is valid
    A valid tree is a binary tree has:
     - the value all left nodes strictly less than the value root and
     - the value of the right nodes strictly greater than the root
     - each subtree is a binary tree
    """

    stack: list[tuple[TreeNode, float | None, float | None]] = [(root, None, None)]

    while stack:
        node, min_value, max_value = stack.pop()
        if max_value is not None and node.value >= max_value:
            return False
        if min_value is not None and node.value <= min_value:
            return False

        if node.left:
            stack.append((node.left, min_value, node.value))
        if node.right:
            stack.append((node.right, node.value, max_value))
    return True
