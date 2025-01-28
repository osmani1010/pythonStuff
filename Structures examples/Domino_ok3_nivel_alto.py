import tkinter as tk
from tkinter import messagebox
import random


class Domino:
    def __init__(self, value1, value2):
        try:
            self.value1 = int(value1)
            self.value2 = int(value2)   
            if not (0 <= self.value1 <= 7 and 0 <= self.value2 <= 7):
                raise ValueError("Domino values must be between 0 and 7")
        except ValueError:
            raise ValueError("Domino values must be valid integers between 0 and 7")

    def __repr__(self):
        return f"[{self.value1}|{self.value2}]"

    def flip(self):
        self.value1, self.value2 = self.value2, self.value1

    def get_score(self):
        return self.value1 + self.value2
    
    # Game Features:
# Add sound effects for moves, wins, and invalid actions
# Implement animation for domino placement
# Add difficulty levels for AI players
# Include a timer for each turn
# Add a game history feature
# Implement save/load game functionality
# AI Intelligence:
# Here's how we can improve the AI logic:


class AIPlayer:
    def __init__(self, difficulty="medium"):
        self.difficulty = difficulty
        
    def choose_move(self, hand, board):
        if self.difficulty == "easy":
            return self._choose_random_move(hand, board)
        elif self.difficulty == "hard":
            return self._choose_strategic_move(hand, board)
        else:  # medium difficulty
            return self._choose_basic_move(hand, board)
        

    def _choose_random_move(self, hand, board):
        if not board:
            return random.randint(0, len(hand) - 1)
            
        valid_moves = []
        for i, piece in enumerate(hand):
            if self._can_play_piece(piece, board[0], board[-1]):
                valid_moves.append(i)
                
        return random.choice(valid_moves) if valid_moves else None
    
    def _choose_basic_move(self, hand, board):
        if not board:
            # Find highest double first
            highest_double_idx = -1
            highest_double_value = -1
            
            for i, piece in enumerate(hand):
                if piece.value1 == piece.value2 and piece.value1 > highest_double_value:
                    highest_double_value = piece.value1
                    highest_double_idx = i
            
            if highest_double_idx != -1:
                return highest_double_idx
            
            # If no doubles, play highest value piece
            return max(range(len(hand)), key=lambda i: hand[i].get_score())
                    
        valid_moves = []
        for i, piece in enumerate(hand):
            if self._can_play_piece(piece, board[0], board[-1]):
                valid_moves.append(i)
                
        return valid_moves[0] if valid_moves else None
    
    def _choose_strategic_move(self, hand, board):
        if not board:
            return self._choose_opening_move(hand)
            
        valid_moves = []
        for i, piece in enumerate(hand):
            if self._can_play_piece(piece, board[0], board[-1]):
                # Calculate move score based on:
                # 1. Number of similar values in hand (matching strategy)
                # 2. Total pip count of the piece (prefer playing high value pieces)
                # 3. Whether it's a double piece (strategic importance)
                score = self._calculate_move_score(piece, hand, board)
                valid_moves.append((i, score))
                
        if not valid_moves:
            return None
            
        # Return the move with highest score
        return max(valid_moves, key=lambda x: x[1])[0]
        
    def _calculate_move_score(self, piece, hand, board):
        score = piece.get_score()  # Base score is pip count
        
        # Bonus for doubles
        if piece.value1 == piece.value2:
            score += 5
            
        # Bonus for matching values with other pieces in hand
        matching_values = sum(1 for p in hand if 
                            p.value1 in (piece.value1, piece.value2) or 
                            p.value2 in (piece.value1, piece.value2))
        score += matching_values * 2
        
        return score
    

# class AIPlayer:
#     def choose_move(self, hand, board):
#         if not board:
#             # Find highest double first
#             highest_double_idx = -1
#             highest_double_value = -1
            
#             for i, piece in enumerate(hand):
#                 if piece.value1 == piece.value2 and piece.value1 > highest_double_value:
#                     highest_double_value = piece.value1
#                     highest_double_idx = i
            
#             if highest_double_idx != -1:
#                 return highest_double_idx
            
#             # If no doubles, play highest value piece
#             return max(range(len(hand)), key=lambda i: hand[i].get_score())
                    
            
#         valid_moves = []
#         for i, piece in enumerate(hand):
#             if self._can_play_piece(piece, board[0], board[-1]):
#                 valid_moves.append((i, piece))
                
