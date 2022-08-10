"""
We've defined a Tree method for you to implement below named insert_child.
In this method, we've given you a basic sketch of the different scenarios
you'll need to consider.

Your tasks are listed below.
    1.      Implement the base case (when the Tree is empty).
    2.      Implement the case where self._root == parent
            (i.e. the case where we're inserting item to the Tree).
    3 + 4.  Implement the recursive case.
            There are two tasks here:
                - Task 3 is for correctly handling the case when item
                  is inserted into one of the subtrees.
                - Task 4 is for correctly handling the case when item is not
                  inserted into any of the subtrees.

You may not add any additional methods to Tree.

Submit your code on MarkUs and run the automated self-test.
Your grade on the quiz will be based solely on the results of the self-test.
(i.e. if you pass all of the tests, you get full marks on the quiz.)
"""

from __future__ import annotations
from typing import Optional, Any, List
import pytest


class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.
    """
    # === Private Attributes ===
    # The item stored at this tree's root, or None if the tree is empty.
    _root: Optional[Any]
    # The list of all subtrees of this tree.
    _subtrees: List[Tree]

    # === Representation Invariants ===
    # - If self._root is None then self._subtrees is an empty list.
    #   This setting of attributes represents an empty tree.
    #
    #   Note: self._subtrees may be empty when self._root is not None.
    #   This setting of attributes represents a tree consisting of just one
    #   node.

    def insert_child(self, item: Any, parent: Any) -> bool:
        """Insert <item> into this tree as a child of a Tree with _root
        <parent>.

        If successful, return True. If <parent> is not in this tree, return
        False.

        If <parent> appears more than once in this tree, <item> should only
        be inserted once (you can pick where to insert it).
        """
        if self.is_empty():
            return False
        elif self._root == parent:
            self._subtrees.append(Tree(item, []))
            return True
        else:
            ...  # TODO: Fill in this case. (Task 3 + 4)
            # Hint: You'll want to make recursive calls. Think about what
            #       the recursive calls *should* return if a child was inserted
            #       into a subtree. What about if it wasn't inserted?
            return self._subtrees.insert_child(item, parent)


    ############################################################################
    # Below are the other Tree methods that are available to you.
    # Do NOT modify these methods.
    ############################################################################
    def __init__(self, root: Optional[Any], subtrees: List[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If <root> is None, the tree is empty.
        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + str(self._root) + '\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                s += subtree._str_indented(depth + 1)
            return s


if __name__ == '__main__':
    pytest.main(['quiz8.py'])
