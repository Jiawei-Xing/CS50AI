"""
Tic Tac Toe Player
"""

import math, copy

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
    x = 0
    o = 0
    for row in board:
        x += row.count(X)
        o += row.count(O)
        
    if x > o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    empties = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                empties.append((i, j))
    
    return empties


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise NameError('Invalid action')
    
    cpboard = copy.deepcopy(board)
    cpboard[action[0]][action[1]] = player(board)
    return cpboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # row
    for row in board:
        if row == [X] * 3:
            return X
        elif row == [O] * 3:
            return O
    
    # vertical
    for i in range(3):
        if board[0][i] == X and board[1][i] == X and board[2][i] == X:
            return X
        elif board[0][i] == O and board[1][i] == O and board[2][i] == O:
            return O
            
    # diagnol
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    elif board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    elif board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
    elif board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O
    
    # no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # win
    if winner(board):
        return True
    
    # tie
    empty = 0
    for row in board:
        empty += row.count(EMPTY)
    if empty == 0:
        return True
        
    # in progress
    return False


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


def max_value(board):
    v = -5
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
        if v == 1:
            break
    return v
    
    
def min_value(board):
    v = 5
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
        if v == -1:
            break
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
            
    if player(board) == X:
        for action in actions(board):
            if min_value(result(board, action)) == max_value(board):
                return action
        
    if player(board) == O:
        for action in actions(board):
            if max_value(result(board, action)) == min_value(board):
                return action