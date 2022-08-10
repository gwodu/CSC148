""" CSC148 Summer 2021 Term Test 3

Q2: Binary Search Trees (BSTs) [20 marks]
--------------------------------------------------------------------------
Provided below is a modified version of the BinarySearchTree class used during
lecture. The __init__ method accepts optional parameters for left and right
subtrees to facilitate testing. It is your responsibility to ensure the
parameters you pass results in a structure that obeys the BST property.

The **balance factor** of a BST is the absolute difference between the height of
its  right subtree and the height of its left subtree. For instance, the balance
factor of the BST rooted at 5 is 0 (since both the left and right subtrees have
a height of 3).

                                    5
                                  ⟋  ⟍
                                 3     6
                               ⟋  ⟍     ⟍
                              2    4      7
                             /             ⟍
                            1               9


The **maximum balance factor** of a BST is the largest balance factor for any of
the subtrees in the BST. E.g., in the above BST, the maximum balance factor is 2
since the subtree rooted at 6 has a balance factor of 2.

A buggy method that attempts to find the maximum balance factor of a BST is
provided as buggy_max_balance_factor.

    (i) [3 marks] Write a valid pytest test case that **passes** when run on
    the buggy_max_balance_factor method.

    (ii) [3 marks] Write a valid pytest test case that **fails** when run on
    the buggy_max_balance_factor method.

    (iii) [4 marks] Making minimal changes to the buggy code, provide the
    correct implementation of finding the maximum balance factor under
    the defined method max_balance_factor.

    (iv) [10 marks] Implement the method from_pre_order based on its docstring
    description.

If you provide more than two test cases, we will only grade the first two.
Remember to start your tests with test_

Do NOT add any additional import statements.

A syntax checker is available to you on MarkUs. It is only for syntax errors
i.e. it does NOT check for correctness.
"""

from __future__ import annotations
from typing import Any, Optional, List


# TODO - Add **Exactly** two test cases for the method buggy_max_balance_factor
def test_max_balance_correct():
    tree = BinarySearchTree(6)
    left = BinarySearchTree(4)
    left._left = BinarySearchTree(2)
    left._left._left = BinarySearchTree(1)
    left._right = BinarySearchTree(5)
    right = BinarySearchTree(7)
    tree._left = left
    tree._right = right
    assert tree.buggy_max_balance_factor() == 2

def test_max_balance_wrong():
    tree = BinarySearchTree(6)
    left = BinarySearchTree(4)
    left._left = BinarySearchTree(2)
    left._left._left = BinarySearchTree(1)
    left._right = BinarySearchTree(5)
    right = BinarySearchTree(9)
    right._left = BinarySearchTree(7)
    right._right = BinarySearchTree(11)
    right._right._right = BinarySearchTree(12)
    tree._left = left
    tree._right = right
    assert tree.buggy_max_balance_factor() == 1

