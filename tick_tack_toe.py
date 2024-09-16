import tkinter as tk
from tkinter import messagebox
import mysql.connector
from modes import PlayerVsPlayer, AIVsPlayer  # Import the modes

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.current_player = 'X'
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_mode = None  # Mode will be set later
        self.create_widgets()
        self.initialize_db()
        self.reset_stats()  
        self.update_stats_label()

    def create_widgets(self):
        self.mode_selection_screen()

    def mode_selection_screen(self):
        """Creates a mode selection screen."""
        self.clear_widgets(preserve_stats=True)

        tk.Label(self.root, text="Select Game Mode", font=('Arial', 20)).grid(row=0, column=0, columnspan=2)
        tk.Button(self.root, text="Player vs Player", font=('Arial', 14), command=self.start_pvp).grid(row=1, column=0, pady=20)
        tk.Button(self.root, text="AI vs Player", font=('Arial', 14), command=self.start_ai).grid(row=1, column=1, pady=20)

    def start_pvp(self):
        """Starts Player vs Player mode."""
        self.clear_widgets(preserve_stats=True)
        self.game_mode = PlayerVsPlayer(self)
        self.game_mode.create_board()

    def start_ai(self):
        """Starts AI vs Player mode."""
        self.clear_widgets(preserve_stats=True)
        self.game_mode = AIVsPlayer(self)
        self.game_mode.create_board()

    def clear_widgets(self, preserve_stats=False):
        """Removes all widgets from the root window."""
        for widget in self.root.winfo_children():
            if preserve_stats and widget == self.stats_label:
                continue
            widget.destroy()

    def initialize_db(self):
        """Initializes the MySQL database connection."""
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='Tias',
                password='tias_pal@2007',
                database='tic_tac_toe'
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Database Error", f"Failed to connect to the database: {err}")
            self.root.quit()

    def reset_stats(self):
        """Fetches the current player stats from the database."""
        try:
            self.cursor.execute("SELECT wins, draws, losses FROM score WHERE player='X'")
            x_scores = self.cursor.fetchone()
            self.x_wins, self.x_draws, self.x_losses = x_scores if x_scores else (0, 0, 0)
            
            self.cursor.execute("SELECT wins, draws, losses FROM score WHERE player='O'")
            o_scores = self.cursor.fetchone()
            self.o_wins, self.o_draws, self.o_losses = o_scores if o_scores else (0, 0, 0)
            
            self.update_stats_label()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Database Error", f"Failed to retrieve stats: {err}")

    def update_stats_label(self):
        """Updates the stats label with current scores."""
        self.stats_label = tk.Label(self.root, text=f"Player X - Wins: {self.x_wins}, Draws: {self.x_draws}, Losses: {self.x_losses}\n"
                                                    f"Player O - Wins: {self.o_wins}, Draws: {self.o_draws}, Losses: {self.o_losses}",
                                    font=('Arial', 14))
        self.stats_label.grid(row=3, column=0, columnspan=3)

    def update_stats(self, player, result):
        """Updates the player stats based on the game result."""
        try:
            if player == 'X':
                if result == 'win':
                    self.x_wins += 1
                elif result == 'draw':
                    self.x_draws += 1
                elif result == 'loss':
                    self.x_losses += 1
            elif player == 'O':
                if result == 'win':
                    self.o_wins += 1
                elif result == 'draw':
                    self.o_draws += 1
                elif result == 'loss':
                    self.o_losses += 1

            # Update the database with the new stats
            self.cursor.execute("UPDATE score SET wins = %s, draws = %s, losses = %s WHERE player = %s",
                                (self.x_wins if player == 'X' else self.o_wins,
                                 self.x_draws if player == 'X' else self.o_draws,
                                 self.x_losses if player == 'X' else self.o_losses,
                                 player))
            self.conn.commit()
            self.update_stats_label()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Database Error", f"Failed to update stats: {err}")

    def reset_scores(self):
        """Resets all scores in the database."""
        try:
            self.cursor.execute("UPDATE score SET wins = 0, draws = 0, losses = 0")
            self.conn.commit()
            self.reset_stats()  # Refresh stats after resetting
            messagebox.showinfo("Tic-Tac-Toe", "All scores have been reset.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Database Error", f"Failed to reset scores: {err}")

    def on_button_click(self, row, col):
        """Calls the game mode's click handling."""
        if self.game_mode:
            self.game_mode.handle_click(row, col)

    def __del__(self):
        if hasattr(self, 'conn') and self.conn is not None:
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
