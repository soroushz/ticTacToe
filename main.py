import tkinter as tk
import random
import pygame

# Initialize pygame mixer for sound effects
pygame.mixer.init()

# Load sound files into a dictionary
sounds = {
    "move": pygame.mixer.Sound("sounds/move.mp3"),
    "win": pygame.mixer.Sound("sounds/win.wav"),
    "draw": pygame.mixer.Sound("sounds/draw.wav"),
}

# Theme configurations
themes = {
    "classic": {"bg": "#d3d3d3", "fg": "#333333"},
    "futuristic": {"bg": "#1a1a2e", "fg": "#16c79a"},
    "nature": {"bg": "#d4e157", "fg": "#3e2723"},
}


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = [""] * 9
        self.current_player = "X"
        self.scores = {"X": 0, "O": 0}
        self.theme = "classic"
        self.ai_mode = False
        self.ai_delay = 500  # AI delay in milliseconds
        self.create_widgets()
        self.create_menu()
        self.create_scoreboard()
        self.create_status_labels()

    def create_widgets(self):
        self.buttons = []
        for i in range(9):
            button = tk.Button(self.root, text="", font=('normal', 40), width=5, height=2,
                               command=lambda i=i: self.button_click(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        options_menu = tk.Menu(menu)
        menu.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Reset", command=self.reset_board)
        options_menu.add_command(label="Two Player Mode", command=self.two_player_mode)
        options_menu.add_command(label="AI Mode", command=self.ai_mode_toggle)

        theme_menu = tk.Menu(menu)
        menu.add_cascade(label="Themes", menu=theme_menu)
        for theme_name in themes.keys():
            theme_menu.add_command(label=theme_name.capitalize(), command=lambda t=theme_name: self.change_theme(t))

    def create_scoreboard(self):
        self.scoreboard = tk.Label(self.root, text=self.get_score_text(), font=('normal', 20))
        self.scoreboard.grid(row=3, columnspan=3)

    def create_status_labels(self):
        self.mode_label = tk.Label(self.root, text=self.get_mode_text(), font=('normal', 12))
        self.mode_label.grid(row=4, column=0, columnspan=1)
        self.theme_label = tk.Label(self.root, text=self.get_theme_text(), font=('normal', 12))
        self.theme_label.grid(row=4, column=2, columnspan=1)

    def get_score_text(self):
        return f"Player X: {self.scores['X']}  Player O: {self.scores['O']}"

    def get_mode_text(self):
        return "Mode: AI" if self.ai_mode else "Mode: Two Player"

    def get_theme_text(self):
        return f"Theme: {self.theme.capitalize()}"

    def update_status_labels(self):
        self.mode_label.config(text=self.get_mode_text())
        self.theme_label.config(text=self.get_theme_text())

    def change_theme(self, theme):
        self.theme = theme
        theme_config = themes[theme]
        for button in self.buttons:
            button.config(bg=theme_config["bg"], fg=theme_config["fg"])
        self.update_status_labels()

    def button_click(self, index):
        if not self.board[index]:
            self.board[index] = self.current_player
            self.update_button(index)
            if self.check_win(self.current_player):
                self.scores[self.current_player] += 1
                self.update_scoreboard()
                sounds["win"].play()
                self.reset_board()
            elif "" not in self.board:
                sounds["draw"].play()
                self.reset_board()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                sounds["move"].play()
                if self.ai_mode and self.current_player == "O":
                    self.root.after(self.ai_delay, self.ai_move)

    def update_button(self, index):
        button = self.buttons[index]
        button.config(text=self.current_player)

    def update_scoreboard(self):
        self.scoreboard.config(text=self.get_score_text())

    def check_win(self, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]  # diagonals
        ]
        for condition in win_conditions:
            if all(self.board[i] == player for i in condition):
                return True
        return False

    def reset_board(self):
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="")

    def ai_mode_toggle(self):
        self.ai_mode = not self.ai_mode
        self.reset_board()
        self.update_status_labels()

    def ai_move(self):
        available_moves = [i for i, spot in enumerate(self.board) if spot == ""]
        if available_moves:
            move = random.choice(available_moves)
            self.button_click(move)

    def two_player_mode(self):
        self.ai_mode = False
        self.reset_board()
        self.update_status_labels()


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