class BinarySearchTree:
    """Binary Search Tree class.

    This class represents a binary tree satisfying the Binary Search Tree
    property: for every item, its value is >= all items stored in its left
    subtree, and <= all items stored in its right subtree.
    """
    # === Private Attributes ===
    # The item stored at the root of the tree, or None if the tree is empty.
    _root: Optional[Any]
    # The left subtree, or None if the tree is empty.
    _left: Optional[BinarySearchTree]
    # The right subtree, or None if the tree is empty.
    _right: Optional[BinarySearchTree]

    # === Representation Invariants ===
    #  - If self._root is None, then so are self._left and self._right.
    #    This represents an empty BST.
    #  - If self._root is not None, then self._left and self._right
    #    are BinarySearchTrees.
    #  - (BST Property) If self is not empty, then
    #    all items in self._left are <= self._root, and
    #    all items in self._right are >= self._root.

    def __init__(self, root: Optional[Any], left=None, right=None) -> None:
        """Initialize a new BST containing only the given root value.
        If <root> is None, initialize an empty tree.

        For convenience, the <left> and <right> subtrees can be provided
        by the user.

        Precondition:
            - If left is not None, left is a valid BST and
              all values in left <= root
            - If right is not None, right is a valid BST and
              all values in right >= root
        """

        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = left or BinarySearchTree(None)
            self._right = right or BinarySearchTree(None)

    def is_empty(self) -> bool:
        """Return whether this BST is empty.

        >>> bst = BinarySearchTree(None)
        >>> bst.is_empty()
        True
        >>> bst = BinarySearchTree(10)
        >>> bst.is_empty()
        False
        """
        return self._root is None

    def __str__(self) -> str:
        """Return a string representation of this BST.

        This string uses indentation to show depth.
        """
        return self._str_indented(0).strip()

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this BST.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            answer = depth * '  ' + str(self._root) + '\n'
            answer += self._left._str_indented(depth + 1)
            answer += self._right._str_indented(depth + 1)
            return answer

    def height(self) -> int:
        """Return the height of this BST.

        >>> BinarySearchTree(None).height()
        0
        >>> bst = BinarySearchTree(7)
        >>> bst.height()
        1
        >>> bst._left = BinarySearchTree(5)
        >>> bst.height()
        2
        >>> bst._right = BinarySearchTree(9)
        >>> bst.height()
        2
        """
        # This method is provided for you. Don't change it
        if self.is_empty():
            return 0
        else:
            return max(self._left.height(), self._right.height()) + 1

    def buggy_max_balance_factor(self):
        """Return the maximum balance factor in this BinarySearchTree.

        This version of the code is buggy.
        """
        if self.is_empty():
            return 0

        left_height, right_height = self._left.height(), self._right.height()

        balance = abs(left_height - right_height)
        return balance

    # def balance_factor(self):
    #     """Returns the balance factor of a tree"""
    #     if self.is_empty():
    #         return 0
    #
    #     left_height, right_height = self._left.height(), self._right.height()
    #
    #     balance = abs(left_height - right_height)
    #     return balance


    def max_balance_factor(self):
        """Return the maximum balance factor in this BinarySearchTree.
        """
        # TODO - Write the correct implementation
        if self.is_empty():
            return 0

        left_height, right_height = self._left.height(), self._right.height()

        balance = abs(left_height - right_height)
        max_balance = balance

        left_max = self._left.max_balance_factor()
        right_max = self._left.max_balance_factor()

        if left_max > max_balance:
            max_balance = left_max
        if right_max > max_balance:
            max_balance = right_max

        return max_balance

    def from_pre_order(self, traversal: List[Any]) -> None:
        """Populate this BinarySearchTree with the values in this <pre_order>
        traversal.

        Preconditions:
            - This BinarySearchTree is empty
            - All values in traversal are unique.

        >>> bst = BinarySearchTree(None)
        >>> bst.from_pre_order([])
        >>> bst.is_empty()
        True
        >>> bst = BinarySearchTree(None)
        >>> bst.from_pre_order([5])
        >>> print(bst)
        5
        >>> bst = BinarySearchTree(None)
        >>> bst.from_pre_order([5, 3, 2, 4, 14])
        >>> print(bst)
        5
          3
            2
            4
          14
        """
        # TODO - Implement this method according to its docstring
        if len(traversal) == 0:
            pass
        else:
            for item in traversal:
                self._insert(item)

    def _insert(self, item: Any) -> None:
        """Insert <item> into this BST, maintaining the BST property.
        """
        if self.is_empty():
            self._root = item
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)
        elif item <= self._root:
            self._left._insert(item)
        else:
            self._right._insert(item)

if __name__ == "__main__":
    # Not required for term test, but is here to verify the sample solution:

    # import python_ta
    # python_ta.check_all(config={
    #     'disable': ['E1136']
    # })

    import doctest
    doctest.testmod()

    import pytest
    pytest.main(["q2.py"])
