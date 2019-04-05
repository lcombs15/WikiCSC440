class SudokuGame():
    """
    Game of sudoku with a game board and solution checker
    """
    BOARD_SIZE = 9

    def __init__(self, board):
        self.board = board
        self.isSolved = self.solved()

    def solved(self):
        """
        Checks if the game board has been solved
        :return: True if solved, False otherwise
        """
        def check_rows():
            for row in self.board:
                if len(set(row)) != self.BOARD_SIZE:
                    return False
            return True

        def check_columns():
            for i in range(0, self.BOARD_SIZE):
                column = [row[i] for row in self.board]
                if len(set(column)) != self.BOARD_SIZE:
                    return False
            return True

        def check_squares():
            for i in range(0, 9, 3):
                for j in range(0, 9, 3):
                    square = [row[j:j+3] for row in self.board[i:i+3]]
                    square = [x for y in square for x in y]
                    if len(set(square)) != self.BOARD_SIZE:
                        return False
            return True

        return check_columns() and check_rows() and check_squares()
