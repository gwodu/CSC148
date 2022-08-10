"""
Question (10 marks)

Implement the Tree method has_path according to the docstring provided.
Read the docstring examples carefully to be sure you understand what the method
should do. The file Q3-instructions.pdf has an example that will be helpful.

We have provided the few pieces of the Tree class that are necessary.

Guidelines:
- Your method MUST be recursive to earn credit.
- Do NOT add to or modify the Tree class.
- Do NOT define any helper methods or functions.

TO HAND IN: Add your code to this file and hand it in on MarkUs.  Be sure to
run the self-test on MarkUs to avoid failing all our tests due to a silly error.

--------------------------------------------------------------------------------
This code is provided solely for the personal and private use of students
taking the CSC148 course at the University of Toronto. Copying for purposes
other than this use is expressly prohibited. All forms of distribution of
this code, whether as given or with any changes, are expressly prohibited.

This file is:
Copyright (c) 2021 Diane Horton, Jonathan Calver, Sophia Huynh, Maryam Majedi,
and Jaisie Sin.
"""
from __future__ import annotations

from typing import Optional, Any, List


class Tree:
    """A recursive tree data structure.
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

    def has_path(self, items: List[int]) -> Optional[List[int]]:
        """Return a description of a path starting at the root of this tree
        and containing each element in items, in order. If there is more than
        one such path, return a description of any one of them. If there is no
        such path, return None.

        A path description is a list of child indexes [c0, c1, c2, ... ck]
        as explained in Q3-instructions.pdf.

        If items == [], return [], since it is trivially true that there is
        a path starting at the root and containing these items.

        >>> t = Tree(1, [Tree(2, []), Tree(3, []), Tree(4, [])])
        >>> t.has_path([1])
        []
        >>> t.has_path([1, 4])
        [2]
        >>> t.has_path([99, 3]) is None
        True
        >>> t.has_path([])
        []
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> baby = Tree(7, [Tree(9, []), Tree(10, [])])
        >>> rt = Tree(3, [Tree(6, []), baby, Tree(8, [])])
        >>> t = Tree(1, [lt, rt])
        >>> t.has_path([1, 3, 7])
        [1, 1]
        >>> t.has_path([1, 3, 7, 9])
        [1, 1, 0]
        >>> t.has_path([1, 3, 7, 9, 15]) is None
        True
        """
        # TODO: implement this method.


if __name__ == '__main__':
    import doctest
    doctest.testmod()
