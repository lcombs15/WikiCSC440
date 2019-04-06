from random import shuffle, randint

solution = None
BOARD_SIZE = 9


def copy_board(board):
    return [row[:] for row in board]


def check_rows(board):
    for row in board:
        xs = set()

        for x in row:
            if x == 0:
                continue

            if x in xs:
                return False

            xs.add(x)

    return True


def check_cols(board):
    cols = [[row[i] for row in board] for i in range(BOARD_SIZE)]
    return check_rows(cols)


def check_sub_boards(board):
    m = int(BOARD_SIZE ** 0.5)

    if m*m != BOARD_SIZE:
        return True

    for i in range(m):
        for j in range(m):
            sub_board = [row[j*m:(j+1)*m] for row in board[i*m:(i+1)*m]]
            xs = set()

            for row in sub_board:
                for x in row:
                    if x == 0:
                        continue

                    if x in xs:
                        return False

                    xs.add(x)

    return True


def check_solution(board):
    return sum([row.count(0) for row in board]) == 0


def solve(board, spots, x):
    global solution

    if len(spots) == 0:
        return

    if solution != None:
        return

    (i, j) = spots[0]
    board[i][j] = x

    is_board_valid = check_rows(board) and check_cols(board) and check_sub_boards(board)
    if not is_board_valid:
        return

    is_board_solved = check_solution(board)
    if is_board_solved:
        solution = board
        return

    for x in range(BOARD_SIZE):
        spots1 = spots[1:]
        solve(copy_board(board), spots1, x+1)


def backtrack(board):
    """
    Solves a Sudoku board

    :param board: [[int]] array representing board to be solved
    :return: [[int]] array representing solved board
    """
    spots = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 0:
                spots.append((i, j))

    for x in range(BOARD_SIZE):
        solve(copy_board(board), spots, x+1)

    return solution


def generate_sudoku(size):
    """
    Generates a solvable sudoku board by removing numbers from a
    pseudo-random solution.

    :param size: number of rows and columns
    :return: [[int]] representation of a valid sudoku board
    """
    global solution
    solution = None
    board = []
    column_indices = list(range(0, size))
    shuffle(column_indices)

    for i, index in enumerate(column_indices):
        row = [0] * 9
        row[index] = i
        board.append(row)

    board = backtrack(board)

    for row in board:
        shuffle(column_indices)
        zeros = randint(size - size // 3, size - size // 5)
        for i in range(zeros):
            row[column_indices[i]] = 0

    return board
