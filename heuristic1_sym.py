EMPTY = ""
PLAYER = "X"
AI = "O"

def evaluate_board(board):
    score = 0
    for i in range(3):
        # Evaluate rows
        row = board[i]
        score += evaluate_line(row)

        # Evaluate columns
        col = [board[j][i] for j in range(3)]
        score += evaluate_line(col)

    # Evaluate diagonals
    diag1 = [board[i][i] for i in range(3)]
    score += evaluate_line(diag1)
    diag2 = [board[i][2 - i] for i in range(3)]
    score += evaluate_line(diag2)

    return score

def evaluate_line(line):
    score = 0
    if line.count(AI) == 2 and line.count(EMPTY) == 1:
        score += 10
    elif line.count(PLAYER) == 2 and line.count(EMPTY) == 1:
        score -= 10
    elif line.count(AI) == 1 and line.count(EMPTY) == 2:
        score += 1
    elif line.count(PLAYER) == 1 and line.count(EMPTY) == 2:
        score -= 1
    return score

def transform_board(board, transform):
    """Apply a transformation (rotation or reflection) to the board."""
    if transform == "rotate_90":
        return [[board[2 - j][i] for j in range(3)] for i in range(3)]
    elif transform == "rotate_180":
        return [[board[2 - i][2 - j] for j in range(3)] for i in range(3)]
    elif transform == "rotate_270":
        return [[board[j][2 - i] for j in range(3)] for i in range(3)]
    elif transform == "reflect_horizontal":
        return [[board[i][2 - j] for j in range(3)] for i in range(3)]
    elif transform == "reflect_vertical":
        return [[board[2 - i][j] for j in range(3)] for i in range(3)]
    return board

def canonical_form(board):
    """Find the canonical form of a board by considering all symmetric equivalents."""
    transformations = [
        "rotate_90",
        "rotate_180",
        "rotate_270",
        "reflect_horizontal",
        "reflect_vertical",
    ]
    canonical = board
    for transform in transformations:
        transformed = transform_board(board, transform)
        if transformed < canonical:
            canonical = transformed
    return canonical

def greedy_best_first(board, maximizing_player):
    seen_boards = set()
    best_move = None
    best_score = float('-inf') if maximizing_player else float('inf')

    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                board[row][col] = AI if maximizing_player else PLAYER

                canonical = canonical_form(board)
                if tuple(map(tuple, canonical)) not in seen_boards:
                    seen_boards.add(tuple(map(tuple, canonical)))

                    score = evaluate_board(board)
                    if (maximizing_player and score > best_score) or (not maximizing_player and score < best_score):
                        best_score = score
                        best_move = (row, col)

                board[row][col] = EMPTY

    return best_score, best_move
