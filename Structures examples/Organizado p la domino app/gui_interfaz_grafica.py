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
