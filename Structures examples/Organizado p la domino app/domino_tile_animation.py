import tkinter as tk
from tkinter import messagebox
import random
import math

class DominoTile(tk.Canvas):
    def __init__(self, parent, value1, value2, size=60):
        super().__init__(parent, width=size*2, height=size, bg='white', highlightthickness=1)
        self.size = size
        self.value1 = value1
        self.value2 = value2
        self.draw_domino()
        
    def draw_domino(self):
        # Draw domino outline
        self.create_rectangle(2, 2, self.size*2-2, self.size-2, width=2)
        self.create_line(self.size, 2, self.size, self.size-2, width=2)
        
        # Draw dots for each half
        self.draw_dots(self.value1, 0)
        self.draw_dots(self.value2, self.size)
        
    def draw_dots(self, value, x_offset):
        dot_positions = {
            0: [],
            1: [(0.5, 0.5)],
            2: [(0.3, 0.3), (0.7, 0.7)],
            3: [(0.3, 0.3), (0.5, 0.5), (0.7, 0.7)],
            4: [(0.3, 0.3), (0.3, 0.7), (0.7, 0.3), (0.7, 0.7)],
            5: [(0.3, 0.3), (0.3, 0.7), (0.5, 0.5), (0.7, 0.3), (0.7, 0.7)],
            6: [(0.3, 0.3), (0.3, 0.5), (0.3, 0.7), (0.7, 0.3), (0.7, 0.5), (0.7, 0.7)]
        }
        
        dot_radius = self.size * 0.08
        for px, py in dot_positions[value]:
            x = x_offset + px * self.size
            y = py * self.size
            self.create_oval(x-dot_radius, y-dot_radius, x+dot_radius, y+dot_radius, fill='black')

class DominoGameGUI:
    def __init__(self, root):
        // ... existing code ...
        self.animation_speed = 15  # Lower is faster
        self.animation_in_progress = False
        // ... existing code ...

    def setup_gui(self):
        // ... existing code ...
        
        # Create canvas for board
        self.board_canvas = tk.Canvas(self.root, width=800, height=200, bg='#e0e0e0')
        self.board_canvas.pack(pady=20)
        
        # Create frame for dominoes in play
        self.domino_frame = tk.Frame(self.board_canvas)
        self.board_canvas.create_window(400, 100, window=self.domino_frame)
        
        # Dictionary to store domino widgets
        self.domino_widgets = []
        
        // ... existing code ...

    def animate_domino_placement(self, domino, start_pos, end_pos, is_start=False):
        if not hasattr(self, 'animation_step'):
            self.animation_step = 0
            
        # Calculate animation parameters
        dx = (end_pos[0] - start_pos[0]) / 20
        dy = (end_pos[1] - start_pos[1]) / 20
        
        # Current position
        current_x = start_pos[0] + (dx * self.animation_step)
        current_y = start_pos[1] + (dy * self.animation_step)
        
        # Move domino to current position
        domino.place(x=current_x, y=current_y)
        
        self.animation_step += 1
        
        if self.animation_step < 20:
            # Continue animation
            self.root.after(self.animation_speed, 
                          lambda: self.animate_domino_placement(domino, start_pos, end_pos, is_start))
        else:
            # Animation complete
            self.animation_step = 0
            self.animation_in_progress = False
            self.update_display()

    def place_domino_on_board(self, piece, is_start=False):
        # Create new domino widget
        domino_widget = DominoTile(self.domino_frame, piece.value1, piece.value2)
        self.domino_widgets.append(domino_widget)
        
        # Calculate positions
        start_y = 300  # Start position (below board)
        end_y = 0     # End position on board
        
        if is_start:
            # Adding to start of board
            end_x = 400 - (len(self.board) * 65)  # 65 pixels per domino
            start_x = end_x
        else:
            # Adding to end of board
            end_x = 400 + (len(self.board) * 65)
            start_x = end_x
            
        # Start animation
        self.animation_in_progress = True
        domino_widget.place(x=start_x, y=start_y)
        self.animate_domino_placement(domino_widget, (start_x, start_y), (end_x, end_y), is_start)

    def _try_play_piece(self, piece, piece_index, first_domino, last_domino):
        """Attempt to play a piece at either end of the board."""
        current_player_hand = self.players[self.current_player]

        # Try to play at the start of the board
        if piece.value2 == first_domino.value1:
            current_player_hand.pop(piece_index)
            self.board.insert(0, piece)
            self.place_domino_on_board(piece, is_start=True)
            return True
            
        if piece.value1 == first_domino.value1:
            piece.flip()
            current_player_hand.pop(piece_index)
            self.board.insert(0, piece)
            self.place_domino_on_board(piece, is_start=True)
            return True
        
        # Try to play at the end of the board
        if piece.value1 == last_domino.value2:
            current_player_hand.pop(piece_index)
            self.board.append(piece)
            self.place_domino_on_board(piece, is_start=False)
            return True
            
        if piece.value2 == last_domino.value2:
            piece.flip()
            current_player_hand.pop(piece_index)
            self.board.append(piece)
            self.place_domino_on_board(piece, is_start=False)
            return True
        
        return False

    def clear_board_display(self):
        # Clear all domino widgets
        for widget in self.domino_widgets:
            widget.destroy()
        self.domino_widgets = []

    def restart_game(self):
        self.clear_board_display()
        // ... existing code ...




   #Add rotation animations:

    def animate_domino_rotation(self, domino_widget, start_angle, end_angle):
        if not hasattr(self, 'rotation_step'):
            self.rotation_step = 0
            
        current_angle = start_angle + ((end_angle - start_angle) * self.rotation_step / 20)
        domino_widget.rotate(current_angle)
        
        self.rotation_step += 1
        
        if self.rotation_step < 20:
            self.root.after(self.animation_speed, 
                        lambda: self.animate_domino_rotation(domino_widget, start_angle, end_angle))
        else:
            self.rotation_step = 0




    def calculate_bounce_position(self, progress):
    # Add a small bounce at the end of the animation
    if progress > 0.8:
        bounce = math.sin((progress - 0.8) * 5 * math.pi) * 10
        return bounce
    return 0