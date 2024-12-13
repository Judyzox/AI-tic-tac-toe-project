import numpy as np

# Proportions & Sizes
BOARD_ROWS = 3
BOARD_COLUMNS = 3

# Memoization dictionary
memo = {}

def minimax(board, depth, is_maximizing):
    """Minimax algorithm with symmetry reduction."""
    # Get the canonical form of the board
    canonical_board = canonical_form(board).tobytes()  # Convert to bytes for hashing

    # Check if this board state has been evaluated before
    if canonical_board in memo:
        return memo[canonical_board]

    # Check terminal states
    if check_win(2, board):
        return float('inf')
    if check_win(1, board):
        return float('-inf')
    if is_board_full(board):
        return 0

    best_score = float('-inf') if is_maximizing else float('inf')
    
    # Iterate over all possible moves
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == 0:
                board[row][col] = 2 if is_maximizing else 1
                score = minimax(board, depth + 1, not is_maximizing)
                board[row][col] = 0
                if is_maximizing:
                    best_score = max(score, best_score)
                else:
                    best_score = min(score, best_score)
    
    # Memoize the result for the canonical form
    memo[canonical_board] = best_score
    return best_score

def check_win(player, check_board):
    """Check if a player has won."""
    for column in range(BOARD_COLUMNS):
        if check_board[0][column] == player and check_board[1][column] == player and check_board[2][column] == player:
            return True
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    return False

def is_board_full(check_board):
    """Check if the board is full."""
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            if check_board[row][column] == 0:
                return False
    return True

def canonical_form(board):
    """Generate the canonical form of the board considering all symmetries."""
    transformations = [
        lambda b: b,  # Original
        lambda b: np.rot90(b),  # 90 degree rotation
        lambda b: np.rot90(b, 2),  # 180 degree rotation
        lambda b: np.rot90(b, 3),  # 270 degree rotation
        lambda b: np.fliplr(b),  # Horizontal flip
        lambda b: np.flipud(b),  # Vertical flip
        lambda b: np.fliplr(np.rot90(b)),  # Horizontal flip and 90 degree rotation
        lambda b: np.flipud(np.rot90(b)),  # Vertical flip and 90 degree rotation
    ]
    
    min_board = board
    for transform in transformations:
        transformed_board = transform(board)
        if np.lexsort(transformed_board.flatten()) < np.lexsort(min_board.flatten()):
            min_board = transformed_board
    return min_board

def best_move(algorithm, board):
    """Determine the best move using a basic heuristic."""
    best_score = float('-inf')
    move = (-1, -1)

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == 0:
                board[row][col] = 2
                if algorithm == "minimax":
                    score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], 2, board)
        return True
    return False

def mark_square(row, column, player, board):
    """Mark a square on the board."""
    board[row][column] = player

# Main game loop
if __name__ == "__main__":
    board = np.zeros((3, 3))
    player = 1
    game_over = False

    while not game_over:
        if player == 1:  # Player's turn
            row, col = map(int, input("Enter row and column (0-2): ").split())
            if board[row][col] == 0:
                mark_square(row, col, player, board)
                if check_win(player, board):
                    print(f"Player {player} wins!")
                    game_over = True
                player = 2
        else:  # AI's turn
            best_move("minimax", board)
            if check_win(2, board):
                print(f"Player {player} wins!")
                game_over = True
            player = 1

        # Print board
        print(board)
