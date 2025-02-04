
        
// ... existing code ...

class DominoGameGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        // ... existing initialization code ...
        self.last_winner = None  # Add this line to track the last winner
        self.setup_gui()
        // ... rest of initialization ...

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
                dominoes[:6],
                dominoes[6:12],
                dominoes[12:18],
                dominoes[18:24]
            ]

            # If there's a last winner, they start, otherwise find highest double
            if self.last_winner is not None:
                self.current_player = self.player_names.index(self.last_winner)
            else:
                self.current_player = self._find_starting_player()

            self.remaining_pieces = dominoes[24:]
            self.board = []  # Start with empty board

            self.update_display()

            # Automatically play first move if AI is starting player
            if self.current_player != 0:  # If not human player
                Clock.schedule_once(lambda dt: self.handle_ai_turn(), 2)

        except Exception as e:
            self.show_popup("Error", f"Failed to initialize game: {e}")

    def handle_round_end(self, popup, start_new_round):
        popup.dismiss()
        if start_new_round:
            # Keep the scores and last winner but reset the board and hands
            self.board = []
            self.initialize_game()
        else:
            self.game_active = False
            self.status_bar.text = "Game Over. Click 'New Game' to play again."

    def check_win_condition(self):
        if len(self.players[self.current_player]) == 0:
            self.game_active = False
            winner_name = self.player_names[self.current_player]
            self.last_winner = winner_name  # Store the winner
            
            if self.current_mode == 'Points':
                # Calculate points from remaining pieces
                round_points = sum(sum(piece.get_score() for piece in hand) for hand in self.players)
                self.scores[winner_name] += round_points
                
                if self.scores[winner_name] >= self.target_score:
                    self.show_final_winner_popup(winner_name)
                else:
                    self.show_round_winner_popup(winner_name, round_points)
            else:
                # Classic or Block mode
                self.scores[winner_name] += 1
                self.show_round_winner_popup(winner_name)

    def restart_game(self, *args):
        self.board = []
        self.current_player = 0
        self.players = []
        self.consecutive_passes = 0
        self.last_winner = None  # Reset last winner on full game restart
        self.initialize_game()

    def handle_deadlock(self):
        player_sums = [self.calculate_player_sum(p) for p in self.players]
        min_sum = min(player_sums)
        winner_index = player_sums.index(min_sum)
        winner_name = self.player_names[winner_index]

        # Update scores for the winner and store last winner
        self.scores[winner_name] += 1
        self.last_winner = winner_name

        // ... rest of handle_deadlock method ...