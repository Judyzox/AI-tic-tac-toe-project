EMPTY = ""
PLAYER = "X"
AI = "O"

def check_winner(board, player):
    # Check rows, columns, and diagonals for a winner
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw(board):
    # Check if the board is full and no winner
    return all(board[i][j] != EMPTY for i in range(3) for j in range(3)) and \
           not check_winner(board, PLAYER) and not check_winner(board, AI)

def alpha_beta(board, depth, alpha, beta, is_maximizing):
    """
    Minimax algorithm with Alpha-Beta Pruning for Tic-Tac-Toe (without symmetry reduction).
    """
    if check_winner(board, AI):
        return 10 - depth, None
    if check_winner(board, PLAYER):
        return depth - 10, None
    if is_draw(board):
        return 0, None

    best_move = None

    if is_maximizing:
        max_eval = float("-inf")
        for row in range(3):
            for col in range(3):
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
        for row in range(3):
            for col in range(3):
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
