import numpy as np

# Board size constants
BOARD_ROWS = 3
BOARD_COLUMNS = 3

# Memoization dictionary
memo = {}

def check_win(player, board):
    """Check if a player has won the game."""
    for column in range(BOARD_COLUMNS):
        if board[0][column] == player and board[1][column] == player and board[2][column] == player:
            return True

    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False

def is_board_full(board):
    """Check if the board is full."""
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            if board[row][column] == 0:
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

def minimax_alpha_beta(board, depth, is_maximizing, alpha, beta):
    """Minimax algorithm with alpha-beta pruning and symmetry reduction."""
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

    if is_maximizing:
        best_score = float('-inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax_alpha_beta(board, depth + 1, False, alpha, beta)
                    board[row][col] = 0
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        # Memoize the result for the canonical form
        memo[canonical_board] = best_score
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = minimax_alpha_beta(board, depth + 1, True, alpha, beta)
                    board[row][col] = 0
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        # Memoize the result for the canonical form
        memo[canonical_board] = best_score
        return best_score

def mark_square(board, row, column, player):
    """Mark a square on the board with the given player's mark."""
    board[row][column] = player

def available_square(board, row, column):
    """Check if a square is available."""
    return board[row][column] == 0

def best_move(board, algorithm):
    """Determine the best move using the selected algorithm."""
    best_score = float('-inf')
    move = (-1, -1)

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == 0:
                mark_square(board, row, col, 2)
                if algorithm == "minimax_alpha_beta":
                    score = minimax_alpha_beta(board, 0, False, float('-inf'), float('inf'))
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(board, move[0], move[1], 2)
        return True
    return False


if __name__ == "__main__":
board = np.zeros((BOARD_ROWS, BOARD_COLUMNS))
    
    game_over = False
    player = 1  # Player 1 starts

    while not game_over:
        # Player makes a move
        if player == 1:
            row, col = map(int, input("Enter row and column (0-2) for Player 1: ").split())
            if available_square(board, row, col):
                mark_square(board, row, col, 1)
                if check_win(1, board):
                    print("Player 1 wins!")
                    game_over = True
            else:
                print("Square already occupied. Try again.")
        else:
            print("AI is making a move...")
            if best_move(board, "minimax_alpha_beta"):
                if check_win(2, board):
                    print("AI wins!")
                    game_over = True

        if not game_over and is_board_full(board):
            print("The game is a draw!")
            game_over = True

        player = 3 - player  # Switch between player 1 and 2

        # Print the board state
        print(board)
