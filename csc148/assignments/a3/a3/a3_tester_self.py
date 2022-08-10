from typing import List, Tuple, Dict

from a3_sudoku_puzzle import SudokuPuzzle
from a3_word_ladder_puzzle import WordLadderPuzzle, EASY, TRIVIAL
from a3_expression_tree import ExprTree, construct_from_list
from a3_expression_tree_puzzle import ExpressionTreePuzzle
from a3_solver import BfsSolver, DfsSolver

from puzzle import Puzzle


def test_fail_fast_empty_grid():
    s = SudokuPuzzle(4,
                         [
                             [" ", " ", " ", " "],
                             [" ", " ", " ", " "],
                             [" ", " ", " ", " "],
                             [" ", " ", " ", " "]
                             ], {"A", "B", "C", "D"})
    assert s.fail_fast() == False


def test_fail_fast_full_grid():
    r1 = ["A", "B", "C", "D"]
    r2 = ["C", "D", "A", "B"]
    r3 = ["B", "A", "D", "C"]
    r4 = ["D", "C", "B", "A"]
    grid = [r1, r2, r3, r4]
    s = SudokuPuzzle(4, grid, {"A", "B", "C", "D"})
    assert s.is_solved() == True
    assert s.fail_fast() == False


def test_fail_fast_one_cell_empty():
    r1 = ["A", "B", "C", "D"]
    r2 = ["C", "D", "A", "B"]
    r3 = ["B", "A", "D", "C"]
    r4 = ["D", "C", "B", " "]
    grid = [r1, r2, r3, r4]
    s = SudokuPuzzle(4, grid, {"A", "B", "C", "D"})
    assert s.fail_fast() == False


def test_fail_fast_one_cell_filled():
    s = SudokuPuzzle(4,
                     [
                         ["A", " ", " ", " "],
                         [" ", " ", " ", " "],
                         [" ", " ", " ", " "],
                         [" ", " ", " ", " "]
                         ], {"A", "B", "C", "D"})
    assert s.fail_fast() == False


def recursive_path_test(path: List[Puzzle]):
    """Tests if all states in returned path leads to solution, by checking
    if each subsequent path is an extension of its predecessor"""
    if path[0].is_solved():
        return True
    if path[1] in path[0].extensions():
        path.pop(0)
        return recursive_path_test(path)
    else:
        return False


def test_dfs_normal():
    s = SudokuPuzzle(4,
                     [
                         [" ", " ", "B", " "],
                         ["B", " ", "D", "C"],
                         [" ", " ", "A", " "],
                         [" ", " ", "C", " "]
                         ], {"A", "B", "C", "D"})
    solver = DfsSolver()
    actual = solver.solve(s)
    assert len(actual) == 11
    assert recursive_path_test(actual) == True


def test_dfs_unsolvable():
    s = SudokuPuzzle(4,
                     [
                         ["D", "B", " ", "A"],
                         ["C", " ", "D", "B"],
                         [" ", " ", "B", "D"],
                         ["B", "D", "A", " "]
                     ], {"A", "B", "C", "D"})
    solver = DfsSolver()
    block = SudokuPuzzle(4,
                     [
                         ["D", "B", "C", "A"],
                         ["C", "A", "D", "B"],
                         ["A", "C", "B", "D"],
                         ["B", "D", "A", " "]
                     ], {"A", "B", "C", "D"})
    assert solver.solve(s, {str(block)}) == []


def test_dfs_multiple_solutions():
    s = SudokuPuzzle(4,
                     [
                         [" ", " ", "B", " "],
                         ["B", " ", "D", "C"],
                         [" ", " ", "A", " "],
                         [" ", " ", "C", " "]
                     ], {"A", "B", "C", "D"})

    block = SudokuPuzzle(4, [["C", "D", "B", "A"],
                             ["B", "A", "D", "C"],
                             ["D", "C", "A", "B"],
                             ["A", "B", "C", "D"]],
                         {"A", "B", "C", "D"})

    block2 = SudokuPuzzle(4, [["D", "C", "B", "A"],
                              ["B", "A", "D", "C"],
                              ["C", "B", "A", "D"],
                              ["A", "D", "C", "B"]],
                          {"A", "B", "C", "D"})

    block3 = SudokuPuzzle(4, [["D", "C", "B", "A"],
                              ["B", "A", "D", "C"],
                              ["C", "D", "A", "B"],
                              ["A", "B", "C", "D"]],
                          {"A", "B", "C", "D"})

    solver = DfsSolver()
    actual = solver.solve(s, {str(block), str(block2)})
    assert len(actual) == 11
    assert actual[-1] == block3
    assert recursive_path_test(actual) == True


