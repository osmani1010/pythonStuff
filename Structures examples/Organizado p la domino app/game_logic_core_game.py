def play_domino(self):
        # Check if game is still active
    if not self.game_active:
        self.status_bar.config(text="Game is over. Please start a new game.")
        messagebox.showinfo("Game Over", "This game has ended. Please start a new game.")
        return False  
        
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

def calculate_player_sum(self, player):
    return sum(piece.value1 + piece.value2 for piece in player)


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