"""CSC148 Summer 2021 Term Test 3

Q3: Trees [20 marks]
-----------------------------------------------------------------------------
Implement the Tree method longest_chain according to the docstring provided.
Read the docstring examples carefully.

We have provided the few pieces of the Tree class that are necessary.

Additional Requirements:
  - Your method **MUST** be recursive to earn credit.
  - You may only add private methods to the Tree class.

Do NOT add any additional import statements.

A syntax checker is available to you on MarkUs. It is only for syntax errors
i.e. it does NOT check for correctness.
"""

from __future__ import annotations
from typing import Any, Optional, List, Union, Tuple


class Tree:
    """A recursive tree data structure.
    """
    # === Private Attributes ===
    # _root: The item stored at this tree's root or None if the tree is empty.
    _root: Optional[Any]
    # _subtrees: The List of all subtrees of this tree.
    _subtrees: List[Tree]

    # === Representation Invariants ===
    # - If self._root is None then self._subtrees is an empty list.
    #     This setting of attributes represents an empty tree.
    #
    #     Note: self._subtrees may be empty when self._root is not None.
    #     This setting of attributes represents a tree consisting of just one
    #     node.
    # - self._subtrees doesn't include empty trees

    def __init__(
        self, root: Optional[Any], subtrees: Optional[List[Tree]] = None
    ) -> None:
        """Initialize a new tree with the given root value and subtrees.

        If <root> is None, this tree is empty.

        For convenience, <subtrees> has a default value of None, so the user
        doesn't have to specify it and subtrees will be set to an empty list
        if <subtrees> is not provided by the user.

        Precondition: if <root> is None, then <subtrees> is empty.
        """
        if subtrees is None:
            subtrees = []
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        >>> t1 = Tree(None)
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3)
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its descendants' items.
        The output is nicely indented.

        You may find this method helpful for debugging.

        >>> n8 = Tree(8, [])
        >>> n1 = Tree(1, [])
        >>> n13 = Tree(13, [n8, n1])
        >>> n2 = Tree(2, [])
        >>> n21 = Tree(21, [n2])
        >>> n9 = Tree(9, [])
        >>> root = Tree(1, [n13, n21, n9])
        >>> print(root)
        1
          13
            8
            1
          21
            2
          9
        """
        return self._str_helper().strip()

    def _str_helper(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            str_repr = ("  " * depth) + str(self._root) + '\n'

            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                str_repr += subtree._str_helper(depth + 1)
            return str_repr

    def longest_chain(self):
        """Return the length of the longest path in the Tree such that all
        values in the path are the same value.

        >>> t = Tree(None)
        >>> t.longest_chain()
        0
        >>> t = Tree(2)
        >>> t.longest_chain()  # The longest chain is for the value 2
        1
        >>> t1 = Tree(4, [Tree(4, [Tree(4, []), Tree(3, [])]), Tree(5, [])])
        >>> t2 = Tree(7, [Tree(5, []), Tree(5, [])])
        >>> t3 = Tree(20, [Tree(10, [Tree(10, [])])])
        >>> t = Tree(5, [t1, t2, t3])
        >>> print(t)
        5
          4
            4
              4
              3
            5
          7
            5
            5
          20
            10
              10
        >>> t.longest_chain()  # The longest chain is the value 4
        3
        """
        if self.is_empty():
            return 0
        else:
            chain_list = []
            main_tree_chain = self._find_chain(self._root, 0)
            chain_list.append(main_tree_chain)
            self._traverse_subtrees(chain_list)
            return max(chain_list)

    def _find_chain(self, num: int, count: int) -> int:
        """Finds the length of the longest train with num as the starting number"""
        if self._root == num and len(self._subtrees) == 0:
            return count + 1
        else:
            count += 1
            count_list = []
            for subtree in self._subtrees:
                if subtree._root == num:
                    count_list.append(subtree._find_chain(num, count))
                else:
                    count_list.append(0)
            return max(count_list)

    def _traverse_subtrees(self, chain_list: List[int]) -> None:
        """Go through all the lengths and append the lengths of the longest chains
        from their roots to chain_list"""
        if len(self._subtrees) == 0:
            chain_list.append(1)
            return
        else:
            for subtree in self._subtrees:
                chain_length = subtree._find_chain(subtree._root, 0)
                chain_list.append(chain_length)
                subtree._traverse_subtrees(chain_list)

if __name__ == "__main__":
    # Not required for term test, but is here to verify the sample solution:

    # import python_ta
    # python_ta.check_all(config={
    #     'disable': ['E1136']
    # })

    import doctest
    doctest.testmod()
