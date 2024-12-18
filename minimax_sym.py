from Utility import check_winner, is_draw, canonical_form

EMPTY = ""
PLAYER = "X"
AI = "O"

cached_results = {}

def minimax_sym(board, depth, is_maximizing, cache=None):
    """Minimax with symmetry optimization and caching."""
    if cache is None:
        cache = {}

    board_canonical = tuple(tuple(row) for row in canonical_form(board))

    if board_canonical in cache:
        return cache[board_canonical]

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
                    evaluation, _ = minimax_sym(board, depth + 1, False, cache)
                    board[row][col] = EMPTY
                    if evaluation > max_eval:
                        max_eval = evaluation
                        best_move = (row, col)
        cache[board_canonical] = (max_eval, best_move)
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER
                    evaluation, _ = minimax_sym(board, depth + 1, True, cache)
                    board[row][col] = EMPTY
                    if evaluation < min_eval:
                        min_eval = evaluation
                        best_move = (row, col)
        cache[board_canonical] = (min_eval, best_move)
        return min_eval, best_move
