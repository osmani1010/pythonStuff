from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.clock import Clock  # Add this import
from kivy.graphics import Rectangle, Color, Ellipse, PushMatrix, PopMatrix
from kivy.properties import NumericProperty
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
            # First priority: highest double
            highest_double_idx = -1
            highest_double_value = -1

            for i, piece in enumerate(hand):
                if piece.value1 == piece.value2 and piece.value1 > highest_double_value:
                    highest_double_value = piece.value1
                    highest_double_idx = i

            if highest_double_idx != -1:
                return highest_double_idx

            # Second priority: highest scoring piece
            return max(range(len(hand)), key=lambda i: hand[i].get_score())

        valid_moves = []
        for i, piece in enumerate(hand):
            if self._can_play_piece(piece, board[0], board[-1]):
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


    def _can_play_piece(self, piece, first_domino, last_domino):
        # Get the values we need to match at either end of the board
        start_value = first_domino.value1
        end_value = last_domino.value2

        # Check if either value of the piece matches either end of the board
        return any(value in (start_value, end_value) for value in (piece.value1, piece.value2))
    

class DominoGameGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_piece_index = None
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Game mode settings
        self.game_modes = {
            'Classic': {'description': 'First to empty hand wins round'},
            'Block': {'description': 'Play to empty hand, blocked game counts'},
            'Points': {'description': 'Play to 100 points, lowest sum wins round'}
        }
        self.current_mode = 'Classic'
        self.target_score = 100  # For Points mode

        # Existing game state variables
        self.board = []
        self.current_player = 0
        self.players = []
        self.player_names = ["Human Player", "Computer 1", "Computer 2", "Computer 3"]
        self.consecutive_passes = 0
        self.scores = {name: 0 for name in self.player_names}
        self.ai_players = [AIPlayer() for _ in range(3)]
        self.game_active = True
        self.winner = None

        self.setup_gui()
        # Add settings and mode selection buttons
        self.button_layout.add_widget(Button(text="Settings", on_press=self.show_difficulty_settings))
        self.button_layout.add_widget(Button(text="Game Modes", on_press=self.show_game_modes))

        self.initialize_game()

    def setup_gui(self):
        # Board display
        self.board_layout = BoxLayout(orientation='vertical', size_hint_y=0.3)
        self.board_label = Label(text="Board:", size_hint_y=0.2)
        self.board_display = Label(text="", size_hint_y=0.8)
        # self.board_layout.background_color = (0.2, 0.8, 0.2, 1)  # Green background
        # Window.clearcolor = (0.2, 0.8, 0.2, 1)  # This sets the window background to green
        self.board_layout.add_widget(self.board_label)
        self.board_layout.add_widget(self.board_display)
        self.add_widget(self.board_layout)

        # Score display
        self.score_label = Label(text="Scores:", size_hint_y=0.1)
        self.add_widget(self.score_label)

        # Player hand display
        self.hand_layout = BoxLayout(orientation='vertical', size_hint_y=0.4)
        self.hand_label = Label(text="Your pieces:", size_hint_y=0.2)
        self.pieces_grid = GridLayout(cols=8, spacing=5, size_hint_y=0.8)
        self.hand_layout.add_widget(self.hand_label)
        self.hand_layout.add_widget(self.pieces_grid)
        self.add_widget(self.hand_layout)

        # Buttons
        self.button_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        self.play_button = Button(text="Play Selected Piece", on_press=self.play_domino)
        self.pass_button = Button(text="Pass Turn", on_press=self.handle_pass)
        self.restart_button = Button(text="New Game", on_press=self.restart_game)
        
        self.button_layout.add_widget(self.play_button)
        self.button_layout.add_widget(self.pass_button)
        self.button_layout.add_widget(self.restart_button)
        self.add_widget(self.button_layout)

        # Status bar
        self.status_bar = Label(text="Ready to play", size_hint_y=0.1)
        self.add_widget(self.status_bar)

    def update_display(self):
        # Update board display
        self.board_display.text = " ".join(str(d) for d in self.board)

        # Update pieces grid
        self.pieces_grid.clear_widgets()
        # Always show human player's pieces (players[0]

        for i, piece in enumerate(self.players[0]):
            btn = Button(
                text=str(piece),
                background_normal='',
                background_color=(0.3, 0.8, 0.3, 1) if self.current_player == 0 else (0.7, 0.7, 0.7, 1)  # Dim when not player's turn
            )
            btn.piece_index = i
            btn.bind(on_press=self.select_piece if self.current_player == 0 else lambda x: None)
            if i == self.selected_piece_index and self.current_player == 0:
                btn.background_color = (0.8, 0.8, 1, 1)
            self.pieces_grid.add_widget(btn)
            
        # Update labels
        self.hand_label.text = "Your pieces: (Waiting for other players)" if self.current_player != 0 else "Your pieces: Your turn!"
        self.status_bar.text = f"Current turn: {self.player_names[self.current_player]}"
    
        score_text = " | ".join(f"{name}: {score}" for name, score in self.scores.items())
        self.score_label.text = f"Scores: {score_text}"
        


    def select_piece(self, button):
        # Reset all pieces to default color
        for child in self.pieces_grid.children:
            child.background_color = (0.3, 0.8, 0.3, 1) if self.current_player == 0 else (0.7, 0.7, 0.7, 1)
        
        # Update selected piece index and highlight the selected piece
        self.selected_piece_index = button.piece_index
        button.background_color = (0.8, 0.8, 1, 1)  # Highlight selected piece
        
    def show_difficulty_settings(self, *args):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        for i, ai_player in enumerate(self.ai_players):
            row = BoxLayout(spacing=10, size_hint_y=None, height=40)
            row.add_widget(Label(text=f"Computer {i+1}:", size_hint_x=0.4))
            
            for difficulty in ['easy', 'medium', 'hard']:
                btn = Button(
                    text=difficulty,
                    size_hint_x=0.2,
                )
                # Use lambda with default arguments to avoid late binding issues
                btn.bind(on_press=lambda btn, idx=i, diff=difficulty: self.update_ai_difficulty(idx, diff))
                if ai_player.difficulty == difficulty:
                    btn.background_color = (0.3, 0.6, 0.9, 1)
                row.add_widget(btn)
            
            content.add_widget(row)

        close_button = Button(
            text='Close',
            size_hint_y=None,
            height=40
        )
        
        self.settings_popup = Popup(
            title='AI Difficulty Settings',
            content=content,
            size_hint=(None, None),
            size=(400, 250),
        )
        
        close_button.bind(on_press=self.settings_popup.dismiss)
        content.add_widget(close_button)
        self.settings_popup.open()


    def update_ai_difficulty(self, ai_index, difficulty):
        self.ai_players[ai_index].difficulty = difficulty
        self.show_popup("Success", f"Computer {ai_index + 1} difficulty updated to {difficulty}")

    
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

            # Determine starting player based on highest double
            self.current_player = self._find_starting_player()

            self.remaining_pieces = dominoes[24:]
            self.board = []  # Start with empty board

            self.update_display()

            # Automatically play first move if AI is starting player
            if self.current_player != 0:  # If not human player
                Clock.schedule_once(lambda dt: self.handle_ai_turn(), 2)  # Changed from root.after

        except Exception as e:
            self.show_popup("Error", f"Failed to initialize game: {e}")


    def _find_starting_player(self):
        highest_double = -1
        starting_player = 0

        for player_idx, hand in enumerate(self.players):
            for piece in hand:
                if piece.value1 == piece.value2 and piece.value1 > highest_double:
                    highest_double = piece.value1
                    starting_player = player_idx

        return starting_player

    def restart_game(self, *args):  # Modified to accept variable arguments
        self.board = []
        self.current_player = 0
        self.players = []
        self.consecutive_passes = 0
        self.initialize_game()


    def play_domino(self, *args):  # Add *args parameter
        # Check if game is still active
        if not self.game_active:
            self.status_bar.text = "Game is over. Please start a new game."
            self.show_popup("Game Over", "This game has ended. Please start a new game.")
            return False

        current_player_hand = self.players[self.current_player]
        if not current_player_hand:
            return False

        # Check if a piece is selected
        if self.selected_piece_index is None:
            self.status_bar.text = "Error: Please select a piece to play"
            self.show_popup("Error", "Please select a piece to play")   
            return False

        piece = current_player_hand[self.selected_piece_index]
        
        # Handle empty board case
        if not self.board:
            current_player_hand.pop(self.selected_piece_index)
            self.board.append(piece)
            self.consecutive_passes = 0
            self.check_win_condition()
            self.selected_piece_index = None  # Reset selection
            self.next_turn()
            return True

        first_domino = self.board[0]
        last_domino = self.board[-1]

        #Try to play the piece and store the result
        play_result = self._try_play_piece(piece, self.selected_piece_index, first_domino, last_domino)

        #Only proceed if the piece was actually played
        if play_result:
            self.consecutive_passes = 0
            self.check_win_condition()
            self.selected_piece_index = None  # Reset selection
            self.next_turn()
            return True
        elif not play_result and self.current_player == 0:
            #Don't show invalid move popup if waiting for side choice
            if not (
                (first_domino.value1 == last_domino.value2 and 
                (piece.value1 == first_domino.value1 or piece.value2 == first_domino.value1)) or
                (first_domino.value1 != last_domino.value2 and 
                piece.value1 == last_domino.value2 and 
                piece.value2 == first_domino.value1 or 
                piece.value1 == first_domino.value1 and piece.value2 == last_domino.value2)
                
            ):
                self.show_popup("Invalid Move", "This piece cannot be played!")
        return False

    def _try_play_piece(self, piece, piece_index, first_domino, last_domino):
        """Attempt to play a piece at either end of the board."""
        current_player_hand = self.players[self.current_player]

        # For human player
        if self.current_player == 0:
            if len(self.board) > 1:
                if first_domino.value1 == last_domino.value2 and (
                    piece.value1 == first_domino.value1 or 
                    piece.value2 == first_domino.value1):
                    self.show_side_choice_popup(piece, piece_index)
                    return False
            
                if first_domino.value1 != last_domino.value2 and (
                    piece.value1 == last_domino.value2 and
                    piece.value2 == first_domino.value1 or 
                    piece.value1 == first_domino.value1 and piece.value2 == last_domino.value2):
                    self.show_side_choice_popup(piece, piece_index)
                    return False

        # Try to play at the start of the board
            if piece.value2 == first_domino.value1:
                current_player_hand.pop(piece_index)
                self.board.insert(0, piece)
                return True
            if piece.value1 == first_domino.value1:
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

        # For AI players
        else:
            if piece.value2 == first_domino.value1:
                current_player_hand.pop(piece_index)
                self.board.insert(0, piece)
                return True
            if piece.value1 == first_domino.value1:
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

    def show_side_choice_popup(self, piece, piece_index):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=f"Choose which side to play {piece}:"))
        
        buttons = BoxLayout(size_hint_y=0.4, spacing=10)
        start_button = Button(text='Start of Board')
        end_button = Button(text='End of Board')
        buttons.add_widget(start_button)
        buttons.add_widget(end_button)
        content.add_widget(buttons)
        
        popup = Popup(
            title='Choose Side',
            content=content,
            size_hint=(None, None),
            size=(300, 200),
            auto_dismiss=False
        )
        
        def play_at_start(instance):
            current_player_hand = self.players[self.current_player]
            if piece.value2 == self.board[0].value1:
                current_player_hand.pop(piece_index)
                self.board.insert(0, piece)
            else:
                piece.flip()
                current_player_hand.pop(piece_index)
                self.board.insert(0, piece)
            popup.dismiss()
            self.consecutive_passes = 0
            self.check_win_condition()
            if self.game_active: # Only call next_turn if game is still active
                self.next_turn()
        
        def play_at_end(instance):
            current_player_hand = self.players[self.current_player]
            if piece.value1 == self.board[-1].value2:
                current_player_hand.pop(piece_index)
                self.board.append(piece)
            else:
                piece.flip()
                current_player_hand.pop(piece_index)
                self.board.append(piece)
            popup.dismiss()
            self.consecutive_passes = 0
            self.check_win_condition()
            if self.game_active: # Only call next_turn if game is still active
                self.next_turn()
        
        start_button.bind(on_press=play_at_start)
        end_button.bind(on_press=play_at_end)
        popup.open()



    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message))
        
        dismiss_button = Button(
            text="OK",
            size_hint=(None, None),
            size=(100, 44),
            pos_hint={'center_x': 0.5}
        )
        
        content.add_widget(dismiss_button)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(400, 200),
            auto_dismiss=True
        )
        
        dismiss_button.bind(on_press=popup.dismiss)
        popup.open()


    def handle_pass(self, *args):  # Add *args parameter
        self.consecutive_passes += 1
        current_player_name = self.player_names[self.current_player]
        self.status_bar.text = f"{self.player_names[self.current_player]} passed their turn"


        if self.consecutive_passes >= 4:
            self.handle_deadlock()
        else:
            self.next_turn()

    def next_turn(self):
        self.current_player = (self.current_player + 1) % 4

        # Handle AI turns
        if self.current_player != 0 and self.game_active:
            self.update_display()
            Clock.schedule_once(lambda dt: self.handle_ai_turn(), 1)  # Changed from root.after
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
            current_player_name = self.player_names[self.current_player]
            self.status_bar.text = f"{self.player_names[self.current_player]} is passing"  
            self.handle_pass()
            
    
    
    def show_game_modes(self, *args):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        for mode, details in self.game_modes.items():
            row = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=60)
            btn = Button(
                text=f"{mode}\n{details['description']}",
                size_hint_y=None,
                height=50
            )
            if mode == self.current_mode:
                btn.background_color = (0.3, 0.6, 0.9, 1)
            btn.bind(on_press=lambda btn, m=mode: self.change_game_mode(m))
            row.add_widget(btn)
            content.add_widget(row)

        if self.current_mode == 'Points':
            score_input = BoxLayout(size_hint_y=None, height=40)
            score_input.add_widget(Label(text="Target Score:"))
            score_btn = Button(
                text=str(self.target_score),
                size_hint_x=0.5,
                on_press=lambda x: self.show_score_input()
            )
            score_input.add_widget(score_btn)
            content.add_widget(score_input)

        close_button = Button(
            text='Close',
            size_hint_y=None,
            height=40
        )
        
        popup = Popup(
            title='Select Game Mode',
            content=content,
            size_hint=(None, None),
            size=(400, 300),
        )
        
        close_button.bind(on_press=popup.dismiss)
        content.add_widget(close_button)
        popup.open()

    def change_game_mode(self, mode):
        self.current_mode = mode
        self.scores = {name: 0 for name in self.player_names}  # Reset scores
        self.show_popup("Game Mode Changed", f"Changed to {mode} mode\n{self.game_modes[mode]['description']}")
        self.restart_game()

    def check_win_condition(self):
        if len(self.players[self.current_player]) == 0:
            self.game_active = False
            
            if self.current_mode == 'Points':
                # Calculate points from remaining pieces
                round_points = sum(sum(piece.get_score() for piece in hand) for hand in self.players)
                self.scores[self.player_names[self.current_player]] += round_points
                
                if self.scores[self.player_names[self.current_player]] >= self.target_score:
                    self.show_final_winner_popup(self.player_names[self.current_player])
                else:
                    self.show_round_winner_popup(self.player_names[self.current_player], round_points)
            else:
                # Classic or Block mode
                self.scores[self.player_names[self.current_player]] += 1
                self.show_round_winner_popup(self.player_names[self.current_player])

    def show_round_winner_popup(self, winner_name, points=None):
        message = f"{winner_name} wins the round!"
        if points is not None:
            message += f"\nPoints earned: {points}"
        message += "\n\nWould you like to start the next round?"
        
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message))
        
        buttons = BoxLayout(size_hint_y=0.4, spacing=10)
        yes_button = Button(text='Yes')
        no_button = Button(text='No')
        buttons.add_widget(yes_button)
        buttons.add_widget(no_button)
        content.add_widget(buttons)
        
        popup = Popup(
            title='Round Over',
            content=content,
            size_hint=(None, None),
            size=(400, 200),
            auto_dismiss=False
        )
        
        yes_button.bind(on_press=lambda x: self.handle_round_end(popup, True))
        no_button.bind(on_press=lambda x: self.handle_round_end(popup, False))
        popup.open()


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
        result_message += "\n\nWould you like to start a new game?"

        # Create confirmation popup
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=result_message))
        
        buttons = BoxLayout(size_hint_y=0.4, spacing=10)
        yes_button = Button(text='Yes')
        no_button = Button(text='No')
        buttons.add_widget(yes_button)
        buttons.add_widget(no_button)
        content.add_widget(buttons)
        
        popup = Popup(
            title='Game Over',
            content=content,
            size_hint=(None, None),
            size=(400, 300),  # Made slightly larger to accommodate the longer message
            auto_dismiss=False
        )
        
        def on_yes(instance):
            popup.dismiss()
            self.restart_game()
            
        def on_no(instance):
            popup.dismiss()
            self.game_active = False
            self.status_bar.text = "Game Over. Click 'New Game' to play again."
        
        yes_button.bind(on_press=on_yes)
        no_button.bind(on_press=on_no)
        popup.open()


    def show_score_input(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Create text input for score
        from kivy.uix.textinput import TextInput
        score_input = TextInput(
            text=str(self.target_score),
            input_filter='int',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        
        # Label for instructions
        content.add_widget(Label(text="Enter target score (10-1000):"))
        content.add_widget(score_input)
        
        # Buttons layout
        buttons = BoxLayout(size_hint_y=None, height=40, spacing=10)
        save_btn = Button(text='Save')
        cancel_btn = Button(text='Cancel')
        buttons.add_widget(save_btn)
        buttons.add_widget(cancel_btn)
        content.add_widget(buttons)
        
        popup = Popup(
            title='Set Target Score',
            content=content,
            size_hint=(None, None),
            size=(300, 200),
            auto_dismiss=False
        )
        
        def save_score(instance):
            try:
                new_score = int(score_input.text)
                if 10 <= new_score <= 1000:
                    self.target_score = new_score
                    popup.dismiss()
                    self.show_popup("Success", f"Target score set to {new_score}")
                else:
                    self.show_popup("Error", "Score must be between 10 and 1000")
            except ValueError:
                self.show_popup("Error", "Please enter a valid number")
        
        save_btn.bind(on_press=save_score)
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

    def show_final_winner_popup(self, winner_name):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Create message with final scores
        message = f"🏆 {winner_name} wins the game! 🏆\n\nFinal Scores:\n"
        for player, score in self.scores.items():
            message += f"{player}: {score}\n"
        
        content.add_widget(Label(
            text=message,
            halign='center'
        ))
        
        # Buttons layout
        buttons = BoxLayout(size_hint_y=None, height=40, spacing=10)
        new_game_btn = Button(text='New Game')
        quit_btn = Button(text='Quit')
        buttons.add_widget(new_game_btn)
        buttons.add_widget(quit_btn)
        content.add_widget(buttons)
        
        popup = Popup(
            title='Game Over',
            content=content,
            size_hint=(None, None),
            size=(400, 300),
            auto_dismiss=False
        )
        
        def start_new_game(instance):
            popup.dismiss()
            self.scores = {name: 0 for name in self.player_names}  # Reset scores
            self.restart_game()
        
        def quit_game(instance):
            popup.dismiss()
            self.game_active = False
            self.status_bar.text = "Game Over. Click 'New Game' to play again."
        
        new_game_btn.bind(on_press=start_new_game)
        quit_btn.bind(on_press=quit_game)
        popup.open()

    def handle_round_end(self, popup, start_new_round):
        popup.dismiss()
        if start_new_round:
            # Keep the scores but reset the board and hands
            self.board = []
            self.initialize_game()
        else:
            self.game_active = False
            self.status_bar.text = "Game Over. Click 'New Game' to play again."


class DominoApp(App):
    def build(self):
        Window.size = (800, 600)
        return DominoGameGUI()

if __name__ == "__main__":
    DominoApp().run()



