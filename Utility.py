EMPTY = ""
PLAYER = "X"
AI = "O"

cached_results = {}

def generate_symmetries(board):
    """Generate all symmetric variations of the board."""
    rotations = [board]  # Original board
    for _ in range(3):  # Rotate 90, 180, and 270 degrees
        rotations.append(rotate_board(rotations[-1]))
    mirrors = [mirror_board(b) for b in rotations]  # Mirror each rotation
    return set(tuple(tuple(row) for row in b) for b in rotations + mirrors)

def rotate_board(board):
    """Rotate the board 90 degrees clockwise."""
    return [[board[2 - col][row] for col in range(3)] for row in range(3)]

def mirror_board(board):
    """Mirror the board horizontally."""
    return [list(reversed(row)) for row in board]

def check_winner(board, player):
    """Check if a player has won the game."""
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(board[row][col] != EMPTY for row in range(3) for col in range(3))

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

def canonical_form(board):
    """Return the lexicographically smallest form of the board considering all symmetries."""
    symmetries = generate_symmetries(board)
    return min(symmetries)


def is_unique_board(board, visited_boards):
    """
    Check if a board is unique among all visited boards.
    """
    symmetries = generate_symmetries(board)
    for symmetry in symmetries:
        if symmetry in visited_boards:
            return False
    return True