#:kivy 2.0.0
from kivy.app import app

< DominoPiece >:
    size_hint: None, None
    size: "100dp", "50dp"
    canvas.before:
        Color:
    rgba: (0.8, 0.8, 1, 1) if self.selected else (1, 1, 1, 1)
Rectangle:
pos: self.pos
size: self.size

< DominoGameScreen >:
BoxLayout:
orientation: 'vertical'
padding: "10dp"
spacing: "10dp"
canvas.before:
Color:
rgba: 0.2, 0.3, 0.4, 1
Rectangle:
pos: self.pos
size: self.size

Label:
text: 'Domino Game'
size_hint_y: 0.1
font_size: "24sp"
bold: True

Label:
text: root.current_player_name
size_hint_y: 0.05

Label:
text: root.score_text
size_hint_y: 0.05

ScrollView:
size_hint_y: 0.3
BoxLayout:
id: board_layout
size_hint_x: None
width: self.minimum_width
spacing: "5dp"

ScrollView:
size_hint_y: 0.4
GridLayout:
cols: 4
spacing: "5dp"
size_hint_y: None
height: self.minimum_height
id: player_hand

BoxLayout:
size_hint_y: 0.1
spacing: "10dp"
Button:
text: 'Play Selected'
on_press: root.play_domino()
background_color: 0.2, 0.7, 0.3, 1
Button:
text: 'Pass'
on_press: root.handle_pass()
background_color: 0.7, 0.2, 0.2, 1
Button:
text: 'New Game'
on_press: root.restart_game()
background_color: 0.3, 0.3, 0.7, 1