from Utility import evaluate_board

EMPTY = ""
PLAYER = "X"
AI = "O"

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
