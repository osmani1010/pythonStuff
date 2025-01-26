import tkinter as tk
from tkinter import messagebox
import random

class Domino:
    def __init__(self, value1, value2):
        try:
            self.value1 = int(value1)
            self.value2 = int(value2)
        except ValueError:
            raise ValueError("Domino values must be integers")

   
    def __repr__(self):
        return f"[{self.value1}|{self.value2}]"
    

    def flip(self):
        self.value1, self.value2 = self.value2, self.value1


class DominoGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Domino Game")
        self.root.geometry("800x600")
        
        # Game state variables
        self.board = []
        self.current_player = 0
        self.players = []
        self.player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]
        self.consecutive_passes = 0
        
        # Create GUI elements
        self.setup_gui()
        self.initialize_game()
    
    def setup_gui(self):
        # Board display
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=20)
        self.board_label = tk.Label(self.board_frame, text="Board:", font=('Arial', 12))
        self.board_label.pack()
        self.board_display = tk.Label(self.board_frame, text="", font=('Arial', 14))
        self.board_display.pack()
        
        # Player hand display
        self.hand_frame = tk.Frame(self.root)
        self.hand_frame.pack(pady=20)
        self.hand_label = tk.Label(self.hand_frame, text="Your pieces:", font=('Arial', 12))
        self.hand_label.pack()
        self.hand_display = tk.Label(self.hand_frame, text="", font=('Arial', 14))
        self.hand_display.pack()
        
        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)
        self.play_button = tk.Button(self.button_frame, text="Play Selected Piece", command=self.handle_play)
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.pass_button = tk.Button(self.button_frame, text="Pass Turn", command=self.handle_pass)
        self.pass_button.pack(side=tk.LEFT, padx=5)

    def initialize_game(self):
        # Generate dominoes
        try:
            dominoes = [Domino(i, j) for i in range(10) for j in range(i, 10)]
            random.shuffle(dominoes)
            
            # Distribute pieces
            self.players = [
                dominoes[:10],
                dominoes[10:20],
                dominoes[20:30],
                dominoes[30:40]
            ]
            self.remaining_pieces = dominoes[40:]
            self.board = [self.remaining_pieces.pop()]

            player1 = dominoes[:10]
            player2 = dominoes[10:20]
            player3 = dominoes[20:30]
            player4 = dominoes[30:40]
            remaining_pieces = dominoes[40:]
            
            self.update_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize game: {e}")
    
    def update_display(self):
        # Update board display
        self.board_display.config(text=" ".join(str(d) for d in self.board))
        
        # Update current player's hand
        self.hand_display.config(text=" ".join(str(d) for d in self.players[self.current_player]))
        
        # Update turn indicator
        self.hand_label.config(text=f"{self.player_names[self.current_player]}'s pieces:")
    

    def play_domino(player, board):
        
        if not board:
            raise ValueError("Board cannot be empty")
        if not player:
            return False
    
    first_domino = board[0]
    last_domino = board[-1]
        
    for piece in player:
        if piece.value1 == first_domino.value1:
            piece.flip()  # Flip to match
            player.remove(piece)
            board.insert(0, piece)
            
            return True
        elif piece.value2 == first_domino.value1:
            player.remove(piece)
            board.insert(0, piece)
            return True
        # Check if piece can be connected to the end of the board
        elif piece.value1 == last_domino.value2:
            player.remove(piece)
            board.append(piece)
            return True
        elif piece.value2 == last_domino.value2:
            piece.flip()  # Flip to match
            player.remove(piece)
            board.append(piece)
            return True       
        

    def handle_play(self):
        # This would need to be implemented with piece selection logic
        if play_domino(self.players[self.current_player], self.board):
            self.consecutive_passes = 0
            self.check_win_condition()
            self.next_turn()
        else:
            messagebox.showinfo("Invalid Move", "No valid moves available!")
    
    def handle_pass(self):
        self.consecutive_passes += 1
        if self.consecutive_passes >= 4:
            self.handle_deadlock()
        else:
            self.next_turn()
    
    def next_turn(self):
        self.current_player = (self.current_player + 1) % 4
        self.update_display()
    
    def check_win_condition(self):
        if len(self.players[self.current_player]) == 0:
            messagebox.showinfo("Game Over", f"{self.player_names[self.current_player]} wins!")
            self.root.quit()
    
    def handle_deadlock(self):
        player_sums = [calculate_player_sum(p) for p in self.players]
        min_sum = min(player_sums)
        winner_index = player_sums.index(min_sum)
        
        result_message = "Game is deadlocked!\n\n"
        for i, sum_value in enumerate(player_sums):
            result_message += f"{self.player_names[i]} total: {sum_value}\n"
        result_message += f"\n{self.player_names[winner_index]} wins with the lowest sum of {min_sum}!"
        
        messagebox.showinfo("Game Over", result_message)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = DominoGameGUI(root)
    root.mainloop()