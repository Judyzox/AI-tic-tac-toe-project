EMPTY = ""
PLAYER = "X"
AI = "O"

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

def greedy_best_first(board, maximizing_player):
    best_move = None
    best_score = float('-inf') if maximizing_player else float('inf')

    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                board[row][col] = AI if maximizing_player else PLAYER

                score = evaluate_board(board)

                board[row][col] = EMPTY

                if (maximizing_player and score > best_score) or (not maximizing_player and score < best_score):
                    best_score = score
                    best_move = (row, col)

    return best_score, best_move
