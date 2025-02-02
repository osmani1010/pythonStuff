# Add these imports at the top
from kivy.uix.screenmanager import ScreenManager, Screen
import socket
import json
import threading
from kivy.app import App
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

    


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(
            text='Domino Game', 
            font_size='24sp',
            size_hint_y=0.3
        )
        
        # Game mode buttons
        singleplayer_btn = Button(
            text='Single Player vs AI',
            size_hint_y=0.15,
            on_press=self.start_singleplayer
        )
        
        local_multiplayer_btn = Button(
            text='Local Multiplayer',
            size_hint_y=0.15,
            on_press=self.start_local_multiplayer
        )
        
        online_btn = Button(
            text='Online Matchmaking',
            size_hint_y=0.15,
            on_press=self.show_online_options
        )
        
        layout.add_widget(title)
        layout.add_widget(singleplayer_btn)
        layout.add_widget(local_multiplayer_btn)
        layout.add_widget(online_btn)
        
        self.add_widget(layout)

    def start_singleplayer(self, *args):
        game_screen = self.manager.get_screen('game')
        game_screen.initialize_game(mode='singleplayer')
        self.manager.current = 'game'

    def start_local_multiplayer(self, *args):
        game_screen = self.manager.get_screen('game')
        game_screen.initialize_game(mode='local_multiplayer')
        self.manager.current = 'game'

    def show_online_options(self, *args):
        self.manager.current = 'online_menu'

class OnlineMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(
            text='Online Matchmaking',
            font_size='24sp',
            size_hint_y=0.3
        )
        
        host_btn = Button(
            text='Host Game',
            size_hint_y=0.15,
            on_press=self.host_game
        )
        
        join_btn = Button(
            text='Join Game',
            size_hint_y=0.15,
            on_press=self.show_join_dialog
        )
        
        back_btn = Button(
            text='Back to Menu',
            size_hint_y=0.15,
            on_press=lambda x: setattr(self.manager, 'current', 'menu')
        )
        
        layout.add_widget(title)
        layout.add_widget(host_btn)
        layout.add_widget(join_btn)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)

    def host_game(self, *args):
        # We'll implement this later
        pass

    def show_join_dialog(self, *args):
        # We'll implement this later
        pass

# Modify the DominoApp class
class DominoApp(App):
    def build(self):
        Window.size = (800, 600)
        sm = ScreenManager()
        
        menu_screen = MenuScreen(name='menu')
        game_screen = DominoGameGUI(name='game')
        online_menu = OnlineMenuScreen(name='online_menu')
        
        sm.add_widget(menu_screen)
        sm.add_widget(game_screen)
        sm.add_widget(online_menu)
        
        return sm

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


   
class DominoGameGUI(Screen):  # Change from BoxLayout to Screen
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.main_layout)
        
        self.game_mode = None
        self.selected_piece_index = None
        self.setup_gui()
        
    def initialize_game(self, mode='singleplayer'):
        self.game_mode = mode
        self.game_active = True
        self.winner = None
        self.consecutive_passes = 0
        
        if mode == 'singleplayer':
            self.player_names = ["Human Player", "Computer 1", "Computer 2", "Computer 3"]
            self.ai_players = [AIPlayer() for _ in range(3)]
        elif mode == 'local_multiplayer':
            self.player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]
            self.ai_players = []
        elif mode == 'online':
            # We'll implement online logic later
            pass
            
        self.scores = {name: 0 for name in self.player_names}
        self.setup_game()
        
    def setup_game(self):
        # Generate and distribute dominoes
        try:
            dominoes = [Domino(i, j) for i in range(8) for j in range(i, 8)]
            random.shuffle(dominoes)
            
            self.players = [
                dominoes[:8],
                dominoes[8:16],
                dominoes[16:24],
                dominoes[24:32]
            ]
            
            self.current_player = self._find_starting_player()
            self.board = []
            
            self.update_display()
            
            # Auto-play for AI in singleplayer mode
            if self.game_mode == 'singleplayer' and self.current_player != 0:
                Clock.schedule_once(lambda dt: self.handle_ai_turn(), 1)
                
        except Exception as e:
            self.show_popup("Error", f"Failed to initialize game: {e}")