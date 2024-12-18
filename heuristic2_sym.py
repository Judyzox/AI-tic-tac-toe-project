from Utility import evaluate_board, is_unique_board

EMPTY = ""
PLAYER = "X"
AI = "O"

cached_results = {}

def hill_climbing(board, maximizing_player):
    current_board = [row[:] for row in board]
    best_score = float('-inf') if maximizing_player else float('inf')
    best_move = None
    possible_moves = [(row, col) for row in range(3) for col in range(3) if current_board[row][col] == EMPTY]
    visited_boards = []

    for move in possible_moves:
        row, col = move
        current_board[row][col] = AI if maximizing_player else PLAYER

        if not is_unique_board(current_board, visited_boards):
            current_board[row][col] = EMPTY
            continue

        visited_boards.append([row[:] for row in current_board])

        score = evaluate_board(current_board)

        current_board[row][col] = EMPTY

        if (maximizing_player and score > best_score) or (not maximizing_player and score < best_score):
            best_score = score
            best_move = move

    return best_score, best_move