def test_bfs_normal():
    s = SudokuPuzzle(4,
                     [
                         [" ", " ", "B", " "],
                         ["B", " ", "D", "C"],
                         [" ", " ", "A", " "],
                         [" ", " ", "C", " "]
                     ], {"A", "B", "C", "D"})
    solver = BfsSolver()
    actual = solver.solve(s)
    assert len(actual) == 11
    assert recursive_path_test(actual) == True

def test_bfs_exp_t_puzzle():
    example = [['+'], [3, "*"], ["c", "*"], [2, 2]]
    exp_t = construct_from_list(example)
    puz = ExpressionTreePuzzle(exp_t, 39)
    solver = BfsSolver()
    solution = solver.solve(puz)
    assert recursive_path_test(solution) == True

def test_bfs_unsolvable():
    s = SudokuPuzzle(4,
                     [
                         ["D", "B", " ", "A"],
                         ["C", " ", "D", "B"],
                         [" ", " ", "B", "D"],
                         ["B", "D", "A", " "]
                     ], {"A", "B", "C", "D"})
    solver = BfsSolver()
    block = SudokuPuzzle(4,
                         [
                             ["D", "B", "C", "A"],
                             ["C", "A", "D", "B"],
                             ["A", "C", "B", "D"],
                             ["B", "D", "A", " "]
                         ], {"A", "B", "C", "D"})
    assert solver.solve(s, {str(block)}) == []


def test_bfs_multiple_solutions():
    s = SudokuPuzzle(4,
                     [
                         [" ", " ", "B", " "],
                         ["B", " ", "D", "C"],
                         [" ", " ", "A", " "],
                         [" ", " ", "C", " "]
                     ], {"A", "B", "C", "D"})

    block = SudokuPuzzle(4, [["C", "D", "B", "A"],
                             ["B", "A", "D", "C"],
                             ["D", "C", "A", "B"],
                             ["A", "B", "C", "D"]],
                         {"A", "B", "C", "D"})

    block2 = SudokuPuzzle(4, [["D", "C", "B", "A"],
                              ["B", "A", "D", "C"],
                              ["C", "B", "A", "D"],
                              ["A", "D", "C", "B"]],
                          {"A", "B", "C", "D"})

    block3 = SudokuPuzzle(4, [["D", "C", "B", "A"],
                              ["B", "A", "D", "C"],
                              ["C", "D", "A", "B"],
                              ["A", "B", "C", "D"]],
                          {"A", "B", "C", "D"})

    solver = BfsSolver()
    actual = solver.solve(s, {str(block), str(block2)})
    assert len(actual) == 11
    assert actual[-1] == block3
    assert recursive_path_test(actual) == True

def test_word_ladder_extensions():
    wl1 = WordLadderPuzzle("coat", "goal", {"coal", "coat", "goal",
                                            "meal", "meat", "moat"})
    wl2 = WordLadderPuzzle("moat", "goal", {"coal", "coat", "goal",
                                            "meal", "meat", "moat"})
    wl3 = WordLadderPuzzle("coal", "goal", {"coal", "coat", "goal",
                                            "meal", "meat", "moat"})
    wl4 = WordLadderPuzzle("meat", "goal", {"coal", "coat", "goal",
                                            "meal", "meat", "moat"})
    wl5 = WordLadderPuzzle("goal", "goal", {"coal", "coat", "goal",
                                            "meal", "meat", "moat"})
    wl6 = WordLadderPuzzle("meal", "goal", {"coal", "coat", "goal",
                                            "meal", "meat", "moat"})
    assert wl1.extensions() == [wl2, wl3]
    assert wl2.extensions() == [wl1, wl4]
    assert wl3.extensions() == [wl5, wl1]
    assert wl4.extensions() == [wl2, wl6]