#         if not valid_moves:
#             return None
        
#         # Return the index of the first valid move
#         return valid_moves[0][0]  # Add this line to return a valid move
        
            
    def _can_play_piece(self, piece, first_domino, last_domino):
        # Check if piece can be played at the start of the board
        # (should match first_domino.value1)
        # or at the end of the board (should match last_domino.value2)
        return (piece.value1 == first_domino.value1 or
                piece.value2 == first_domino.value1 or
                piece.value1 == last_domino.value2 or
                piece.value2 == last_domino.value2)    
    
    
        
class DominoGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Domino Game")
        self.root.geometry("800x600")
        self.game_active = True
        self.winner = None
        
        
        # Game state variables
        self.board = []
        self.current_player = 0
        self.players = []
        self.player_names = ["Human Player", "Computer 1", "Computer 2", "Computer 3"]
        self.consecutive_passes = 0
        self.scores = {name: 0 for name in self.player_names}

        # Initialize AI players
        self.ai_players = [AIPlayer() for _ in range(3)]


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

        # Score display
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(pady=10)
        self.score_label = tk.Label(self.score_frame, text="Scores:", font=('Arial', 12))
        self.score_label.pack() 
        
        # Player hand display
        self.hand_frame = tk.Frame(self.root)
        self.hand_frame.pack(pady=20)
        self.hand_label = tk.Label(self.hand_frame, text="Your pieces:", font=('Arial', 12))
        self.hand_label.pack()
        self.hand_display = tk.Label(self.hand_frame, text="", font=('Arial', 14))
        self.hand_display.pack()
        self.piece_listbox = tk.Listbox(self.hand_frame, height=10)
        self.piece_listbox.pack(pady=15)
        
        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)
        self.play_button = tk.Button(self.button_frame, text="Play Selected Piece", command=self.play_domino)
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.pass_button = tk.Button(self.button_frame, text="Pass Turn", command=self.handle_pass)
        self.pass_button.pack(side=tk.LEFT, padx=5)
        self.restart_button = tk.Button(self.button_frame, text="New Game", command=self.restart_game)
        self.restart_button.pack(side=tk.LEFT, padx=5)
        

        # Add new GUI elements
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # Game menu
        self.game_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Game", menu=self.game_menu)
        self.game_menu.add_command(label="New Game", command=self.restart_game)
        # self.game_menu.add_command(label="Save Game", command=self.save_game)
        # self.game_menu.add_command(label="Load Game", command=self.load_game)
        self.game_menu.add_separator()
        self.game_menu.add_command(label="Exit", command=self.root.quit)
        
        # Settings menu
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="AI Difficulty", command=self.show_difficulty_settings)
        
        # Add timer label
        # self.timer_label = tk.Label(self.root, text="Time: 0:30", font=('Arial', 12))
        # self.timer_label.pack(pady=5)
        
        # Add status bar 
        self.status_bar = tk.Label(self.root, text="Ready to play", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

    def show_difficulty_settings(self):
        # Create a new top-level window for difficulty settings
        settings_window = tk.Toplevel(self.root)
        settings_window.title("AI Difficulty Settings")
        settings_window.geometry("300x200")
        
        # Create difficulty options for each AI player
        for i, ai_player in enumerate(self.ai_players):
            frame = tk.Frame(settings_window)
            frame.pack(pady=5)
            
            tk.Label(frame, text=f"Computer {i+1}:").pack(side=tk.LEFT, padx=5)
            
            difficulty = tk.StringVar(value=ai_player.difficulty)
            difficulty_menu = tk.OptionMenu(frame, difficulty, "easy", "medium", "hard",
                command=lambda d, index=i: self.update_ai_difficulty(index, d))
            difficulty_menu.pack(side=tk.LEFT)
            
    def update_ai_difficulty(self, ai_index, difficulty):
        self.ai_players[ai_index].difficulty = difficulty
        messagebox.showinfo("Success", f"Computer {ai_index + 1} difficulty updated to {difficulty}")

    def initialize_game(self):
        self.game_active = True
        self.winner = None
        self.consecutive_passes = 0
        
        # Generate dominoes
        try:
            dominoes = [Domino(i, j) for i in range(8) for j in range(i, 8)]
            random.shuffle(dominoes)

            # Distribute pieces
            self.players = [
                dominoes[:8],
                dominoes[8:16],
                dominoes[16:24],
                dominoes[24:32]
            ]
            
            # Determine starting player based on highest double
            self.current_player = self._find_starting_player()
            
            self.remaining_pieces = dominoes[32:]
            self.board = []  # Start with empty board
            
            self.update_display()

            # Automatically play first move if AI is starting player
            if self.current_player != 0:  # If not human player
                self.root.after(1000, self.handle_ai_turn)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize game: {e}")
        

    def _find_starting_player(self):
        highest_double = -1
        starting_player = 0
        
        for player_idx, hand in enumerate(self.players):
            for piece in hand:
                if piece.value1 == piece.value2 and piece.value1 > highest_double:
                    highest_double = piece.value1
                    starting_player = player_idx
        
        return starting_player
    
    def restart_game(self):
        self.board = []
        self.current_player = 0
        self.players = []
        self.consecutive_passes = 0
        self.initialize_game()


    def update_display(self):
        # Update board display
        self.board_display.config(text=" ".join(str(d) for d in self.board))

        # Update current player's hand
        self.hand_display.config(text=" ".join(str(d) for d in self.players[self.current_player]))

        # Update turn indicator
        self.hand_label.config(text=f"{self.player_names[self.current_player]}'s pieces:")
        self.status_bar.config(text=f"Current turn: {self.player_names[self.current_player]}")

        # Update the listbox with current player's pieces
        self.piece_listbox.delete(0, tk.END)
        for i, piece in enumerate(self.players[self.current_player]):
            self.piece_listbox.insert(tk.END, f"{i}: {piece}")

        score_text = " | ".join(f"{name}: {score}" for name, score in self.scores.items())
        self.score_label.config(text=f"Scores: {score_text}")

    def play_domino(self):  
        current_player_hand = self.players[self.current_player]
        if not current_player_hand:
            return False
       
    # Get selected piece index
        selection = self.piece_listbox.curselection()
        if not selection:
            self.status_bar.config(text="Error: Please select a piece to play")
            messagebox.showinfo("Error", "Please select a piece to play")
            return False
        
        piece_index = selection[0]
        piece = current_player_hand[piece_index]

        # Handle empty board case
        if not self.board:
            current_player_hand.pop(piece_index)
            self.board.append(piece)
            self.consecutive_passes = 0
            self.check_win_condition()
            self.next_turn()
            return True

        first_domino = self.board[0]
        last_domino = self.board[-1]

        # Try to play the selected piece
        if self._try_play_piece(piece, piece_index, first_domino, last_domino):
            self.consecutive_passes = 0
            self.check_win_condition()
            self.next_turn()
            return True
            
        messagebox.showinfo("Invalid Move", "This piece cannot be played!")
        return False

    def _try_play_piece(self, piece, piece_index, first_domino, last_domino):
        """Attempt to play a piece at either end of the board."""
        current_player_hand = self.players[self.current_player]

        #Try to play at the start of the board
        if piece.value2 == first_domino.value1:  # Changed from piece.value1
            current_player_hand.pop(piece_index)
            self.board.insert(0, piece)
            return True
        if piece.value1 == first_domino.value1:  # Changed from piece.value2
            piece.flip()
            current_player_hand.pop(piece_index)
            self.board.insert(0, piece)
            return True
        
    # Try to play at the end of the board
        if piece.value1 == last_domino.value2:
            current_player_hand.pop(piece_index)
            self.board.append(piece)
            return True
        if piece.value2 == last_domino.value2:
            piece.flip()
            current_player_hand.pop(piece_index)
            self.board.append(piece)
            return True
        
        return False

    def calculate_player_sum(self, player):
        return sum(piece.value1 + piece.value2 for piece in player)
    
    def handle_pass(self):
        self.consecutive_passes += 1
        self.status_bar.config(text=f"{self.player_names[self.current_player]} passed their turn")
        
        if self.consecutive_passes >= 4:
            self.handle_deadlock()
        else:
            self.next_turn()

    def next_turn(self):
        self.current_player = (self.current_player + 1) % 4

        # Handle AI turns
        if self.current_player != 0 and self.game_active:
            self.update_display()
            self.root.after(1000, self.handle_ai_turn)  # Delay AI move by 1 second
        else:
            self.update_display()

    def handle_ai_turn(self):
        if not self.game_active:
            return
            
        ai_index = self.current_player - 1  # Adjust index for AI players array
        move_index = self.ai_players[ai_index].choose_move(self.players[self.current_player], self.board)
        
        if move_index is not None:
            piece = self.players[self.current_player][move_index]
            if not self.board: # If board is empty
                self.players[self.current_player].pop(move_index)
                self.board.append(piece)
                self.consecutive_passes = 0
                self.check_win_condition()
                self.next_turn()
            else:
                first_domino = self.board[0]
                last_domino = self.board[-1]
                if self._try_play_piece(piece, move_index, first_domino, last_domino):
                    self.consecutive_passes = 0
                    self.check_win_condition()
                    self.next_turn()
                else:
                    self.handle_pass()
                    
        else:
            self.status_bar.config(text=f"{self.player_names[self.current_player]} is passing")
            self.handle_pass()
            
            # messagebox.showinfo("Not a valid move", f"{self.player_names[self.current_player]} passed")
            

    def check_win_condition(self):
        if len(self.players[self.current_player]) == 0:
            # Update scores for the winner
            self.scores[self.player_names[self.current_player]] += 1
            
            # Show win message
            messagebox.showinfo("Game Over", f"{self.player_names[self.current_player]} wins!")
            
            # Ask if players want to start a new game
            if messagebox.askyesno("New Game", "Would you like to start a new game?"):
                self.restart_game()
            else:
                self.root.quit()

    def handle_deadlock(self):
        player_sums = [self.calculate_player_sum(p) for p in self.players]
        min_sum = min(player_sums)
        winner_index = player_sums.index(min_sum)

        # Update scores for the winner
        self.scores[self.player_names[winner_index]] += 1

        result_message = "Game is deadlocked!\n\n"
        for i, sum_value in enumerate(player_sums):
            result_message += f"{self.player_names[i]} total: {sum_value}\n"
        result_message += f"\n{self.player_names[winner_index]} wins with the lowest sum of {min_sum}!"

        self.game_active = False  # Mark game as inactive
        messagebox.showinfo("Game Over", result_message)

        # Ask if players want to start a new game
        if messagebox.askyesno("New Game", "Would you like to start a new game?"):
            self.restart_game()
        else:
            self.root.quit()
    

if __name__ == "__main__":
    root = tk.Tk()
    game = DominoGameGUI(root)
    root.mainloop()





    
    
    
    
    # def _choose_opening_move(self, hand):
    #     # First priority: highest double
    #     highest_double_idx = -1
    #     highest_double_value = -1
        
    #     for i, piece in enumerate(hand):
    #         if piece.value1 == piece.value2 and piece.value1 > highest_double_value:
    #             highest_double_value = piece.value1
    #             highest_double_idx = i
        
    #     if highest_double_idx != -1:
    #         return highest_double_idx
        
    #     # Second priority: highest scoring piece
    #     return max(range(len(hand)), key=lambda i: hand[i].get_score())

    



#     def update_display(self):
        
#         # Update turn indicator and status bar
#         self.hand_label.config(text=f"{self.player_names[self.current_player]}'s pieces:")
#         self.status_bar.config(text=f"Current turn: {self.player_names[self.current_player]}")

# // ... existing code ...

#     def handle_pass(self):
#         self.consecutive_passes += 1
#         self.status_bar.config(text=f"{self.player_names[self.current_player]} passed their turn")
#         if self.consecutive_passes >= 4:
#             self.handle_deadlock()
#         else:
#             self.next_turn()

# // ... existing code ...

#     def play_domino(self):
#         current_player_hand = self.players[self.current_player]
#         if not current_player_hand:
#             return False
       
#         # Get selected piece index
#         selection = self.piece_listbox.curselection()
#         if not selection:
#             self.status_bar.config(text="Error: Please select a piece to play")
#             messagebox.showinfo("Error", "Please select a piece to play")
#             return False

# // ... existing code ...


# # Add sound effects
# def play_sound(self, sound_type):
#     # Implement sound effects for:
#     # - placing dominoes
#     # - winning
#     # - invalid moves
#     # - passing turn
#     pass

