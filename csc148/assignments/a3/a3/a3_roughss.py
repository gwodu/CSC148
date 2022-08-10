from a3_sudoku_puzzle import SudokuPuzzle
from a3_word_ladder_puzzle import WordLadderPuzzle, EASY, TRIVIAL
from a3_expression_tree import ExprTree, construct_from_list
from a3_expression_tree_puzzle import ExpressionTreePuzzle
from a3_solver import BfsSolver, DfsSolver


example = [['+'], [3, '*', 'a', '+'], ['a', 'b'], [5, 'c']]
exp_t = construct_from_list(example)