def test_word_ladder_get_difficulty_visualiser():
    wl1 = WordLadderPuzzle("coat", "goal", {"coal", "coat", "goal",
                                            "meal", "meat", "moat"})
    assert wl1.get_difficulty() == EASY

def test_word_ladder_get_difficulty_medium():
    wl1 = WordLadderPuzzle("moats", "pears", {"moats", "boats", "meats",
                                            "seats", "sears", "pears",
                                              "hears", "tears", "coats",
                                              "hoats", "heats"})
    assert wl1.get_difficulty() == "medium"

def test_word_ladder_get_difficulty_hard():
    wl1 = WordLadderPuzzle("moaty", "foctl", {"moaty", "meaty", "featy",
                                              "seaty", "seary", "peary",
                                              "heary", "teary", "seary",
                                              "hoaty", "heaty", "beaty",
                                            "boary", "beary", "feary",
                                            "featl", "foatl", "foctl"})
    assert wl1.get_difficulty() == "hard"

def test_populate_lookup_empty():
    expr_t = ExprTree(None, [])
    look_up = {}
    expr_t.populate_lookup(look_up)
    assert len(look_up) == 0

def test_populate_lookup():
    expr_t = ExprTree('+', [
        ExprTree('*', [
                ExprTree("a", []), ExprTree('+', [
                    ExprTree("b", []), ExprTree(4, [])
                                                  ])
                     ]),
        ExprTree("d", [])
                     ])
    look_up = {}
    expr_t.populate_lookup(look_up)
    assert len(look_up) == 3
    assert all(look_up[i] == 0 for i in look_up) == True

def test_populate_lookup2():
    expr_t = ExprTree('+', [
         ExprTree(3, []), ExprTree('*', [
                 ExprTree('x', []), ExprTree('y', [])
                                           ]),
        ExprTree('x', [])
                    ])
    look_up = {}
    expr_t.populate_lookup(look_up)
    assert len(look_up) == 2
    assert all(look_up[i] == 0 for i in look_up) == True

def test_expression_tree_eval_doctest() -> None:
    """Test ExprTree.eval on the provided doctest"""
    exp_t = ExprTree('+', [ExprTree(3, []),
                           ExprTree('*', [ExprTree('x', []),
                                          ExprTree('y', [])]),
                           ExprTree('x', [])])
    look_up = {}
    exp_t.populate_lookup(look_up)
    assert exp_t.eval(look_up) == 3

    look_up['x'] = 7
    look_up['y'] = 3
    assert exp_t.eval(look_up) == 31

def test_expression_tree_eval1() -> None:
    """Test ExprTree.eval on the provided doctest"""
    expr_t = ExprTree('+', [
        ExprTree('*', [
            ExprTree("a", []), ExprTree('+', [
                ExprTree("b", []), ExprTree(6, [])
            ])
        ]),
        ExprTree("d", [])
    ])
    look_up = {}
    expr_t.populate_lookup(look_up)
    assert expr_t.eval(look_up) == 0

    look_up['a'] = 7
    look_up['b'] = 6
    look_up['d'] = 5
    assert expr_t.eval(look_up) == 89

def test_expression_tree_eval2() -> None:
    """Test ExprTree.eval on the provided doctest"""
    expr_t = ExprTree('+', [
        ExprTree(3, []), ExprTree('*', [
            ExprTree('x', []), ExprTree('y', [])
        ]),
        ExprTree('x', [])
    ])
    look_up = {}
    expr_t.populate_lookup(look_up)
    assert expr_t.eval(look_up) == 3

    look_up['x'] = 9
    look_up['y'] = 7
    assert expr_t.eval(look_up) == 75

