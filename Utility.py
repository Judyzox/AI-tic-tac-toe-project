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

    # Check rows, columns, and diagonals
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
        score += 10  # AI has a line with two pieces, one empty
    elif line.count(PLAYER) == 2 and line.count(EMPTY) == 1:
        score -= 10  # Player has a line with two pieces, one empty
    elif line.count(AI) == 1 and line.count(EMPTY) == 2:
        score += 1  # AI has a single piece, two empty spots (weak advantage)
    elif line.count(PLAYER) == 1 and line.count(EMPTY) == 2:
        score -= 1  # Player has a single piece, two empty spots (weak disadvantage)
    return score


def generate_symmetries(board):
    """
    Generate all symmetries (rotations and reflections) of the board.
    """
    symmetries = []

    def rotate_90(board):
        return [[board[2 - i][j] for i in range(3)] for j in range(3)]

    def reflect_vertical(board):
        return [row[::-1] for row in board]

    # Original board
    symmetries.append(board)

    # Rotations
    rotated_90 = rotate_90(board)
    symmetries.append(rotated_90)

    rotated_180 = rotate_90(rotated_90)
    symmetries.append(rotated_180)

    rotated_270 = rotate_90(rotated_180)
    symmetries.append(rotated_270)

    # Reflections
    reflected = reflect_vertical(board)
    symmetries.append(reflected)

    # Reflections of rotations
    symmetries.append(reflect_vertical(rotated_90))
    symmetries.append(reflect_vertical(rotated_180))
    symmetries.append(reflect_vertical(rotated_270))

    return symmetries
