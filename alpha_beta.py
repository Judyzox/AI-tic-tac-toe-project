from Utility import check_winner, is_draw

EMPTY = ""
PLAYER = "X"
AI = "O"

# def alpha_beta(board, depth, alpha, beta, is_maximizing):
#     """
#     Minimax algorithm with Alpha-Beta Pruning for Tic-Tac-Toe (without symmetry reduction).
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
#                     evaluation, _ = alpha_beta(board, depth + 1, alpha, beta, False)
#                     board[row][col] = EMPTY
#                     if evaluation > max_eval:
#                         max_eval = evaluation
#                         best_move = (row, col)
#                     alpha = max(alpha, evaluation)
#                     if beta <= alpha:
#                         break
#         return max_eval, best_move
#     else:
#         min_eval = float("inf")
#         for row in range(3):
#             for col in range(3):
#                 if board[row][col] == EMPTY:
#                     board[row][col] = PLAYER
#                     evaluation, _ = alpha_beta(board, depth + 1, alpha, beta, True)
#                     board[row][col] = EMPTY
#                     if evaluation < min_eval:
#                         min_eval = evaluation
#                         best_move = (row, col)
#                     beta = min(beta, evaluation)
#                     if beta <= alpha:
#                         break
#         return min_eval, best_move


# Predefined move order for heuristic reduction (center, corners, edges).
MOVE_ORDER = [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2), (0, 1), (1, 0), (1, 2), (2, 1)]

def alpha_beta (board, depth, alpha, beta, is_maximizing):
    """
    Minimax algorithm with Alpha-Beta Pruning and heuristic reduction for Tic-Tac-Toe.
    """
    # Terminal conditions
    if check_winner(board, AI):
        return 10 - depth, None
    if check_winner(board, PLAYER):
        return depth - 10, None
    if is_draw(board):
        return 0, None
    best_move = None

    if is_maximizing:
        max_eval = float("-inf")
        for row, col in MOVE_ORDER:
            if board[row][col] == EMPTY:
                board[row][col] = AI
                evaluation, _ = alpha_beta(board, depth + 1, alpha, beta, False)
                board[row][col] = EMPTY
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = (row, col)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for row, col in MOVE_ORDER:
            if board[row][col] == EMPTY:
                board[row][col] = PLAYER
                evaluation, _ = alpha_beta(board, depth + 1, alpha, beta, True)
                board[row][col] = EMPTY
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = (row, col)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
        return min_eval, best_move
