import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX = 0
    countO = 0

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == X:
                countX += 1
            if board[row][col] == O:
                countO += 1

    if countX > countO:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    allPossibleActions = set()

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                allPossibleActions.add((row, col))

    return allPossibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # check if is a valid action:
    if action not in actions(board):
        raise Exception("Not a valid action!")

    row, col = action

    board_cp = copy.deepcopy(board)
    board_cp[row][col] = player(board)

    return board_cp


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if checkCol(board, X) or checkRow(board, X) or checkFirstDiagonal(board, X) or checkSecondDiagonal(board, X):
        return X
    elif checkCol(board, O) or checkRow(board, O) or checkFirstDiagonal(board, O) or checkSecondDiagonal(board, O):
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        return max_value(board, -math.inf, math.inf)[1]
    else:
        return min_value(board, -math.inf, math.inf)[1]


# Custom Functions

# Winner:

def checkRow(board, player):
    for row in range(len(board)):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    return False


def checkCol(board, player):
    for col in range(len(board)):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    return False


def checkFirstDiagonal(board, player):
    return board[0][0] == board[1][1] == board[2][2] == player


def checkSecondDiagonal(board, player):
    return board[0][2] == board[1][1] == board[2][0] == player


# Min Max:

def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board), None

    v = -math.inf
    best_action = None

    for action in actions(board):
        min_val = min_value(result(board, action), alpha, beta)[0]

        if min_val > v:
            v = min_val
            best_action = action

        alpha = max(alpha, v)

        if alpha >= beta:
            break

    return v, best_action


def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board), None

    v = math.inf
    best_action = None

    for action in actions(board):
        max_val = max_value(result(board, action), alpha, beta)[0]

        if max_val < v:
            v = max_val
            best_action = action

        beta = min(beta, v)

        if alpha >= beta:
            break

    return v, best_action
