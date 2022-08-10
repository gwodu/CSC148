"""
Question (10 marks)

On assignment 2, you worked on a class for a limited kind of arithmetic
expression. Here we have begun to write a similar class, but for boolean
expressions. You will notice two things that are different than on assignment 2
- This class does not allow constant values, only variables.
- This class supports an operator ('not') that has only one operand.

Read the class docstring carefully, and then complete the method eval.

We have provided a __str__ method, in case you find that useful for testing
your code.

Guidelines:
- Your method MUST be recursive to earn credit.
- You must NOT use Python's built-in eval function. Do all the evaluation
  yourself.
- Do NOT define any helper methods or functions.

TO HAND IN: Write your code in this file and hand it in on MarkUs. Be sure you
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

from typing import List, Dict, Optional, Union

# constants for the supported operators
OP_AND = 'and'
OP_OR = 'or'
OP_NOT = 'not'
OPERATORS = [OP_AND, OP_OR, OP_NOT]


class BoolTree:
    """A tree representing a boolean expression.

    This class supports operators that represent logical 'and', 'or', and 'not',
    as well as variables. It does not support constants.

    === Private Attributes ===
    _root: The item stored at this tree's root, or None if the tree is empty.
    _subtrees: The list of all subtrees of this boolean expression tree.

    === Representation Invariants ===
    - If self._root is None then self._subtrees is an empty list.
      This setting of attributes represents an empty tree.

      Note: self._subtrees may be empty when self._root is not None.
      This setting of attributes represents a tree consisting of just one
      node.

    - _subtrees contains no empty trees.
    - if _root is a variable, it is a single character (a-z).
    - if _root is a variable, then _subtrees is an empty list.
    - if _root is OP_AND or OP_OR, len(subtrees) >= 2.
    - if _root is the OP_NOT, len(subtrees) == 1.
    """
    _root: Optional[str]
    _subtrees: List[BoolTree]

    def __init__(self, root: Optional[Union[str, int]],
                 subtrees: List[BoolTree] = None) -> None:
        """Initialize a new BoolTree with the given <root> value and <subtrees>.

        If <root> is None, the tree is empty.

        For convenience, <subtrees> has a default value of None, so the user
        doesn't have to specify it and subtrees will be set to an empty list
        if <subtrees> is not provided by the user.

        Preconditions:
        - if <root> is None, then <subtrees> is an empty list.
        - if <root> is not None, then it is either an operator (OP_AND, OP_OR
          or OP_NOT) or a variable (a-z).
        - if <root> is OP_AND or OP_OR, then len(subtrees) >= 2.
        - if <root> is OP_NOT, then len(subtrees) == 1.
        - if <root> is not an operator, subtrees is an empty list.
        """
        if subtrees is None:
            subtrees = []
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this expression tree is empty.

        >>> t1 = BoolTree(None)
        >>> t1.is_empty()
        True
        >>> t2 = BoolTree('p')
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def eval(self, lookup: Dict[str, bool]) -> bool:
        """Evaluate this boolean expression tree and return the result.

        An empty tree should evaluate to False.

        Precondition:
        lookup contains all of the variables necessary to evaluate this
        expression tree.

        >>> bt = BoolTree(None)
        >>> lookup = {}
        >>> bt.eval(lookup)
        False
        >>> bt = BoolTree('p')
        >>> lookup = {'p': True}
        >>> bt.eval(lookup)
        True
        >>> subtree = BoolTree('or', [BoolTree('p'), BoolTree('q')])
        >>> bt = BoolTree('not', [subtree])
        >>> look_up = {'p': True, 'q': True}
        >>> bt.eval(look_up)
        False
        >>> look_up = {'p': False, 'q': True}
        >>> bt.eval(look_up)
        False
        >>> look_up = {'p': False, 'q': False}
        >>> bt.eval(look_up)
        True
        """
        # TODO: Implement this method.

    def __str__(self) -> str:
        """Return a string representation of this boolean expression tree

        >>> one = BoolTree('or', [BoolTree('a'), BoolTree('b'), BoolTree('c')])
        >>> print(one)
        (a or b or c)
        >>> two = BoolTree('not', [BoolTree('q')])
        >>> print(two)
        (not q)
        >>> three = BoolTree('p')
        >>> print(three)
        p
        >>> bt = BoolTree('and', [one, two, three])
        >>> print(bt)
        ((a or b or c) and (not q) and p)
        """
        if self.is_empty():
            return '()'
        if self._root == OP_NOT:
            return '(' + self._root + ' ' + str(self._subtrees[0]) + ')'
        elif self._root in OPERATORS:  # OP_AND or OP_OR
            rslt = '('
            for c in self._subtrees:
                rslt += str(c) + ' ' + self._root + ' '
            return rslt.rstrip(self._root + ' ') + ')'
        else:  # a variable (str)
            return self._root


if __name__ == '__main__':
    import doctest
    doctest.testmod()
