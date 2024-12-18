import tkinter as tk
from tkinter import ttk
from gui import TicTacToe

selected_algorithm = None

def on_alg_button_click(algorithm):
    """
    Function called when an algorithm button is clicked.
    It sets the selected algorithm and launches the game.
    """
    global selected_algorithm
    selected_algorithm = algorithm
    root.destroy()  
    game = TicTacToe(algorithm=selected_algorithm)
    game.run()

def create_algorithm_selection_window():
    """
    Function to create the algorithm selection window.
    """
    global root
    root = tk.Tk()
    root.title("Tic-Tac-Toe AI Selector")
    root.geometry("300x500")
    root.configure(bg="#ffe6f2")

    frame = tk.Frame(root, bg="#ffe6f2")
    frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Create a label for instructions
    label = tk.Label(
        frame,
        text="Choose an algorithm to solve \nthe Tic-Tac-Toe problem",
        font=("Helvetica", 14, "bold"),
        bg="#ffe6f2",
        fg="#cc0052"
    )
    label.pack(pady=20)

    style = ttk.Style()
    style.configure(
        "TButton",
        font=("Helvetica", 12),
        padding=5,
        relief="flat",
        background="#ff80bf",
        foreground="pink"
    )
    style.map(
        "TButton",
        background=[('pressed', '#cc0052'), ('active', '#ff4d94')],
        foreground=[('pressed', 'white'), ('active', 'white')]
    )

    alg_buttons = [
        ("MiniMax", "minimax"),
        ("MiniMax Alpha Beta", "alpha_beta"),
        ("MiniMax First Heuristic", "heuristic"),
        ("MiniMax Second Heuristic", "heuristic2"),
        ("MiniMax Symmetry", "minimax_symmetry"),
        ("AlphaBeta Symmetry", "alphabeta_symmetry"),
        ("first heuristic Symmetry", "heuristic1_sym"),
        ("Second heuristic Symmetry", "heuristic2_sym")
    ]

    for alg_name, alg_value in alg_buttons:
        button = ttk.Button(frame, text=alg_name, command=lambda alg=alg_value: on_alg_button_click(alg))
        button.pack(pady=5, fill=tk.X, padx=10)

    root.mainloop()

if __name__ == "__main__":
    create_algorithm_selection_window()

