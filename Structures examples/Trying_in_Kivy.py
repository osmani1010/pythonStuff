
#Main code:

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty, ListProperty
from domino_logic import Domino, AIPlayer

class DominoGameScreen(Screen):
    board = ListProperty([])
    player_hand = ListProperty([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_active = True
        self.current_player = 0
        self.players = []
        self.player_names = ["Human Player", "Computer 1", "Computer 2", "Computer 3"]
        self.consecutive_passes = 0
        self.scores = {name: 0 for name in self.player_names}
        self.ai_players = [AIPlayer() for _ in range(3)]
        self.initialize_game()

    def initialize_game(self):
        # Similar logic to your original initialize_game method
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

class DominoApp(App):
    def build(self):
        return DominoGameScreen()

if __name__ == '__main__':
    DominoApp().run()




# Kivy code:

# <DominoGameScreen>:
#     BoxLayout:
#         orientation: 'vertical'
#         padding: 10
#         spacing: 10
#
#         Label:
#             text: 'Domino Game'
#             size_hint_y: 0.1
#
#         Label:
#             text: ' '.join(str(d) for d in root.board)
#             size_hint_y: 0.2
#
#         ScrollView:
#             size_hint_y: 0.4
#             GridLayout:
#                 cols: 4
#                 spacing: 5
#                 size_hint_y: None
#                 height: self.minimum_height
#                 id: player_hand
#
#         BoxLayout:
#             size_hint_y: 0.2
#             spacing: 10
#             Button:
#                 text: 'Play Selected'
#                 on_press: root.play_domino()
#             Button:
#                 text: 'Pass'
#                 on_press: root.handle_pass()
#             Button:
#                 text: 'New Game'
#                 on_press: root.restart_game()


# Domino logic:
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

# Include the AIPlayer class here as well (same as your original code)