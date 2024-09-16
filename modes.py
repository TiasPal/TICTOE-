import tkinter as tk
from tkinter import messagebox
import random

class GameMode:
    def __init__(self, parent):
        self.parent = parent
        self.current_player = 'X'
        self.buttons = parent.buttons

    def create_board(self):
        """Create the game board UI."""
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.parent.root, text=' ', font=('Arial', 40), width=5, height=2,
                                   command=lambda r=row, c=col: self.parent.on_button_click(r, c))
                button.grid(row=row, column=col, padx=5, pady=5)
                self.buttons[row][col] = button

        self.parent.stats_label.grid(row=3, column=0, columnspan=3)
        self.parent.reset_button = tk.Button(self.parent.root, text="Reset Scores", font=('Arial', 12),
                                             command=self.parent.reset_scores)
        self.parent.reset_button.grid(row=4, column=0, columnspan=3, pady=10)

    def check_win(self, player):
        """Check for a win."""
        for row in range(3):
            if all(self.buttons[row][col]['text'] == player for col in range(3)):
                return True
        for col in range(3):
            if all(self.buttons[row][col]['text'] == player for row in range(3)):
                return True
        if all(self.buttons[i][i]['text'] == player for i in range(3)):
            return True
        if all(self.buttons[i][2 - i]['text'] == player for i in range(3)):
            return True
        return False

    def check_draw(self):
        """Check for a draw."""
        return all(self.buttons[row][col]['text'] != ' ' for row in range(3) for col in range(3))

    def reset_board(self):
        """Reset the game board."""
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]['text'] = ' '
        self.current_player = 'X'


class PlayerVsPlayer(GameMode):
    def handle_click(self, row, col):
        button = self.buttons[row][col]
        if button['text'] == ' ':
            button['text'] = self.current_player
            if self.check_win(self.current_player):
                messagebox.showinfo("Tic-Tac-Toe", f"Player {self.current_player} wins!")
                self.parent.update_stats(self.current_player, 'win')
                self.parent.update_stats('O' if self.current_player == 'X' else 'X', 'loss')
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                self.parent.update_stats('X', 'draw')
                self.parent.update_stats('O', 'draw')
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'


class AIVsPlayer(GameMode):
    def handle_click(self, row, col):
        if self.current_player == 'X':
            self.player_move(row, col)
        elif self.current_player == 'O':
            self.ai_move()

    def player_move(self, row, col):
        button = self.buttons[row][col]
        if button['text'] == ' ':
            button['text'] = 'X'
            if self.check_win('X'):
                messagebox.showinfo("Tic-Tac-Toe", "Player X wins!")
                self.parent.update_stats('X', 'win')
                self.parent.update_stats('O', 'loss')
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                self.parent.update_stats('X', 'draw')
                self.parent.update_stats('O', 'draw')
                self.reset_board()
            else:
                self.ai_move()

    def ai_move(self):
        available_moves = [(r, c) for r in range(3) for c in range(3) if self.buttons[r][c]['text'] == ' ']
        if available_moves:
            row, col = random.choice(available_moves)
            self.buttons[row][col]['text'] = 'O'
            if self.check_win('O'):
                messagebox.showinfo("Tic-Tac-Toe", "Player O (AI) wins!")
                self.parent.update_stats('O', 'win')
                self.parent.update_stats('X', 'loss')
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                self.parent.update_stats('X', 'draw')
                self.parent.update_stats('O', 'draw')
                self.reset_board()
            else:
                self.current_player = 'X'
