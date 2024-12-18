import tkinter as tk
import time
import threading
import csv
import os
from minimax import minimax
from alpha_beta import alpha_beta
from minimax_sym import minimax_sym
from alpha_beta_sym import alpha_beta_sym
from heuristic import greedy_best_first
from heuristic2 import hill_climbing
from heuristic1_sym import greedy_best_first
from heuristic2_sym import hill_climbing
from datetime import datetime

# Constants for the game
EMPTY = ""
PLAYER = "X"
AI = "O"


class TicTacToe:
    def __init__(self, algorithm="minimax"):
        self.algorithm = algorithm  # Selected AI algorithm
        self.board = [[EMPTY] * 3 for _ in range(3)]
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.times = []  # Store time taken for each AI move
        self.csv_file = self.generate_unique_filename(algorithm)
        self.game_state = "In Progress"  # Track the state of the game

        self.create_game_board()

    def generate_unique_filename(self, algorithm):
        """
        Generate a unique CSV filename based on the algorithm and timestamp.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{algorithm}_averages_{timestamp}.csv"
        counter = 1

        while os.path.exists(filename):
            filename = f"{algorithm}_averages_{timestamp}_{counter}.csv"
            counter += 1

        return filename

    def create_game_board(self):
        """
        Initialize the game board GUI elements.
        """
        self.board_frame = tk.Frame(self.window, bg="pink")
        self.board_frame.pack(fill="both", expand=True)

        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Helvetica", 28),
                    height=3,
                    width=7,
                    bg="lightpink",
                    command=lambda row=i, col=j: self.player_move(row, col),
                )
                button.grid(row=i, column=j, padx=10, pady=10)
                self.buttons[i][j] = button

        self.result_label = tk.Label(
            self.board_frame,
            text="",
            font=("Helvetica", 18),
            bg="pink",
            fg="deeppink",
        )
        self.result_label.grid(row=3, column=0, columnspan=3, pady=20)

        self.algorithm_label = tk.Label(
            self.board_frame,
            text="AI Algorithm:",
            font=("Helvetica", 14),
            bg="pink"
        )
        self.algorithm_label.grid(row=4, column=0, padx=10, sticky="w")

        self.algorithm_dropdown = tk.StringVar(self.window)
        self.algorithm_dropdown.set(self.algorithm)
        self.dropdown_menu = tk.OptionMenu(
            self.board_frame,
            self.algorithm_dropdown,
            "minimax",
            "alpha_beta",
            "minimax-symmetry",
            "alpha-beta-symmetry",
            "heuristic",
            "heuristic2",
            "heuristic1_sym",
            "heuristic2_sym",
            command=self.set_algorithm
        )
        self.dropdown_menu.config(font=("Helvetica", 14), bg="lightpink")
        self.dropdown_menu.grid(row=4, column=1, columnspan=2, sticky="ew")

        self.restart_button = tk.Button(
            self.board_frame,
            text="Restart",
            font=("Helvetica", 14),
            command=self.restart_game,
            bg="pink",
        )
        self.restart_button.grid(row=5, column=0, sticky="ew")

        self.stop_button = tk.Button(
            self.board_frame,
            text="Stop",
            font=("Helvetica", 14),
            command=self.window.quit,
            bg="pink",
        )
        self.stop_button.grid(row=5, column=2, sticky="ew")

        self.time_label = tk.Label(
            self.board_frame,
            text="Algorithm Time: 0s",
            font=("Helvetica", 14),
            bg="pink"
        )
        self.time_label.grid(row=6, column=0, columnspan=3, pady=10)

    def set_algorithm(self, _):
        self.algorithm = self.algorithm_dropdown.get()
        self.csv_file = self.generate_unique_filename(self.algorithm)

    def player_move(self, row, col):
        if self.game_over or self.board[row][col] != EMPTY:
            return

        self.board[row][col] = PLAYER
        self.buttons[row][col].config(text=PLAYER, state=tk.DISABLED, fg="deeppink")

        if self.check_winner(PLAYER):
            self.display_message("You win!")
            self.game_over = True
            self.game_state = "Win"
            return

        if self.is_draw():
            self.display_message("It's a draw!")
            self.game_over = True
            self.game_state = "Draw"
            return

        threading.Thread(target=self.ai_move).start()

    def ai_move(self):
        if self.game_over:
            return

        start_time = time.time()
        move = None  # Initialize `move` to avoid UnboundLocalError

        if self.algorithm == "minimax":
            _, move = minimax(self.board, 0, True)
        elif self.algorithm == "alpha_beta":
            _, move = alpha_beta(self.board, 0, float("-inf"), float("inf"), True)
        elif self.algorithm == "minimax_symmetry":
            _, move = minimax_sym(self.board, 0, True)
        elif self.algorithm == "alphabeta_symmetry":
            _, move = alpha_beta_sym(self.board, 0, float("-inf"), float("inf"), True)
        elif self.algorithm == "heuristic":
            _, move = greedy_best_first(self.board, True)
        elif self.algorithm == "heuristic2":
            _, move = hill_climbing(self.board, True)
        elif self.algorithm == "heuristic1_sym":
            _, move = greedy_best_first(self.board, True)
        elif self.algorithm == "heuristic2_sym":
            _, move = hill_climbing(self.board, True)
        else:
            print(f"Error: Unsupported algorithm '{self.algorithm}'")
            return  # Exit the function early

        elapsed_time = round(time.time() - start_time, 4)
        self.window.after(0, lambda: self.time_label.config(text=f"Algorithm Time: {elapsed_time}s"))
        self.times.append(elapsed_time)

        if move:
            row, col = move
            self.board[row][col] = AI
            self.window.after(0, lambda: self.buttons[row][col].config(text=AI, state=tk.DISABLED, fg="blue"))

            if self.check_winner(AI):
                self.window.after(0, lambda: self.display_message("AI wins!"))
                self.game_over = True
                self.game_state = "Lose"
            elif self.is_draw():
                self.window.after(0, lambda: self.display_message("It's a draw!"))
                self.game_over = True
                self.game_state = "Draw"

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        return all(self.board[i][i] == player for i in range(3)) or \
               all(self.board[i][2 - i] == player for i in range(3))

    def is_draw(self):
        return all(self.board[i][j] != EMPTY for i in range(3) for j in range(3))

    def display_message(self, message):
        self.result_label.config(text=message)

    def restart_game(self):
        avg_time = self.calculate_average_time()
        self.log_to_csv(avg_time)

        self.board = [[EMPTY] * 3 for _ in range(3)]
        self.game_over = False
        self.result_label.config(text="")
        self.times = []
        self.game_state = "In Progress"
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state=tk.NORMAL)

    def calculate_average_time(self):
        return round(sum(self.times) / len(self.times), 4) if self.times else 0

    def log_to_csv(self, avg_time):
        try:
            with open(self.csv_file, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([self.algorithm, avg_time, self.game_state])
        except PermissionError:
            print("PermissionError: Unable to write to the CSV file.")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()

