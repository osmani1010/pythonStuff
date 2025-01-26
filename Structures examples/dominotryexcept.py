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

# Generate all the domino pieces
try:
    dominoes = [Domino(i, j) for i in range(10) for j in range(i, 10)]
except ValueError as e:
    print(f"Error generating dominoes: {e}")
    exit(1)


import random

# Shuffle the domino pieces
random.shuffle(dominoes)


def distribute_pieces(dominoes):
    
    try:
        if len(dominoes) < 40:
            raise ValueError("Not enough dominoes to distribute")
        player1 = dominoes[:10]
        player2 = dominoes[10:20]
        player3 = dominoes[20:30]
        player4 = dominoes[30:40]
        remaining_pieces = dominoes[40:]
        
        return player1, player2, player3, player4, remaining_pieces
    except Exception as e:
        print(f"Error distributing pieces: {e}")
        
# Distribute the pieces  
try: 
    player1, player2, player3, player4, remaining_pieces = distribute_pieces(dominoes)
except TypeError:
    print("Error when distributing pieces")
    exit(1)

# Print each player's domino pieces
print("Player 1:", player1)
print("Player 2:", player2)
print("Player 3:", player3)
print("Player 4:", player4)
print("Remaining pieces:", remaining_pieces)   
    

def play_domino(player, board):
    if not board:
        raise ValueError("Board cannot be empty")
    if not player:
        return False
    
    first_domino = board[0]
    last_domino = board[-1]
        
    for piece in player:
            # Check if piece can be connected to the start of the board
        if piece.value1 == first_domino.value1:
            piece.flip()  # Flip to match
            player.remove(piece)
            board.insert(0, piece)
            return True
        elif piece.value2 == first_domino.value1:
            player.remove(piece)
            board.insert(0, piece)
            return True
        # Check if piece can be connected to the end of the board
        elif piece.value1 == last_domino.value2:
            player.remove(piece)
            board.append(piece)
            return True
        elif piece.value2 == last_domino.value2:
            piece.flip()  # Flip to match
            player.remove(piece)
            board.append(piece)
            return True       
    return False

def calculate_player_sum(player):
    return sum(piece.value1 + piece.value2 for piece in player)

def play_game():
    if not remaining_pieces:
        raise ValueError("No remaining pieces to start the board")
    try:
        board = [remaining_pieces.pop()]
    except IndexError:
        raise ValueError("No pieces available to start the board")

    current_player = 0
    players = [player1, player2, player3, player4]
    player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]
    consecutive_passes = 0
        

    # Validate initial game state
    if any(not isinstance(p, list) for p in players):
        raise ValueError("Invalid player hands")
    
    while True:
        
        
        print("\nBoard:", *board)
        print(f"\n{player_names[current_player]}'s turn")
        print("Your pieces:", players[current_player])
            
        if not play_domino(players[current_player], board):
            print("No valid moves. Passing turn...")
            consecutive_passes += 1
        else:
            consecutive_passes = 0
                
         # Check win condition
        if len(players[current_player]) == 0:
            print(f"\n{player_names[current_player]} wins!")
            break
            
        # Check deadlock condition (all players passed)
        if consecutive_passes >= 4:
            print("\nGame is deadlocked! No more valid moves possible.")
            # Calculate sums for each player
            player_sums = [calculate_player_sum(p) for p in players]
            min_sum = min(player_sums)
            winner_index = player_sums.index(min_sum)
            
            # Print final scores
            for i, sum_value in enumerate(player_sums):
                print(f"{player_names[i]} total: {sum_value}")
            
            print(f"\n{player_names[winner_index]} wins with the lowest sum of {min_sum}!")
            break
            
        current_player = (current_player + 1) % 4

if __name__ == "__main__":
    try:
        play_game()
    except Exception as e:
        print(f"Game error: {e}")





