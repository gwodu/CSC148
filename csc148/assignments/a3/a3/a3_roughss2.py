from a3_sudoku_puzzle import SudokuPuzzle
from a3_solver import DfsSolver
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
actual = solver.solve(s, {str(block), str(block2), str(block3)})
print(actual)


