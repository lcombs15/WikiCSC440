from wiki.web.sudoku import SudokuGame
from wiki.web.sudoku_gen import generate_sudoku, backtrack

import unittest


class TestSudoku(unittest.TestCase):

    def setUp(self) -> None:
        self.board = [[6,3,2,7,8,1,9,4,5],[4,8,7,5,9,6,2,1,3],
                      [5,1,9,2,4,3,8,7,6],[8,6,4,3,5,2,7,9,1],
                      [7,5,1,9,6,8,3,2,4],[2,9,3,1,7,4,6,5,8],
                      [9,4,5,6,3,7,1,8,2],[1,7,6,8,2,5,4,3,9],
                      [3,2,8,4,1,9,5,6,7]]
        self.game = SudokuGame(self.board)

    def test_create_board(self):
        game = SudokuGame([[0] * 9] * 9)
        board = [[0] * 9] * 9
        self.assertEquals(board, game.board)

    def test_solved_not_solved(self):
        game = SudokuGame([[0] * 9] * 9)
        self.assertFalse(game.solved())

    def test_solved_solved(self):
        self.assertTrue(self.game.solved())

    def test_backtrack(self):
        board = [[0, 0, 0, 0, 0, 0, 6, 8, 0],
                [0, 0, 0, 0, 7, 3, 0, 0, 9],
                [3, 0, 9, 0, 0, 0, 0, 4, 5],
                [4, 9, 0, 0, 0, 0, 0, 0, 0],
                [8, 0, 3, 0, 5, 0, 9, 0, 2],
                [0, 0, 0, 0, 0, 0, 0, 3, 6],
                [9, 6, 0, 0, 0, 0, 3, 0, 8],
                [7, 0, 0, 6, 8, 0, 0, 0, 0],
                [0, 2, 8, 0, 0, 0, 0, 0, 0]]

        board = backtrack(board)
        for row in board:
            for col in row:
                self.assertNotEqual(col, 0)

if __name__ == "__main__":
    unittest.main()
