"""
Tic Tac Toe Player
"""

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
    count_x = 0
    count_o = 0

    for row in board:
        for column in row:

            if column == X:
                count_x += 1

            elif column == O:
                count_o += 1

    if count_x > count_o:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions
            
    
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid action")
    
    temp_board = [row[:] for row in board]

    temp_board[action[0]][action[1]] = player(board)
    
    return temp_board



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row == [X, X, X]:
            return X
        elif row == [O, O, O]:
            return O
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == X:
            return X
        elif board[0][col] == board[1][col] == board[2][col] == O:
            return O
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == X or board[0][2] == board[1][1] == board[2][0] == X:
        return X
    elif board[0][0] == board[1][1] == board[2][2] == O or board[0][2] == board[1][1] == board[2][0] == O:
        return O
    
    # No winner
    return None
                
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or all(cell != EMPTY for row in board for cell in row):
        return True
    else:
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


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    best_action = None
    best_score = -math.inf if player(board) == X else math.inf

    for action in actions(board):
        if player(board) == X:
            score = utility(result(board, action))
            if score > best_score:
                best_score = score
                best_action = action
        else:
            score = utility(result(board, action))
            if score < best_score:
                best_score = score
                best_action = action

    return best_action
