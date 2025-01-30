from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import random
from domino_logic import Domino, AIPlayer

class DominoPiece(ButtonBehavior, Image):
    value1 = NumericProperty(0)
    value2 = NumericProperty(0)
    selected = ObjectProperty(False)
    
    def __init__(self, domino, **kwargs):
        super().__init__(**kwargs)
        self.value1 = domino.value1
        self.value2 = domino.value2
        self.domino = domino
        self.source = f'assets/dominoes/{self.value1}_{self.value2}.png'  # You'll need to create these images
        
    def on_press(self):
        self.selected = not self.selected
        self.opacity = 0.5 if self.selected else 1.0
        self.parent.parent.parent.selected_domino = self if self.selected else None

class DominoGameScreen(Screen):
    board = ListProperty([])
    player_hand = ListProperty([])
    current_player_name = ObjectProperty("")
    score_text = ObjectProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_active = True
        self.current_player = 0
        self.players = []
        self.player_names = ["Human Player", "Computer 1", "Computer 2", "Computer 3"]
        self.consecutive_passes = 0
        self.scores = {name: 0 for name in self.player_names}
        self.ai_players = [AIPlayer() for _ in range(3)]
        self.selected_domino = None
        self.sound_place = SoundLoader.load('assets/sounds/place.wav')
        self.sound_error = SoundLoader.load('assets/sounds/error.wav')
        self.initialize_game()

    def initialize_game(self):
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
        
    def update_display(self):
        # Update player hand display
        hand_grid = self.ids.player_hand
        hand_grid.clear_widgets()
        for domino in self.players[0]:  # Player's hand
            piece = DominoPiece(domino)
            hand_grid.add_widget(piece)
            
        # Update current player label
        self.current_player_name = f"Current Player: {self.player_names[self.current_player]}"
        
        # Update score display
        self.score_text = "Scores: " + " | ".join(f"{name}: {score}" 
                                                 for name, score in self.scores.items())

    def _find_starting_player(self):
        highest_double = -1
        starting_player = 0
        
        for player_idx, hand in enumerate(self.players):
            for piece in hand:
                if piece.value1 == piece.value2 and piece.value1 > highest_double:
                    highest_double = piece.value1
                    starting_player = player_idx
        
        return starting_player
    
    def handle_pass(self):
        self.consecutive_passes += 1
        self.status_bar.config(text=f"{self.player_names[self.current_player]} passed their turn")
        
        if self.consecutive_passes >= 4:
            self.handle_deadlock()
        else:
            self.next_turn()


    def play_domino(self):
        if not self.selected_domino:
            self.sound_error.play()
            return
            
        domino = self.selected_domino.domino
        if self._is_valid_move(domino):
            self._place_domino(domino)
            self.sound_place.play()
            self.selected_domino = None
            self._next_turn()
        else:
            self.sound_error.play()

    def _is_valid_move(self, domino):
        if not self.board:
            return True
        left_value = self.board[0].value1
        right_value = self.board[-1].value2
        return (domino.value1 == left_value or 
                domino.value2 == left_value or 
                domino.value1 == right_value or 
                domino.value2 == right_value)

    def _place_domino(self, domino):
        # Remove from player's hand
        self.players[self.current_player].remove(domino)
        
        # Add to board with animation
        if not self.board:
            self.board.append(domino)
        else:
            # Determine placement and flip if needed
            if domino.value1 == self.board[0].value1:
                domino.flip()
                self.board.insert(0, domino)
            elif domino.value2 == self.board[0].value1:
                self.board.insert(0, domino)
            elif domino.value1 == self.board[-1].value2:
                self.board.append(domino)
            elif domino.value2 == self.board[-1].value2:
                domino.flip()
                self.board.append(domino)

    def _next_turn(self):
        self.current_player = (self.current_player + 1) % 4
        self.consecutive_passes = 0
        self.update_display()
        
        if self.current_player != 0:  # AI turns
            Clock.schedule_once(self._ai_play, 1)

    def _ai_play(self, dt):
        ai_player = self.ai_players[self.current_player - 1]
        move = ai_player.make_move(self.board, self.players[self.current_player])
        if move:
            self._place_domino(move)
            self.sound_place.play()
        else:
            self.consecutive_passes += 1
        self._next_turn()

    def restart_game(self):
        self.board = []
        self.current_player = 0
        self.players = []
        self.consecutive_passes = 0
        self.initialize_game()

class DominoApp(App):
    def build(self):
        return DominoGameScreen()

if __name__ == '__main__':
    DominoApp().run()




#:kivy 2.0.0

# <DominoPiece>:
#     size_hint: None, None
#     size: "100dp", "50dp"
#     canvas.before:
#         Color:
#             rgba: (0.8, 0.8, 1, 1) if self.selected else (1, 1, 1, 1)
#         Rectangle:
#             pos: self.pos
#             size: self.size

# <DominoGameScreen>:
#     BoxLayout:
#         orientation: 'vertical'
#         padding: "10dp"
#         spacing: "10dp"
#         canvas.before:
#             Color:
#                 rgba: 0.2, 0.3, 0.4, 1
#             Rectangle:
#                 pos: self.pos
#                 size: self.size

#         Label:
#             text: 'Domino Game'
#             size_hint_y: 0.1
#             font_size: "24sp"
#             bold: True
            
#         Label:
#             text: root.current_player_name
#             size_hint_y: 0.05
            
#         Label:
#             text: root.score_text
#             size_hint_y: 0.05
            
#         ScrollView:
#             size_hint_y: 0.3
#             BoxLayout:
#                 id: board_layout
#                 size_hint_x: None
#                 width: self.minimum_width
#                 spacing: "5dp"
                
#         ScrollView:
#             size_hint_y: 0.4
#             GridLayout:
#                 cols: 4
#                 spacing: "5dp"
#                 size_hint_y: None
#                 height: self.minimum_height
#                 id: player_hand
                
#         BoxLayout:
#             size_hint_y: 0.1
#             spacing: "10dp"
#             Button:
#                 text: 'Play Selected'
#                 on_press: root.play_domino()
#                 background_color: 0.2, 0.7, 0.3, 1
#             Button:
#                 text: 'Pass'
#                 on_press: root.handle_pass()
#                 background_color: 0.7, 0.2, 0.2, 1
#             Button:
#                 text: 'New Game'
#                 on_press: root.restart_game()
#                 background_color: 0.3, 0.3, 0.7, 1


#  a folder structure 

# your_game_folder/
#     ├── main.py
#     ├── domino.kv
#     ├── domino_logic.py
#     ├── assets/
#     │   ├── dominoes/
#     │   │   ├── 0_0.png
#     │   │   ├── 0_1.png
#     │   │   └── ...
#     │   └── sounds/
#     │       ├── place.wav
#     │       └── error.wav



# For the domino images, you'll need to create PNG files for each domino combination (0_0.png through 7_7.png). You can create these using any image editing software or find free domino assets online.
# 5. For the sounds, you can find free sound effects online for the placing and error sounds.
# To make this work, you'll need to:
# Install required dependencies:
# Create the asset folders and add the necessary images and sounds
# Implement the AIPlayer class in domino_logic.py (which you already have)
