"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy 

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

    xs = os = 0
    for row in board:
        for col in row:
            if col == 'X':
                xs += 1
            elif col == 'O':
                os += 1

    if xs + os == 9:
        return None
    elif xs <= os:
        return 'X'
    else:
        return 'O'

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    moves = set()
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    if len(moves) == 0:
        return None
    
    return moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    boardCopy = deepcopy(board)
    if action[0] < 0 or action[1] < 0 or boardCopy[action[0]][action[1]] != EMPTY:
        raise NameError("Invalid action")
    else:
        boardCopy[action[0]][action[1]] = player(board)
    
    return boardCopy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for player in ('X', 'O'):
        for row in board:
            if row == [player]*3:
                return player
            
        for i in range(3):
            column = [board[x][i] for x in range(3)]
            if column == [player] * 3:
                return player
                        
    prinDiag = [0, 0]
    secndDiag = [0, 0]
    for i in range(0, 3):

        if board[i][i] == 'X':
            prinDiag[0] += 1
        elif board[i][i] == 'O':
            prinDiag[1] += 1

        if board[i][2-i] == 'X':
            secndDiag[0] += 1
        elif board[i][2-i] == 'O':
            secndDiag[1] += 1

    if prinDiag[0] == 3 or secndDiag[0] == 3:
        return 'X'
    elif prinDiag[1] == 3 or secndDiag[1] == 3:
        return 'O'  
    else:
        return None   

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    if winner(board) != None or actions(board) == None:
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    winner_player = winner(board)

    if winner_player == 'X':
        return 1
    elif winner_player == 'O':
        return -1
    else:
        return 0

def max_value(board):
    if terminal(board):
        return utility(board)
    else:
        v = -math.inf

        for action in actions(board):
            v = max(v, min_value(result(board, action)))

        return v
            
def min_value(board):
    if terminal(board):
        return utility(board)
    else:
        v = math.inf

        for action in actions(board):
            v = min(v, max_value(result(board, action)))

        return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board) or winner(board) != None:
        return None

    best_action = tuple()
    
    if player(board) == 'X':
        maxv = -math.inf
        for action in actions(board):
            adversary = min_value(result(board, action)) 

            if adversary > maxv:
                best_action = action
                maxv = adversary
    elif player(board) == 'O':
        minv = math.inf
        for action in actions(board):
            adversary = max_value(result(board, action)) 

            if adversary < minv:
                best_action = action
                minv = adversary

    return best_action 
