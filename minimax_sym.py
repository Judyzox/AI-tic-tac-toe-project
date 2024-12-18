from Utility import check_winner, is_draw

EMPTY = ""
PLAYER = "X"
AI = "O"

# Cache for previously evaluated board states
cached_results = {}


def rotate_90(board):
    """Rotate the board 90 degrees clockwise."""
    return [[board[2 - j][i] for j in range(3)] for i in range(3)]


def reflect_horizontal(board):
    """Reflect the board horizontally."""
    return [row[::-1] for row in board]


def reflect_vertical(board):
    """Reflect the board vertically."""
    return board[::-1]


def generate_symmetries(board):
    """Generate all symmetries (rotations and reflections) of the board."""
    symmetries = []
    current = board

    for _ in range(4):  # 4 rotations
        current = rotate_90(current)
        symmetries.append(current)
        symmetries.append(reflect_horizontal(current))
        symmetries.append(reflect_vertical(current))
        symmetries.append(reflect_horizontal(reflect_vertical(current)))

    # Remove duplicates by converting to a set of tuples (for immutability)
    unique_symmetries = set(tuple(tuple(row) for row in b) for b in symmetries)
    return [list(map(list, sym)) for sym in unique_symmetries]


def canonical_form(board):
    """Find the canonical form of the board by comparing all symmetries."""
    symmetries = generate_symmetries(board)
    return min(symmetries, key=lambda x: str(x))  # Pick the lexicographically smallest representation


def minimax_sym(board, depth, is_maximizing, cache=None):
    """Minimax with symmetry optimization and caching."""
    if cache is None:
        cache = {}

    # Get the canonical form of the board
    board_canonical = tuple(tuple(row) for row in canonical_form(board))

    # If the state has already been evaluated, return the cached result
    if board_canonical in cache:
        return cache[board_canonical]

    # Check for terminal states
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
