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

This module contains the abstract Solver class and its two subclasses, which
find solutions to puzzles, step by step.
"""

from __future__ import annotations

from typing import List, Optional, Set, Tuple

# You may remove this import if you don't use it in your code.
from adts import Queue

from puzzle import Puzzle


class Solver:
    """"
    A solver for full-information puzzles. This is an abstract class
    and purely provides the interface for our solve method.
    """

    # You may NOT change the interface to the solve method.
    # Note the optional parameter seen and its type.
    # Your implementations of this method in the two subclasses should use seen
    # to keep track of all puzzle states that you encounter during the
    # solution process.
    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        raise NotImplementedError


# Your solve method MUST be a recursive function (i.e. it must make
# at least one recursive call to itself)
# You may NOT change the interface to the solve method.
class DfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a depth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.

        Note: A user of this method may pass a set of puzzle states that
        shouldn't appear in the path to the solution. You should also update
        seen to include states, that you have encountered, which are not the
        solved state of the puzzle.
        """
        if seen is None:
            seen = set()
            seen_set = seen
        else:
            seen_set = seen

        if str(puzzle) in seen_set:
            return []
        elif puzzle.fail_fast():
            seen_set.add(str(puzzle))
            return []
        elif puzzle.is_solved():
            return [puzzle]
        else:
            seen_set.add(str(puzzle))
            extensions = puzzle.extensions()
            for p_state in extensions:
                new_solt = self.solve(p_state, seen_set)
                if new_solt != []:
                    return [puzzle] + new_solt
        return []


# Hint: You may find a Queue useful here.
class BfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a breadth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.

        Note: A user of this method may pass a set of puzzle states that
        shouldn't appear in the path to the solution. You should also update
        seen to include states, that you have encountered, which are not the
        solved state of the puzzle.
        """

        if seen is None:  # add seen = set(); and seen_set = set()
            seen = set()
            seen_set = seen
        else:
            seen_set = seen

        p_state_queue = Queue()
        p_state_queue.enqueue(puzzle)
        parent_to_extension = []  # list of tuple(parent, extensions)
        solved_state = None
        while not p_state_queue.is_empty():
            curr_p_state = p_state_queue.dequeue()
            if not curr_p_state.fail_fast() and not str(curr_p_state)\
                    in seen_set:
                if not curr_p_state.is_solved():
                    _enqueue_extensions(p_state_queue, curr_p_state,
                                        seen_set)
                    # connector_tuple => (puzzle, puzzle.extensions())
                    connector_tuple =\
                        (curr_p_state, curr_p_state.extensions(),)
                    parent_to_extension.append(connector_tuple)
                else:
                    solved_state = curr_p_state
                    break
            else:
                seen_set.add(str(curr_p_state))
        if solved_state is not None:
            return\
                self._get_me_my_path(puzzle, solved_state, parent_to_extension)
        else:
            return []

    def _get_me_my_path(self, origin_puzzle: Puzzle, passed_puzzle: Puzzle,
                        p_list: List[Tuple[Puzzle, List[Puzzle]]])\
            -> List[Puzzle]:
        """Populate <dict> with <puzzle> extensions mapping to <puzzle>
        Precondition: The first passed_puzzle must be solved"""
        # if len(p_list) == 0:
        #     return []
        # else:
        if passed_puzzle == origin_puzzle:
            return [passed_puzzle]
        else:
            i = 0
            while i < len(p_list):  # this while loop finds the parent puzzle
                p_puzzle = p_list[i][0]
                if passed_puzzle in p_list[i][1]:
                    # p_list.pop(i)
                    parent_plus_puzzle =\
                        self._get_me_my_path(origin_puzzle,
                                             p_puzzle, p_list) + [passed_puzzle]
                    return parent_plus_puzzle
                else:
                    i += 1
        # return []


def _enqueue_extensions(queue: Queue, puzzle: Puzzle,
                        seen: Set[str]) -> None:
    """Enqueue extensions in <extensions> in <queue> if they are not in seen
    and they do not fail fast, and update seen with the str representation
    extensions in <extensions>"""

    seen.add(str(puzzle))
    extensions = puzzle.extensions()
    for p_state in extensions:
        queue.enqueue(p_state)  # Adds elements of <extensions> to queue


if __name__ == "__main__":
    # you may add any code you want to use for testing here
    import python_ta

    python_ta.check_all(config={
        # # uncomment to disable openning pyta output in browser
        'pyta-reporter': 'ColorReporter',
        'allowed-io': [],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing', '__future__', 'puzzle', 'adts'
        ],
        'disable': ['E1136'],
        'max-attributes': 15
    })