def test_expression_tree_substitute1() -> None:
    """Test ExprTree.substitute on the provided doctest"""
    # This test relies on ExprTree.__str__ working correctly.
    expr_t = ExprTree('+', [
        ExprTree('*', [
            ExprTree("a", []), ExprTree('+', [
                ExprTree("b", []), ExprTree(4, [])
            ])
        ]),
        ExprTree("d", [])
    ])
    expr_t.substitute({'a': 2, 'b': 3, 'd': 5, '*': '+', '+': '*'})
    assert str(expr_t) == '((2 + (3 * 4)) * 5)'

def test_expression_tree_substitute2() -> None:  # also checks on int
    expr_t = ExprTree('+', [
        ExprTree(3, []), ExprTree('*', [
            ExprTree('x', []), ExprTree('y', [])
        ]),
        ExprTree('x', [])
    ])
    expr_t.substitute({'x': 2, 'y': 3, '*': '+', '+': '*', 3: 4})
    assert str(expr_t) == '(4 * (2 + 3) * 2)'

def test_expression_tree_construct_from_list() -> None:
    example = [['+'], ["+", 3, '*', 5], ["a", "b", "*"], [2, 3, "+"], ["a", "b"],
               [5, 9, "*"], ["c", "d"]]
    exp_t = construct_from_list(example)
    assert exp_t._height() == 5
    assert str(exp_t) == '((a + b + (a * b)) + 3 + (2 * 3 * (5 + 9 + (c * d))) + 5)'

def test_expression_tree_ultimate() -> None:
    example = [['+'], ["+", 3, '*', 5], ["a", "b", "*"], [2, 3, "+"], ["a", "b"],
                [5, 9, "*"], ["c", "d"]]
    exp_t = construct_from_list(example)
    assert exp_t._height() == 5
    assert str(exp_t) == '((a + b + (a * b)) + 3 + (2 * 3 * (5 + 9 + (c * d))) + 5)'

    exam_expr_t = ExprTree("+", [ExprTree("+", [ExprTree("a", []), ExprTree("b", []),
                                                ExprTree("*", [ExprTree("a", []),
                                                               ExprTree("b", [])])]),
                                 ExprTree(3, []), ExprTree("*", [ExprTree(2, []),
                                                                 ExprTree(3, []),
                                                                 ExprTree("+", [
                                                                     ExprTree(5, []),
                                                                     ExprTree(9, []),
                                                                     ExprTree("*", [
                                                                         ExprTree("c", []),
                                                                         ExprTree("d", [])
                                                                     ])
                                                                 ])]),
                                 ExprTree(5, [])])
    assert exam_expr_t == exp_t

    lookup = {}
    exp_t.populate_lookup(lookup)
    assert len(lookup) == 4
    assert all(lookup[i] == 0 for i in lookup) == True
    lookup["a"] = 4
    lookup["b"] = 5
    lookup["c"] = 6
    lookup["d"] = 7
    assert exp_t.eval(lookup) == 373
    exp_t.substitute({"a" : 4, "b" : 4, "c" : 4, "d" : 4, "*" : "+"})
    assert exp_t.eval(lookup) == 51

def test_extension_tree_puzzle_extensions():
    example = [['+'], ["+", 3, '*', 5], ["a", "b", "*"], [2, 3, "+"], ["a", "b"],
               [5, 9, "*"], ["c", "d"]]
    exp_t = construct_from_list(example)
    puz = ExpressionTreePuzzle(exp_t, 7)
    puz.variables["b"] = 1
    puz.variables["d"] = 2
    extensions = puz.extensions()
    assert len(extensions) == 18
    # extensions_puz_list = [str(puz.variables) for puz in extensions]
    # print(extensions_puz_list)

def test_extension_tree_puzzle_fail_fast():
    example = [['+'], ["+", 3, '*', 5], ["a", "b", "*"], [2, 3, "+"], ["a", "b"],
               [5, 9, "*"], ["c", "d"]]
    exp_t = construct_from_list(example)
    puz = ExpressionTreePuzzle(exp_t, 101)
    assert puz.fail_fast() == False #right on the border
    puz.variables["a"] = 4
    puz.variables["b"] = 5
    puz.variables["c"] = 6
    puz.variables["d"] = 7
    assert puz.fail_fast() == True

if __name__ == "__main__":
    import pytest
    pytest.main(["a3_tester_self.py"])
