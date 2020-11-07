"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np

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

    turn = 0

    # Counts turns based on characters in the board.
    for row in board:
        for cell in row:
            if cell is not None:
                turn += 1

    
    if turn % 2 == 0:
        return 'X'
    elif turn % 2 == 1:
        return 'O'
    else:
        return None
    
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    posibility = set() # will contain all posible actions.

    # Iterates through board looking for non-empty cells.
    for row in range(len(board)):
        for column in range(len(board)):
            if board[row][column] is None:
                posibility.add((row, column))

    if len(posibility) == 0:
        return None
    else:
        return posibility

    raise NotImplementedError
    

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Raises exeption for invalid actions when board cell is alredy filled or when action
    # has valoes that are not in the range [0, 2].
    if board[action[0]][action[1]] is not None:
        raise ValueError("action is not valid")

    for i in range(len(action)):
        if action[i] > 2 or action[i] < 0:
            raise ValueError("action is not valid")

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for plyr in ['X', 'O']:
        lst = [0, 1, 2]

        # horizontal win.
        for row in lst:
            if board[row][0] == plyr and board[row][1] == plyr and board[row][2] == plyr:
                return plyr

        # Vertical win.
        for column in lst:
            if board[0][column] == plyr and board[1][column] == plyr and board[2][column] == plyr:
                return plyr

        #Diagonal win.
        if board[0][2] == plyr and board[1][1] == plyr and board[2][0] == plyr:
            return plyr
        if board[0][0] == plyr and board[1][1] == plyr and board[2][2] == plyr:
            return plyr

    return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None:
        return True

    #Iterates through 
    for row in board:
        for cell in row:
            if cell is None:
                return False
    
    return True

    raise NotImplementedError

    
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == 'X':
        return 1
    elif winner(board) == 'O':
        return -1
    else:
        return 0

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    lst = {"action": [], "output": []}
    alpha = -np.inf
    beta = np.inf

    
    if player(board) =='X':
        optimal = [-np.inf, ()]
        
        for move in actions(board):
            lst["action"].append(move)
            lst["output"].append(min_value(result(board, move), alpha, beta))

        for i in range(len(lst["output"])):
            if lst["output"][i] > optimal[0]:
                optimal[0] = lst["output"][i]
                optimal[1] = lst["action"][i]

        return optimal[1]
    else:
        optimal = [np.inf, ()]
        for move in actions(board):
            lst["action"].append(move)
            lst["output"].append(max_value(result(board, move), alpha, beta))

        for i in range(len(lst["output"])):
            if lst["output"][i] < optimal[0]:
                optimal[0] = lst["output"][i]
                optimal[1] = lst["action"][i]

        return optimal[1]
    

    raise NotImplementedError


def max_value(board, alpha,beta):
    """
    Returns the highest posible board value from all the posible actions.
    """
    if terminal(board):
        return utility(board)
    
    value = -np.inf

    for move in actions(board):
        new_value = min_value(result(board, move), alpha, beta)
        value = max(value, new_value)
        alpha = max(alpha, new_value)
        if beta <= alpha:
            break

    return value


def min_value(board, alpha, beta):
    """
    Returns the lowest posible board value from all the posible actions.
    """
    
    if terminal(board):
        return utility(board)
    
    value = np.inf

    for move in actions(board):
        new_value = max_value(result(board, move), alpha, beta)
        value = min(value, max_value(result(board, move), alpha, beta))
        beta = min(beta, new_value)
        if beta <= alpha:
            break

    return value


def min(value, new_value):
    """
    Returns the lowest value between the arguments.
    """
    if new_value < value:
        return new_value
    
    return value

def max(value, new_value):
    """
    Returns the highest value between the arguments.
    """
    if new_value > value:
        return new_value
    
    return value