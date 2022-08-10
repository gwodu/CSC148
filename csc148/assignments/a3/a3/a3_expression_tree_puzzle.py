"""
CSC148, Summer 2021
Assignment 3: Automatic Puzzle Solver
==============================
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Jonathan Calver, Sophia Huynh,
         Maryam Majedi, and Jaisie Sin.

All of the files in this directory are:
Copyright (c) 2021 Diane Horton, Jonathan Calver, Sophia Huynh,
                   Maryam Majedi, and Jaisie Sin.

This module is adapted from the CSC148 Winter 2021 A2 with permission from
the author.

=== Module Description ===

This module contains the ExpressionTreePuzzle class.
"""

from __future__ import annotations

from typing import List, Dict

from a3_expression_tree import ExprTree
from puzzle import Puzzle


class ExpressionTreePuzzle(Puzzle):
    """"
    An expression tree puzzle.

    === Public Attributes ===
    variables: the dictionary of variable name (str) - value (int) pairs
               A variable is considered "unassigned" unless it has a
               non-zero value.
    target: the target value for the expression tree to evaluate to

    === Private Attributes ===
    _tree: the expression tree

    === Representation Invariants ===
    - variables contains a key for each variable appearing in _tree

    - all values stored in variables are single digit integers (0-9).
    """
    _tree: ExprTree
    variables: Dict[str, int]
    target: int

    def __init__(self, tree: ExprTree, target: int) -> None:
        """
        Create a new expression tree puzzle given the provided
        expression tree and the target value. The variables are initialized
        using the tree's populate_lookup method.

        >>> puz = ExpressionTreePuzzle(ExprTree('a', []), 4)
        >>> puz.variables == {'a': 0}
        True
        >>> puz.target
        4
        """
        self.variables = {}
        tree.populate_lookup(self.variables)
        self._tree = tree
        self.target = target

    def is_solved(self) -> bool:
        """
        Return True iff ExpressionTreePuzzle self is solved.

        The puzzle is solved if all variables have been assigned a non-zero
        value and the expression tree evaluates to the target value.

        >>> exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
        >>> puz = ExpressionTreePuzzle(exp_t, 7)
        >>> puz.is_solved()
        False
        >>> puz.variables['a'] = 7
        >>> puz.is_solved()
        False
        >>> puz.variables['a'] = 5
        >>> puz.variables['b'] = 2
        >>> puz.is_solved()
        True
        """
        if all(self.variables[i] != 0 for i in self.variables) and\
                self._tree.eval(self.variables) == self.target:
            return True
        else:
            return False

    def __str__(self) -> str:
        """
        Return a string representation of this ExpressionTreePuzzle.

        The first line should show the dictionary of variables and the
        second line should show the string representation of the algebraic
        equation represented by the puzzle.

        >>> exprt = ExprTree('+', [ExprTree('*', \
                                            [ExprTree('a', []), \
                                             ExprTree('+', [ExprTree('b', []), \
                                                            ExprTree(6, []), \
                                                            ExprTree(6, []), \
                                                           ])]), \
                                   ExprTree(5, [])])
        >>> puz = ExpressionTreePuzzle(exprt, 61)
        >>> print(puz)
        {'a': 0, 'b': 0}
        ((a * (b + 6 + 6)) + 5) = 61
        """
        return str(self.variables) + "\n" + str(self._tree) + " = " +\
            str(self.target)

    def extensions(self) -> List[ExpressionTreePuzzle]:
        """
        Return the list of legal extensions of this ExpressionTreePuzzle.

        A legal extension is a new ExpressionTreePuzzle equal to this
        ExpressionTreePuzzle, except that it assigns a single currently
        unassigned variable a value in the range 1-9.

        A variable is "unassigned" if it has a value of 0.

        A copy of the expression tree and variables dictionary should be
        used in each extension made to avoid unintended aliasing.

        >>> exp_t = ExprTree('a', [])
        >>> puz = ExpressionTreePuzzle(exp_t, 7)
        >>> exts_of_puz = puz.extensions()
        >>> len(exts_of_puz)
        9
        >>> exts_of_an_ext = exts_of_puz[0].extensions()
        >>> len(exts_of_an_ext)
        0
        >>> exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
        >>> puz = ExpressionTreePuzzle(exp_t, 8)
        >>> exts_of_puz = puz.extensions()
        >>> len(exts_of_puz)
        18
        """
        extensions = []
        for variable in self.variables:
            if self.variables[variable] == 0:
                for num in range(1, 10):
                    new_expression_puzzle = ExpressionTreePuzzle(
                        self._tree.copy(), self.target)
                    new_expression_puzzle.variables = self.variables.copy()
                    new_expression_puzzle.variables[variable] = num
                    extensions.append(new_expression_puzzle)
        return extensions

    # The specifics of how you implement this are up to you.
    # Hint 1: remember that a puzzle can only be extended by assigning a value
    #         to an unassigned variable.
    # Hint 2: remember that our expression tree only supports addition,
    #         multiplication, and non-negative integers.
    def fail_fast(self) -> bool:
        """
        Return True if this ExpressionTreePuzzle can be quickly determined to
        have no solution, False otherwise.

        """
        if not self.is_solved():
            variables_copy = self.variables.copy()
            tree_copy = self._tree.copy()
            puz_copy = ExpressionTreePuzzle(tree_copy, self.target)
            puz_copy.variables = variables_copy
            for variable in puz_copy.variables:
                if puz_copy.variables[variable] == 0:
                    puz_copy.variables[variable] = 1

            if puz_copy._tree.eval(puz_copy.variables) > self.target:
                return True
        return False

    def __eq__(self, other: ExpressionTreePuzzle) -> bool:
        """Return True if other's tree, variables and target are equal to self's
        own"""
        return self._tree == other._tree and\
            self.variables == other.variables and self.target == other.target


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        # # uncomment to disable openning pyta output in browser
        'pyta-reporter': 'ColorReporter',
        'allowed-io': [],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing', '__future__',
            'a3_expression_tree', 'puzzle', 'solver'
        ],
        'disable': ['E1136'],
        'max-attributes': 15
    })
