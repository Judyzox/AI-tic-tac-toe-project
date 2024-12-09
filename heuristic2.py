EMPTY = ""
PLAYER = "X"
AI = "O"

def evaluate_board(board):
    """
    Evaluate the board state with a more intelligent heuristic:
    - Positive values for AI's potential winning moves.
    - Negative values for Player's potential winning moves.
    - Zero for neutral positions.
    """
    score = 0

    # Check rows, columns, and diagonals
    for i in range(3):
        # Evaluate rows
        row = board[i]
        score += evaluate_line(row, AI, PLAYER)

        # Evaluate columns
        col = [board[j][i] for j in range(3)]
        score += evaluate_line(col, AI, PLAYER)

    # Evaluate diagonals
    diag1 = [board[i][i] for i in range(3)]
    score += evaluate_line(diag1, AI, PLAYER)
    diag2 = [board[i][2 - i] for i in range(3)]
    score += evaluate_line(diag2, AI, PLAYER)

    return score

def evaluate_line(line, ai_symbol, player_symbol):
    score = 0
    if line.count(ai_symbol) == 2 and line.count(EMPTY) == 1:
        score += 10
    elif line.count(player_symbol) == 2 and line.count(EMPTY) == 1:
        score -= 10
    elif line.count(ai_symbol) == 1 and line.count(EMPTY) == 2:
        score += 1
    elif line.count(player_symbol) == 1 and line.count(EMPTY) == 2:
        score -= 1
    return score

def hill_climbing(board, maximizing_player):
    current_board = [row[:] for row in board]
    best_score = float('-inf') if maximizing_player else float('inf')
    best_move = None

    possible_moves = [(row, col) for row in range(3) for col in range(3) if current_board[row][col] == EMPTY]

    for move in possible_moves:
        row, col = move

        current_board[row][col] = AI if maximizing_player else PLAYER

        score = evaluate_board(current_board)

        current_board[row][col] = EMPTY

        if (maximizing_player and score > best_score) or (not maximizing_player and score < best_score):
            best_score = score
            best_move = move

    # Return the best score and best move found
    return best_score, best_move
