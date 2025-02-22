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
from kivy.graphics import Rectangle, Color, Ellipse, PushMatrix, PopMatrix, Line, Scale, Rotate
from kivy.properties import NumericProperty
from kivy.animation import Animation
import random

class Domino:
    def __init__(self, value1, value2):
        try:
            self.value1 = int(value1)
            self.value2 = int(value2)
            if not (0 <= self.value1 <= 6 and 0 <= self.value2 <= 6):
                raise ValueError("Domino values must be between 0 and 6")
        except ValueError:
            raise ValueError("Domino values must be valid integers between 0 and 6")

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


class DominoPiece(Button):
    rotation = NumericProperty(0)
    
    def __init__(self, domino, size = (80, 40), **kwargs):
        super().__init__(**kwargs)
        self.domino = domino
        self.size_hint = (None, None) 
        self.size = size
        
        # if domino.value1 == domino.value2:
        #     self.size = (size[1], size[0])
        # else:
        #     self.size = size
        self.is_vertical = domino.value1 == domino.value2  # Track if its a double piece
        self.background_normal = ''
        self.background_color = (0.95, 0.95, 0.95, 0.1)  # Slightly off-white
        self.dots_color = (0, 0, 0, 1)  # Pure black for better contrast
        self.text = ''
        

        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.bind(rotation=self.update_canvas)
        if domino.value1 == domino.value2:
           
            self.rotation = 90
        #     # self.pos_hint = {'center_y': 0.5}

            self.update_canvas()

    def rotate(self):
        self.is_vertical = not self.is_vertical
        
    def get_size(self):
        if self.is_vertical:
            return self.size[1], self.size[0]

        return self.size

    def update_canvas(self, *args):
        self.canvas.before.clear()
        self.canvas.after.clear()
        
        with self.canvas.before:


            PushMatrix()
            Rotate(angle=self.rotation, origin=self.center)
            
            # Draw white background
            Color(0.95, 0.95, 0.95, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            # Draw black border
            Color(0, 0, 0, 1)
            Line(rectangle=(self.x, self.y, self.width, self.height), width=2.0)
            
            # Draw dividing line
            Line(points=[self.center_x, self.y, self.center_x, self.y + self.height], width=2.0)
            
            # Draw dots
            self._draw_dots(self.domino.value1, 'left')
            self._draw_dots(self.domino.value2, 'right')
            
        with self.canvas.after:
            PopMatrix()

   

    def _draw_dots(self, value, side):
        dot_size = min(self.width, self.height) / 6  # Increased dot size
        
        # Calculate the center of each half
        half_width = self.width / 2
        if side == 'left':
            base_x = self.x + half_width / 2
        else:
            base_x = self.x + half_width + half_width / 2
            
        base_y = self.y + self.height / 2
        
        # Define relative positions for dots (values from -0.5 to 0.5)
        dot_layouts = {
            1: [(0, 0)],
            2: [(-0.3, 0.3), (0.3, -0.3)],
            3: [(-0.3, 0.3), (0, 0), (0.3, -0.3)],
            4: [(-0.3, 0.3), (-0.3, -0.3), (0.3, 0.3), (0.3, -0.3)],
            5: [(-0.3, 0.3), (-0.3, -0.3), (0, 0), (0.3, 0.3), (0.3, -0.3)],
            # Two columns of three dots each
            6: [(-0.3, 0.3), (0, 0.3), (0.3, 0.3),  # Left column
            (-0.3, -0.3), (0, -0.3), (0.3, -0.3)]     # Right column       
    
        }

        # Draw the dots
        Color(*self.dots_color)
        spacing = min(half_width, self.height) * 0.8  # Reduced spacing
        
        if value in dot_layouts:
            for dx, dy in dot_layouts[value]:
                x = base_x + dx * spacing - dot_size / 2
                y = base_y + dy * spacing - dot_size / 2
                Ellipse(pos=(x, y), size=(dot_size, dot_size))


class BoardLayout(BoxLayout):
    def __init__(self, gap=5, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 0
        self.padding = 0
        self.size_hint_y = None
        self.width = 600
        self.height = 450
        self.gap = gap
        self.pieces = []

        self.left_spacer = Widget(size_hint_x=0.3)
        self.add_widget(self.left_spacer)
        
        # Create a center anchor widget
        self.center_layout = BoxLayout(orientation='horizontal', spacing=0, size_hint_x=None,
                                        pos_hint={'center_x': 0.5, 'center_y': 1})
            
        self.center_layout.bind(minimum_width=self.center_layout.setter('width'))
        # self.add_widget(Widget(size_hint_x=0.5))
        self.add_widget(self.center_layout)
        
        self.right_spacer = Widget(size_hint_x=0.3)
        self.add_widget(self.right_spacer)

     
    def add_piece(self, domino, position='end'):
        piece = Domino(domino.value1, domino.value2)
        domino_widget = DominoPiece(piece)
        

        # Special handling for the first piece
        if not self.pieces:
            self.center_layout.add_widget(domino_widget)
            self.pieces.append(domino_widget)
            return

        # Get the last piece's position and size
        last_piece = self.pieces[-1]

        if domino_widget not in self.pieces: 

        # Calculate the new position based on the previous piece
            if position == 'end':
                # Adjust spacing for double pieces
                if last_piece.is_vertical or domino_widget.is_vertical:
                    padding = -20
                    
                    new_x = last_piece.x + last_piece.width + padding  # Adjust spacing for double pieces
                
                else:
                    padding = 0
                    new_x = last_piece.x + last_piece.width 
                new_y = last_piece.y
                
            else:
                first_piece = self.pieces[0]
                if first_piece.is_vertical or domino_widget.is_vertical:
                    padding = -20
                    new_x = first_piece.x - domino_widget.width + padding  # Adjust spacing for double pieces
                    
                else:
                    padding = 0
                    new_x = first_piece.x - domino_widget.width 
                new_y = first_piece.y

        # Set the position of the new piece
        domino_widget.pos = (new_x, new_y)
        print(f"new position: {new_x}, {new_y}")
        # Apply margin by wrapping the domino_widget in another layout
        piece_wrapper = BoxLayout(size_hint=(None, None), size=(domino_widget.width + padding, domino_widget.height),
                                 padding=(padding if position == 'end' else 0, 0) )
       
        piece_wrapper.add_widget(domino_widget)

        # Add the new piece to the layout and list
        if position == 'start':
            self.center_layout.add_widget(piece_wrapper, index=0) 
            self.pieces.insert(0, domino_widget)
        else:
            self.center_layout.add_widget(piece_wrapper)
            self.pieces.append(domino_widget)

        # Update spacer widths based on layout width
        spacer_width = (1.0 - self.center_layout.width / self.width) / 2 if self.width else 0.5
        self.left_spacer.size_hint_x = spacer_width
        self.right_spacer.size_hint_x = spacer_width

    def clear(self):
        self.center_layout.clear_widgets()
        self.pieces = []

    
class DominoGameGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_piece_index = None
        self.orientation = 'horizontal'  # Change to horizontal to have left menu
        self.padding = 2
        self.spacing = 0

        # Create left menu layout
        left_menu = BoxLayout(
            orientation='vertical',
            size_hint_x=0.15,  # Take 20% of horizontal space
            padding=5,
            spacing=5
        )

        # Create menu button that will show/hide the cascade
        self.menu_button = Button(
            text='Menu ▼',
            size_hint_y=None,
            height=30,
            background_color=(0.3, 0.5, 0.7, 1)
        )
        self.menu_button.bind(on_press=self.toggle_menu)

        # Create cascade menu container
        self.cascade_container = GridLayout(
            cols=1,
            size_hint_y=None,
            height=0,  # Start hidden
            opacity=0
        )

        # Create menu buttons
        menu_buttons = [
            ('New Game', self.restart_game),
            ('Game Modes', self.show_game_modes),
            ('Settings', self.show_difficulty_settings),
            ('Exit Game', self.confirm_exit)
        ]

        for text, callback in menu_buttons:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=25,
                background_color=(0.4, 0.6, 0.8, 1)
            )
            btn.bind(on_press=callback)
            self.cascade_container.add_widget(btn)

        # Add menu button and cascade container to left menu
        left_menu.add_widget(self.menu_button)
        left_menu.add_widget(self.cascade_container)
        left_menu.add_widget(Widget())  # Spacer to push menu to top

        # Create main content layout
        main_content = BoxLayout(orientation='vertical')

        # Add existing widgets to main content
        self.game_modes = {
            'Classic': {
                'description': 'First to empty hand wins round',
                'rules': 'Win by being first to play all your dominoes'
            },
            'Block': {
                'description': 'Lowest sum wins when game is blocked',
                'rules': 'When no one can play, lowest pip sum wins'
            },
            'Points': {
                'description': 'Play to target score, collect opponent pips',
                'rules': 'Score points equal to sum of opponents remaining pips'
            }
        }
        
        self.current_mode = 'Classic'
        self.target_score = 100

        # Add existing game state variables and GUI elements to main_content
        self.board = []
        self.current_player = 0
        self.players = []
        self.player_names = ["Human Player", "Computer 1", "Computer 2", "Computer 3"]
        self.consecutive_passes = 0
        self.scores = {name: 0 for name in self.player_names}
        self.ai_players = [AIPlayer() for _ in range(3)]
        self.game_active = True
        self.winner = None
        self.passes_per_player = {name: 0 for name in self.player_names}

        # Score display
        self.score_label = Label(text="Scores:", size_hint_y=0.1, font_size=18, bold=True)
        main_content.add_widget(self.score_label)

        # Board display
         
        board_container = BoxLayout(orientation='vertical', size_hint_y=None, height=500)
        self.board_layout = BoardLayout()
        self.board_layout.pos_hint = {'center_x': 0.5}  # Center the board horizontally
        
        self.board_label = Label(text="Board", size_hint_y=0.1, font_size=20, bold=True)
        board_container.add_widget(self.board_label)
        
        board_container.add_widget(self.board_layout)
        main_content.add_widget(board_container)
        
        self.board_display = Label(text="", size_hint_y=0.2)
        
        # board_container = BoxLayout(orientation='vertical', size_hint_y=None, height=450)
        
        board_container.add_widget(self.board_display)
        # main_content.add_widget(board_container)
        # main_content.add_widget(self.board_layout)
        
        
       
        # Player hand display

        self.hand_layout = BoxLayout(orientation='vertical', size_hint_y=0.1)
        self.hand_label = Label(text="Your pieces:", size_hint_y=0.05, font_size=18, bold=True)
    
        # Create a horizontal container for the grid and spacers
        grid_container = BoxLayout(orientation='horizontal')
        
        # Add left spacer (takes 20% of width)
        grid_container.add_widget(Widget(size_hint_x=0.35))
        
        self.pieces_grid = GridLayout(
            cols=8,
            spacing=10,
            padding=5,
            size_hint_x=0.3,  # Grid takes 60% of width
            size_hint_y=0.9,
            height=80,
            row_default_height=80,
            col_default_width=40,
            col_force_default=True,
            row_force_default=True
        )
        
        grid_container.add_widget(self.pieces_grid)
        
        # Add right spacer (takes 20% of width)
        grid_container.add_widget(Widget(size_hint_x=0.35))
        
        hand_container = BoxLayout(orientation='vertical', size_hint_y=0.3)
        hand_container.add_widget(self.hand_label)
        hand_container.add_widget(grid_container)  # Add the grid container instead of pieces_grid directly
        main_content.add_widget(hand_container)

        # Add play and pass buttons at the bottom
        button_row = BoxLayout(size_hint_y=0.1, size_hint_x=0.8, spacing=10)
        
        # Create a center container for the buttons
        button_container = BoxLayout(
            size_hint_x=0.1,  # Take 40% of the width
            spacing=10,
            pos_hint={'center_x': 0.5}  # Center the container
        )
        
        # Make buttons smaller
        self.play_button = Button(
            text="Play Selected Piece",
            size_hint=(None, None),
            size=(160, 40),  # Fixed width and height
            pos_hint={'center_y': 0.3}  # Center vertically

        )
        self.play_button.bind(on_press=self.play_domino)
        
        self.pass_button = Button(
            text="Pass Turn",
            size_hint=(None, None),
            size=(100, 40),  # Fixed width and height
            pos_hint={'center_y': 0.3}  # Center vertically
        )
        self.pass_button.bind(on_press=self.handle_pass)
        
        # Add buttons to the container
        button_container.add_widget(self.play_button)
        button_container.add_widget(self.pass_button)
        
        # Add spacers on either side to center the container
        button_row.add_widget(Widget())  # Left spacer
        button_row.add_widget(button_container)
        button_row.add_widget(Widget())  # Right spacer
        
        main_content.add_widget(button_row)

        # Status bar
        self.status_bar = Label(
            text="Ready to play",
            size_hint_y=0.1,
            height=40,
            color=(1, 1, 1, 1),
            bold=True,
        )
        main_content.add_widget(self.status_bar)

        # Add left menu and main content to root layout
        self.add_widget(left_menu)
        self.add_widget(main_content)

        self.initialize_game()

    def toggle_menu(self, *args):
        if self.cascade_container.height == 0:
            # Show menu
            self.cascade_container.height = 44 * len(self.cascade_container.children)
            self.cascade_container.opacity = 1
            self.menu_button.text = 'Menu ▲'
        else:
            # Hide menu
            self.cascade_container.height = 0
            self.cascade_container.opacity = 0
            self.menu_button.text = 'Menu ▼'


    def update_display(self):
        # Update board display
        self.board_layout.clear()
        # # Then add each piece
        for piece in self.board:
            self.board_layout.add_piece(piece)

        # Update pieces grid
        self.pieces_grid.clear_widgets()
        for i, piece in enumerate(self.players[0]):
            piece_widget = DominoPiece(
                piece,
                size=(80, 40),
                size_hint=(None, None),
                pos_hint={},
                background_color=(0.95, 0.95, 0.95, 0.1) if self.current_player == 0 
                else (0.7, 0.7, 0.7, 1)

            )
            piece_widget.rotation = 90
            

            piece_widget.piece_index = i
            if self.current_player == 0:
                piece_widget.bind(on_press=self.select_piece)
            if i == self.selected_piece_index and self.current_player == 0:
                piece_widget.background_color = (0.2, 0.4, 0.2, 0.1)
            self.pieces_grid.add_widget(piece_widget)

    # Update labels
        self.hand_label.text = "Your pieces: (Waiting for other players)" if self.current_player != 0 else "Your pieces: Your turn!"
        self.status_bar.text = f"Current turn: {self.player_names[self.current_player]}"
        
        #Enable/disable pass button based on current player
        self.pass_button.disabled = self.current_player != 0
        score_text = " | ".join(f"{name}: {score}" for name, score in self.scores.items())
        self.score_label.text = f"Scores: {score_text}"

        # self.board_display.text = " ".join(str(d) for d in self.board)

    def select_piece(self, button):
        for child in self.pieces_grid.children:
            child.background_color = (0.3, 0.3, 0.3, 0.1) if self.current_player == 0 else (0.7, 0.7, 0.7, 1)
        
        # Update selected piece index and highlight the selected piece
        self.selected_piece_index = button.piece_index
        button.background_color = (0.2, 0.7, 0.2, 0.5)  # Highlight selected piece

    def show_difficulty_settings(self, *args):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Store buttons in a dictionary to access them later
        difficulty_buttons = {}
        
        for i, ai_player in enumerate(self.ai_players):
            row = BoxLayout(spacing=10, size_hint_y=None, height=40)
            row.add_widget(Label(text=f"Computer {i+1}:", size_hint_x=0.4))
            
            # Store buttons for this AI player
            difficulty_buttons[i] = {}
            
            for difficulty in ['easy', 'medium', 'hard']:
                btn = Button(
                    text=difficulty,
                    size_hint_x=0.2,
                )
                
                # Update button color based on current difficulty
                if ai_player.difficulty == difficulty:
                    btn.background_color = (0.3, 0.6, 0.9, 1)
                else:
                    btn.background_color = (0.3, 0.5, 0.4, 0.9)
                
                # Store button reference
                difficulty_buttons[i][difficulty] = btn
                
                # Create update function that updates all button colors
                def update_difficulty(btn, idx=i, diff=difficulty, buttons=difficulty_buttons):
                    # Update AI difficulty
                    self.ai_players[idx].difficulty = diff
                    
                    # Update button colors for this AI player
                    for d, b in buttons[idx].items():
                        if d == diff:
                            b.background_color = (0.3, 0.6, 0.9, 1)
                        else:
                            b.background_color = (0.3, 0.5, 0.4, 0.9)
                    

                    self.show_popup("Success", f"Computer {idx + 1} difficulty updated to {diff}")
                
                btn.bind(on_press=update_difficulty)
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
        
    
    def initialize_game(self):
        self.game_active = True
        self.winner = None
        self.consecutive_passes = 0

        # Generate dominoes
        try:
            dominoes = [Domino(i, j) for i in range(7) for j in range(i, 7)]
            random.shuffle(dominoes)

            # Distribute pieces
            self.players = [
                dominoes[:6],
                dominoes[6:12],
                dominoes[12:18],
                dominoes[18:24]
            ]

            

            # If this is the first game or game mode changed, find starting player based on highest double
            if not hasattr(self, 'last_winner') or not hasattr(self, 'last_mode') or self.last_mode != self.current_mode:
                self.current_player = self._find_starting_player()
            else:
                # Make the last winner the starting player only if continuing in same mode
                self.current_player = self.last_winner


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



    def restart_game(self, *args):
        if self.game_active:
            # Show confirmation popup
            content = BoxLayout(orientation='vertical', padding=10)
            content.add_widget(Label(text="Are you sure you want to end the current game\nand start a new one?"))
            
            buttons = BoxLayout(size_hint_y=0.4, spacing=10)
            yes_button = Button(text='Yes')
            no_button = Button(text='No')
            buttons.add_widget(yes_button)
            buttons.add_widget(no_button)
            content.add_widget(buttons)
            
            popup = Popup(
                title='Confirm New Game',
                content=content,
                size_hint=(None, None),
                size=(400, 200),
                auto_dismiss=False
            )
            
            def confirm_restart(instance):
                popup.dismiss()
                self._perform_restart()
                
            def cancel_restart(instance):
                popup.dismiss()
            
            yes_button.bind(on_press=confirm_restart)
            no_button.bind(on_press=cancel_restart)
            popup.open()
        else:
            self._perform_restart()

    def _perform_restart(self):
            self.board = []
            self.current_player = 0
            self.players = []
            self.consecutive_passes = 0
            # Reset passes tracking
            self.passes_per_player = {name: 0 for name in self.player_names}
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
            self.board_layout.clear()
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
                self.selected_piece_index = None #Reset highlight
                self.update_display()
           
        return False
   

    def _try_play_piece(self, piece, piece_index, first_domino, last_domino):
        current_player_hand = self.players[self.current_player]

        def play_with_flip(flip_needed, position):
            if flip_needed:
                piece.flip()
            
            current_player_hand.pop(piece_index)
            if position == 'start':
                self.board.insert(0, piece)
            else:
                self.board.append(piece)
            

           
            for domino_widget in self.board_layout.pieces:
                if domino_widget.domino == piece:
                    if flip_needed:
                        anim = Animation(rotation=360, duration=1)
                    def on_flip_complete(anim, widget):
                        anim.bind(on_complete=on_flip_complete)
                        anim.start(domino_widget)
                    break
            return True


        if self.current_player == 0:
             # Special case: If it's the last piece and both ends have same number
            if len(current_player_hand) == 1 and first_domino.value1 == last_domino.value2:
                # Always play at the end of the board in this case
                if piece.value1 == last_domino.value2:
                    # return play_with_flip(False, 'end')
                    current_player_hand.pop(piece_index)
                    self.board.append(piece)
                    return True
                if piece.value2 == last_domino.value2:
                    # return play_with_flip(True, 'end')
                    piece.flip()
                    current_player_hand.pop(piece_index)
                    self.board.append(piece)
                    return True

            if len(current_player_hand) == 1 and first_domino.value1 != last_domino.value2:
                if piece.value1 == last_domino.value2:
                    # return play_with_flip(False, 'end')
                    current_player_hand.pop(piece_index)
                    self.board.append(piece)
                    return True
                if piece.value2 == last_domino.value2:
                    # return play_with_flip(True, 'end')
                    piece.flip()
                    current_player_hand.pop(piece_index)
                    self.board.append(piece)
                    return True
                

            if len(self.board) > 1:
                if first_domino.value1 == last_domino.value2 and (
                    piece.value1 == first_domino.value1 or 
                    piece.value2 == first_domino.value1):
                    self.show_side_choice_popup(piece, piece_index)
                    self.selected_piece_index = None #Reset highlight
                    self.update_display()
                    return False
            
                if first_domino.value1 != last_domino.value2 and (
                    piece.value1 == last_domino.value2 and
                    piece.value2 == first_domino.value1 or 
                    piece.value1 == first_domino.value1 and piece.value2 == last_domino.value2):
                    self.show_side_choice_popup(piece, piece_index)
                    self.selected_piece_index = None #Reset highlight
                    self.update_display()
                    return False


            # When adding piece to board, specify position
            # Try to play at the start of the board
            if piece.value2 == first_domino.value1:
                # return play_with_flip(False, 'start')
                current_player_hand.pop(piece_index)
                self.board.insert(0, piece)
                self.board_layout.add_piece(piece, position='start') 
                return True
            if piece.value1 == first_domino.value1:
                # return play_with_flip(True, 'start')
                piece.flip()
                current_player_hand.pop(piece_index)
                self.board.insert(0, piece)
                self.board_layout.add_piece(piece, position='start') 
                return True

            # Try to play at the end of the board
            if piece.value1 == last_domino.value2:
                # return play_with_flip(False, 'end')
                current_player_hand.pop(piece_index)
                self.board.append(piece)
                self.board_layout.add_piece(piece, position='end')
                return True
            if piece.value2 == last_domino.value2:
                # return play_with_flip(True, 'end')
                piece.flip()
                current_player_hand.pop(piece_index)
                self.board.append(piece)
                self.board_layout.add_piece(piece, position='end')
                return True
            return False

            

        # For AI players
        else:
            if piece.value2 == first_domino.value1:
                # return play_with_flip(False, 'start')
                current_player_hand.pop(piece_index)
                self.board.insert(0, piece)
                self.board_layout.add_piece(piece, position='start')
                return True
            if piece.value1 == first_domino.value1:
                # return play_with_flip(True, 'start')
                piece.flip()
                current_player_hand.pop(piece_index)
                self.board.insert(0, piece)
                self.board_layout.add_piece(piece, position='start')
                return True

            # Try to play at the end of the board
            if piece.value1 == last_domino.value2:
                # return play_with_flip(False, 'end')
                current_player_hand.pop(piece_index)
                self.board.append(piece)
                self.board_layout.add_piece(piece, position='end')
                return True
            if piece.value2 == last_domino.value2:
                # return play_with_flip(True, 'end')
                piece.flip()
                current_player_hand.pop(piece_index)
                self.board.append(piece)
                self.board_layout.add_piece(piece, position='end')
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

    def handle_pass(self, *args):
    # For human player, check if they have any valid moves
        if self.current_player == 0:
            # Check if there are any valid moves available
            has_valid_move = False
            if not self.board:
                # If board is empty, player can't pass as they can play any piece
                self.show_popup("Invalid Pass", "You must play a piece when the board is empty!")
                return
            else:
                for piece in self.players[0]:
                # Check if piece can be played at either end
                    if piece.value1 == self.board[0].value1 or \
                    piece.value2 == self.board[0].value1 or \
                    piece.value1 == self.board[-1].value2 or \
                    piece.value2 == self.board[-1].value2:
                        has_valid_move = True
                        break
                
            if has_valid_move:
                self.show_popup("Invalid Pass", "You have valid moves available!")
                return
        # If we get here, either it's an AI player or human player with no valid moves
        self.consecutive_passes += 1
        self.passes_per_player[self.player_names[self.current_player]] += 1
        
        # Create and show the temporary pass popup
        if self.current_player == 0:
            content = Label(
                text=f"You passed your turn",
                size_hint_y=None,
                height=40
            )
        else:
            content = Label(
                text=f"{self.player_names[self.current_player]} passed their turn",
                size_hint_y=None,
                height=40
            )
        
        pass_popup = Popup(
            title='Pass',
            content=content,
            size_hint=(None, None),
            size=(300, 100),
            auto_dismiss=True
        )
        pass_popup.open()
        
        # Schedule the popup to close after 1 second
        Clock.schedule_once(pass_popup.dismiss, 1)

        if self.consecutive_passes >= 4:
            if self.current_mode == 'Block':
                self.handle_block_deadlock()

            elif self.current_mode == 'Points':
                self.handle_points_deadlock()
            else:  # Classic mode
                self.handle_classic_deadlock()
        else:
            self.next_turn()
        

    def handle_classic_deadlock(self):
        player_sums = [self.calculate_player_sum(p) for p in self.players]
        min_sum = min(player_sums)
        
        # Find all players with the minimum sum
        min_sum_indices = [i for i, sum_value in enumerate(player_sums) if sum_value == min_sum]
        
        if len(min_sum_indices) > 1:
            # First tiebreaker: fewest passes
            min_passes = min(self.passes_per_player[self.player_names[i]] for i in min_sum_indices)
            min_pass_indices = [i for i in min_sum_indices 
                            if self.passes_per_player[self.player_names[i]] == min_passes]
            
            if len(min_pass_indices) > 1:
                # Second tiebreaker: player position (earlier player wins)
                winner_index = min(min_pass_indices)
            else:
                winner_index = min_pass_indices[0]
        else:
            winner_index = player_sums.index(min_sum)

        # Update scores for the winner
        self.scores[self.player_names[winner_index]] += 1

        # Update winner information for the next round
        self.last_winner = winner_index
        self.last_mode = self.current_mode

        result_message = "Game is blocked!\n\n"
        result_message += "In Classic mode, when the game is blocked, the player with the lowest pip sum wins.\n\n"
        for i, sum_value in enumerate(player_sums):
            result_message += f"{self.player_names[i]} total: {sum_value} (Passes: {self.passes_per_player[self.player_names[i]]})\n"
        
        if len(min_sum_indices) > 1:
            if len(min_pass_indices) > 1:
                result_message += f"\n{self.player_names[winner_index]} wins with the lowest sum of {min_sum}, "
                result_message += f"fewest passes ({self.passes_per_player[self.player_names[winner_index]]}) "
                result_message += "and earliest player position!"
            else:
                result_message += f"\n{self.player_names[winner_index]} wins with the lowest sum of {min_sum} "
                result_message += f"and fewest passes ({self.passes_per_player[self.player_names[winner_index]]})!"
        else:
            result_message += f"\n{self.player_names[winner_index]} wins with the lowest sum of {min_sum}!"
            
        result_message += "\n\nWould you like to start a new round?"

        self._show_deadlock_popup("Classic Game Blocked", result_message)


    def handle_points_deadlock(self):
        player_sums = [self.calculate_player_sum(p) for p in self.players]
        min_sum = min(player_sums)
        
        # Find all players with the minimum sum
        min_sum_indices = [i for i, sum_value in enumerate(player_sums) if sum_value == min_sum]
        
        if len(min_sum_indices) > 1:
            # First tiebreaker: fewest passes
            min_passes = min(self.passes_per_player[self.player_names[i]] for i in min_sum_indices)
            min_pass_indices = [i for i in min_sum_indices 
                            if self.passes_per_player[self.player_names[i]] == min_passes]
            
            if len(min_pass_indices) > 1:
                # Second tiebreaker: player position (earlier player wins)
                winner_index = min(min_pass_indices)
            else:
                winner_index = min_pass_indices[0]
        else:
            winner_index = player_sums.index(min_sum)

        # Calculate total points from all remaining dominoes
        total_points = sum(player_sums)
        
        # Award points to the winner
        self.scores[self.player_names[winner_index]] += total_points

        # Store winner information for the next round
        self.last_winner = winner_index
        self.last_mode = self.current_mode

        result_message = "Game is blocked!\n\n"
        result_message += "In Points mode, when the game is blocked, the player with the lowest pip sum wins all remaining points.\n\n"
        for i, sum_value in enumerate(player_sums):

            result_message += f"{self.player_names[i]} total: {sum_value} (Passes: {self.passes_per_player[self.player_names[i]]})\n"
        
        if len(min_sum_indices) > 1:
            if len(min_pass_indices) > 1:
                result_message += f"\n{self.player_names[winner_index]} wins with the lowest sum of {min_sum}, "
                result_message += f"fewest passes ({self.passes_per_player[self.player_names[winner_index]]}) "
                result_message += "and earliest player position!"
            else:
                result_message += f"\n{self.player_names[winner_index]} wins with the lowest sum of {min_sum} "
                result_message += f"and fewest passes ({self.passes_per_player[self.player_names[winner_index]]})!"
        else:
            result_message += f"\n{self.player_names[winner_index]} wins with the lowest sum of {min_sum}!"
        
        result_message += f"\nPoints awarded: {total_points}"
        
        if self.scores[self.player_names[winner_index]] >= self.target_score:
            self.show_final_winner_popup(self.player_names[winner_index])
        else:
            result_message += "\n\nWould you like to start a new round?"
            self._show_deadlock_popup("Points Game Blocked", result_message)
    

    def handle_block_deadlock(self):
        player_sums = [self.calculate_player_sum(p) for p in self.players]
        min_sum = min(player_sums)
        
        # Find all players with the minimum sum
        min_sum_indices = [i for i, sum_value in enumerate(player_sums) if sum_value == min_sum]
        
        if len(min_sum_indices) > 1:
            # First tiebreaker: fewest passes
            min_passes = min(self.passes_per_player[self.player_names[i]] for i in min_sum_indices)
            min_pass_indices = [i for i in min_sum_indices 
                            if self.passes_per_player[self.player_names[i]] == min_passes]
            
            if len(min_pass_indices) > 1:
                # Second tiebreaker: player position (earlier player wins)
                winner_index = min(min_pass_indices)
            else:
                winner_index = min_pass_indices[0]
        else:
            winner_index = player_sums.index(min_sum)

        # Update scores for the winner
        self.scores[self.player_names[winner_index]] += 1

        # Store winner information for the next round
        self.last_winner = winner_index
        self.last_mode = self.current_mode

        result_message = "Block Game Deadlock!\n\n"
        result_message += "In Block mode, the player with the lowest pip sum wins when the game is blocked.\n\n"
        for i, sum_value in enumerate(player_sums):

            result_message += f"{self.player_names[i]} total: {sum_value} (Passes: {self.passes_per_player[self.player_names[i]]})\n"
        
        if len(min_sum_indices) > 1:
            if len(min_pass_indices) > 1:
                result_message += f"\n{self.player_names[winner_index]} wins with the lowest sum of {min_sum}, "
                result_message += f"fewest passes ({self.passes_per_player[self.player_names[winner_index]]}) "
                result_message += "and earliest player position!"
            else:
                result_message += f"\n{self.player_names[winner_index]} wins with the lowest sum of {min_sum} "
                result_message += f"and fewest passes ({self.passes_per_player[self.player_names[winner_index]]})!"
        else:
            result_message += f"\n{self.player_names[winner_index]} wins with the lowest sum of {min_sum}!"
            
        result_message += "\n\nWould you like to start a new round?"

        self._show_deadlock_popup("Block Game Blocked", result_message)

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
            title='Block Game Over',
            content=content,
            size_hint=(None, None),
            size=(500, 400),  # Made larger to accommodate the longer message
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


    def _show_deadlock_popup(self, title, message):
        # Set game as inactive when deadlock occurs
        self.game_active = False
       

        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message))
        
        buttons = BoxLayout(size_hint_y=0.4, spacing=10)
        yes_button = Button(text='Yes')
        no_button = Button(text='No')
        buttons.add_widget(yes_button)
        buttons.add_widget(no_button)
        content.add_widget(buttons)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(500, 400),
            auto_dismiss=False
        )
        
        def on_yes(instance):
            popup.dismiss()
            #Temporaly set game active to False
            self.game_active = False
            # self.restart_game()
            self._perform_restart()
            

        def on_no(instance):
            popup.dismiss()
            self.game_active = False
            self.status_bar.text = "Game Over. Click 'New Game' to play again."
        
        yes_button.bind(on_press=on_yes)
        no_button.bind(on_press=on_no)
        popup.open()


    def next_turn(self):
        self.current_player = (self.current_player + 1) % 4
        self.selected_piece_index = None #Reset selection


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
            self.status_bar.text = f"{self.player_names[self.current_player]} is passing"  
            self.handle_pass()

    def show_game_modes(self, *args):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Store buttons in a dictionary
        mode_buttons = {}
        
        for mode, details in self.game_modes.items():
            row = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=80)
            btn = Button(
                text=f"{mode}\n{details['description']}\n{details['rules']}",
                size_hint_y=None,
                height=70
            )
            
            # Set initial button color based on current mode
            if mode == self.current_mode:
                btn.background_color = (0.3, 0.6, 0.9, 1)
            else:
                btn.background_color = (0.3, 0.5, 0.4, 0.9)
            
            # Store button reference
            mode_buttons[mode] = btn
            
            # Create update function that updates all button colors
            def update_mode(btn, selected_mode=mode, buttons=mode_buttons):
                # Update all button colors
                for m, b in buttons.items():
                    if m == selected_mode:
                        b.background_color = (0.3, 0.6, 0.9, 1)
                    else:
                        b.background_color = (0.3, 0.5, 0.4, 0.9)
                
                # Change game mode
                self.current_mode = selected_mode
                self.scores = {name: 0 for name in self.player_names}  # Reset scores
                if hasattr(self, 'last_mode'):
                    self.last_mode = None  # Reset last mode to force highest double start
                
                # Temporarily set game active to False
                was_active = self.game_active
                self.game_active = False
                self._perform_restart()
                self.show_popup("Game Mode Changed", 
                              f"Changed to {selected_mode} mode\n{self.game_modes[selected_mode]['description']}")
            
            btn.bind(on_press=update_mode)
            row.add_widget(btn)
            content.add_widget(row)

        if self.current_mode == 'Points':
            score_input = BoxLayout(size_hint_y=None, height=20)
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
            size=(550, 400),
        )
        
        close_button.bind(on_press=popup.dismiss)
        content.add_widget(close_button)
        popup.open()


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
            elif self.current_mode == 'Block':
                # For Block mode, handle blocked game differently
                if self.consecutive_passes >= 4:
                    # self.handle_deadlock()
                    self.handle_block_deadlock()
                else:
                    self.scores[self.player_names[self.current_player]] += 1
                    self.show_round_winner_popup(self.player_names[self.current_player])
            else:  # Classic mode
                self.scores[self.player_names[self.current_player]] += 1
                self.show_round_winner_popup(self.player_names[self.current_player])


    def show_round_winner_popup(self, winner_name, points=None):
        # Set game as inactive when round is won
        self.game_active = False
        # Store the winner's index for the next round
        self.last_winner = self.player_names.index(winner_name)
        self.last_mode = self.current_mode

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
        # Set game as inactive when round is won
        self.game_active = False
        # Store the winner's index for the next round
        self.last_winner = self.player_names.index(winner_name)
        self.last_mode = self.current_mode


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

    def confirm_exit(self, *args):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Are you sure you want to exit the game?"))
        
        buttons = BoxLayout(size_hint_y=0.4, spacing=10)
        yes_button = Button(text='Yes')
        no_button = Button(text='No')
        buttons.add_widget(yes_button)
        buttons.add_widget(no_button)
        content.add_widget(buttons)
        
        popup = Popup(
            title='Confirm Exit',
            content=content,
            size_hint=(None, None),
            size=(300, 200),
            auto_dismiss=False
        )
        
        def exit_game(instance):
            from kivy.core.window import Window
            from kivy.app import App
            popup.dismiss()
            App.get_running_app().stop()
            Window.close()
        
        yes_button.bind(on_press=exit_game)
        no_button.bind(on_press=popup.dismiss)
        popup.open()


class DominoApp(App):
    def build(self):
        Window.size = (800, 600)
        return DominoGameGUI()

if __name__ == "__main__":
    DominoApp().run()




           