from Utility import evaluate_board, canonical_form

EMPTY = ""
PLAYER = "X"
AI = "O"

cached_results = {}
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