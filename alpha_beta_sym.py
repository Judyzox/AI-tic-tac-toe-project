from Utility import check_winner, is_draw, generate_symmetries

EMPTY = ""
PLAYER = "X"
AI = "O"
cached_results = {}

def alpha_beta_sym(board, depth, alpha, beta, is_maximizing):
    """
    Minimax algorithm with Alpha-Beta Pruning for Tic-Tac-Toe and symmetry reduction.
    """
    # Convert the board to a tuple for hashing in cache (to store board configurations)
    board_tuple = tuple(tuple(row) for row in board)

    # Check cache for precomputed results for this symmetry
    if board_tuple in cached_results:
        return cached_results[board_tuple]

    # Evaluate terminal states
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
                    # Simulate the AI move (O) only in empty spots
                    board[row][col] = AI
                    evaluation, _ = alpha_beta_sym(board, depth + 1, alpha, beta, False)
                    board[row][col] = EMPTY
                    if evaluation > max_eval:
                        max_eval = evaluation
                        best_move = (row, col)
                    alpha = max(alpha, evaluation)
                    if beta <= alpha:
                        break
        result = max_eval, best_move
    else:
        min_eval = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    # Simulate the player move (X) only in empty spots
                    board[row][col] = PLAYER
                    evaluation, _ = alpha_beta_sym(board, depth + 1, alpha, beta, True)
                    board[row][col] = EMPTY
                    if evaluation < min_eval:
                        min_eval = evaluation
                        best_move = (row, col)
                    beta = min(beta, evaluation)
                    if beta <= alpha:
                        break
        result = min_eval, best_move

    # Cache the result for the board and all its symmetric forms
    symmetries = generate_symmetries(board)
    for sym_board in symmetries:
        sym_board_tuple = tuple(tuple(row) for row in sym_board)
        cached_results[sym_board_tuple] = result

    return result
