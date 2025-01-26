import random

class Domino:
    def __init__(self, value1, value2):
        try:
            self.value1 = int(value1)
            self.value2 = int(value2)
        except ValueError:
            raise ValueError("Domino values must be integers")

   
    def __repr__(self):
        return f"[{self.value1}|{self.value2}]"
    

    def flip(self):
        self.value1, self.value2 = self.value2, self.value1

class DominoGame:
    def __init__(self):
        try:
            # Generate all domino pieces
            self.dominoes = [Domino(i, j) for i in range(10) for j in range(i, 10)]
            random.shuffle(self.dominoes)
            self.players = self.distribute_pieces(self.dominoes)
            self.board = []
            self.remaining_pieces = self.dominoes[40:]
        except ValueError as e:
            raise ValueError(f"Error initializing game: {e}")

    def distribute_pieces(self, dominoes):
        try:
            if len(dominoes) < 40:
                raise ValueError("Not enough dominoes to distribute")
            return [
                dominoes[:10],
                dominoes[10:20],
                dominoes[20:30],
                dominoes[30:40]
            ]
        except Exception as e:
            raise ValueError(f"Error distributing pieces: {e}")

    def play_domino(self, player, board):
        self.player = player
        self.board = board
        if not self.board:
            raise ValueError("Board cannot be empty")
        if not self.player:
            return False

        first_domino = self.board[0]
        last_domino = self.board[-1]
        
        for piece in self.player:
            # Check if piece can be connected to the start of the board
            if piece.value1 == first_domino.value1:
                piece.flip()  # Flip to match
                self.player.remove(piece)
                self.board.insert(0, piece)
                return True
            elif piece.value2 == first_domino.value1:
                self.player.remove(piece)
                self.board.insert(0, piece)
                return True
            # Check if piece can be connected to the end of the board
            elif piece.value1 == last_domino.value2:
                self.player.remove(piece)
                self.board.append(piece)
                return True
            elif piece.value2 == last_domino.value2:
                piece.flip()  # Flip to match
                self.player.remove(piece)
                self.board.append(piece)
                return True       
        return False



    def calculate_player_sum(self, player):
        return sum(piece.value1 + piece.value2 for piece in player)

    def play_game(self):
        if not self.remaining_pieces:
            raise ValueError("No remaining pieces to start the board")
        try:
            self.board = [self.remaining_pieces.pop()]
        except IndexError:
            raise ValueError("No pieces available to start the board")

        current_player = 0
        player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]
        consecutive_passes = 0

        # Validate initial game state
        if any(not isinstance(p, list) for p in self.players):
            raise ValueError("Invalid player hands")
        
        while True:
            print("\nBoard:", *self.board)
            print(f"\n{player_names[current_player]}'s turn")
            print("Your pieces:", self.players[current_player])
                
            if not self.play_domino(self.players[current_player], self.board):
                print("No valid moves. Passing turn...")
                consecutive_passes += 1
            else:
                consecutive_passes = 0
                    
            # Check win condition
            if len(self.players[current_player]) == 0:
                print(f"\n{player_names[current_player]} wins!")
                return player_names[current_player]
                
            # Check deadlock condition (all players passed)
            if consecutive_passes >= 4:
                print("\nGame is deadlocked! No more valid moves possible.")
                # Calculate sums for each player
                player_sums = [self.calculate_player_sum(p) for p in self.players]
                min_sum = min(player_sums)
                winner_index = player_sums.index(min_sum)
                
                # Print final scores
                for i, sum_value in enumerate(player_sums):
                    print(f"{player_names[i]} total: {sum_value}")
                
                print(f"\n{player_names[winner_index]} wins with the lowest sum of {min_sum}!")
                return player_names[winner_index]
                
            current_player = (current_player + 1) % 4

if __name__ == "__main__":
    try:
        game = DominoGame()
        winner = game.play_game()
    except Exception as e:
        print(f"Game error: {e}")






    