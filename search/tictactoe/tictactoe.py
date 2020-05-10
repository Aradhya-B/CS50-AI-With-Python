"""
Tic Tac Toe Player
"""

import math
import copy

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
    xMoves = count_moves_in_board(board, X)
    oMoves = count_moves_in_board(board, O)
    if xMoves == oMoves:
        return X
    else:
        return O

def count_moves_in_board(board, move):
    count = 0
    for row in board:
        for col in row:
            if col == move:
                count += 1
    return count

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = set()
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col is EMPTY:
                possibleActions.add((i, j))
    return possibleActions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    boardCopy = copy.deepcopy(board)
    currPlayer = player(boardCopy)
    possibleActions = actions(boardCopy)
    if action in possibleActions:
        boardCopy[action[0]][action[1]] = currPlayer
    else:
        raise Exception('not possible to make action')
    return boardCopy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    rowWinner = check_for_winner_on_rows(board)
    diagonalWinner = check_for_winner_on_diagonals(board)
    columnWinner = check_for_winner_on_columns(board)

    if rowWinner:
        return rowWinner
    elif diagonalWinner:
        return diagonalWinner
    elif columnWinner:
        return columnWinner
    else:
        return None

def check_for_winner_on_rows(board):
    winner = None
    for row in board:
        if all(el == row[0] for el in row):
            winner = row[0]
            break
    return winner

def check_for_winner_on_diagonals(board):
    winner = None
    leftDiagonal = [board[0][0], board[1][1], board[2][2]]
    rightDiagonal = [board[0][2], board[1][1], board[2][0]]
    if all(el == leftDiagonal[0] for el in leftDiagonal):
        winner = leftDiagonal[0]
    elif all(el == rightDiagonal[0] for el in rightDiagonal):
        winner = rightDiagonal[0]
    return winner
            
def check_for_winner_on_columns(board):
    winner = None
    leftColumn = [board[0][0], board[1][0], board[2][0]]
    middleColumn = [board[0][1], board[1][1], board[2][1]]
    rightColumn = [board[0][2], board[1][2], board[2][2]]
    if all(el == leftColumn[0] for el in leftColumn):
        winner = leftColumn[0]
    elif all(el == middleColumn[0] for el in middleColumn):
        winner = middleColumn[0]
    elif all(el == rightColumn[0] for el in rightColumn):
        winner = rightColumn[0]
    return winner

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    isTerminal = False
    if winner(board) or (EMPTY not in board[0] and EMPTY not in board[1] and EMPTY not in board[2]):
        isTerminal = True
    return isTerminal

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    possibleWinner = winner(board)

    if possibleWinner == X:
        boardUtility = 1
    elif possibleWinner == O:
        boardUtility = -1
    else:
        boardUtility = 0
    return boardUtility


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    currPlayer = player(board)
    possibleActions = actions(board)
    if currPlayer == X:
        u = float("-inf")
        for possibleAction in possibleActions:
            possibleActionUtility = min_value(result(board, possibleAction))
            if possibleActionUtility > u:
                u = possibleActionUtility
                actionToTake = possibleAction
    else:
        u = float("inf")
        for possibleAction in possibleActions:
            possibleActionUtility = max_value(result(board, possibleAction))
            if possibleActionUtility < u:
                u = possibleActionUtility
                actionToTake = possibleAction
    return actionToTake

def max_value(board):
    if terminal(board):
        return utility(board)
    possibleActions = actions(board)
    u = float("-inf")
    for possibleAction in possibleActions:
        u = max(u, min_value(result(board, possibleAction)))
    return u

def min_value(board):
    if terminal(board):
        return utility(board)
    possibleActions = actions(board)
    u = float("inf")
    for possibleAction in possibleActions:
        u = min(u, max_value(result(board, possibleAction)))
    return u
