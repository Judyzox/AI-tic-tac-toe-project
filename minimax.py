from Utility import check_winner, is_draw

EMPTY = ""
PLAYER = "X"
AI = "O"


# def minimax(board, depth, is_maximizing):
#     """
#     Basic Minimax algorithm for Tic-Tac-Toe without symmetry reduction.
#     """
#     if check_winner(board, AI):
#         return 10 - depth, None
#     if check_winner(board, PLAYER):
#         return depth - 10, None
#     if is_draw(board):
#         return 0, None
#
#     best_move = None
#
#     if is_maximizing:
#         max_eval = float("-inf")
#         for row in range(3):
#             for col in range(3):
#                 if board[row][col] == EMPTY:
#                     board[row][col] = AI
#                     evaluation, _ = minimax(board, depth + 1, False)
#                     board[row][col] = EMPTY
#                     if evaluation > max_eval:
#                         max_eval = evaluation
#                         best_move = (row, col)
#         return max_eval, best_move
#     else:
#         min_eval = float("inf")
#         for row in range(3):
#             for col in range(3):
#                 if board[row][col] == EMPTY:
#                     board[row][col] = PLAYER
#                     evaluation, _ = minimax(board, depth + 1, True)
#                     board[row][col] = EMPTY
#                     if evaluation < min_eval:
#                         min_eval = evaluation
#                         best_move = (row, col)
#         return min_eval, best_move


def evaluate_board(board):
    """
    Heuristic evaluation function to score the board.
    Positive score favors AI, negative score favors PLAYER.
    """
    if check_winner(board, AI):
        return 10
    if check_winner(board, PLAYER):
        return -10
    return 0

def minimax(board, depth, is_maximizing):
    """
    Minimax algorithm with heuristic reduction.
    """
    score = evaluate_board(board)
    if score != 0 or is_draw(board):
        return score - depth if score > 0 else score + depth, None

    best_move = None

    if is_maximizing:
        max_eval = float("-inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = AI
                    evaluation, _ = minimax(board, depth + 1, False)
                    board[row][col] = EMPTY
                    if evaluation > max_eval:
                        max_eval = evaluation
                        best_move = (row, col)
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER
                    evaluation, _ = minimax(board, depth + 1, True)
                    board[row][col] = EMPTY
                    if evaluation < min_eval:
                        min_eval = evaluation
                        best_move = (row, col)
        return min_eval, best_move
