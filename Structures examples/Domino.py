class Domino:
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2

    def __repr__(self):
        return f"[{self.value1}|{self.value2}]"
    

    def flip(self):
        self.value1, self.value2 = self.value2, self.value1

# Generate all the domino pieces
dominoes = [Domino(i, j) for i in range(10) for j in range(i, 10)]

# Print all domino pieces
print(dominoes)

import random

# Shuffle the domino pieces
random.shuffle(dominoes)

# Print shuffled dominoes
print(dominoes)

def distribute_pieces(dominoes):
    player1 = dominoes[:10]
    player2 = dominoes[10:20]
    player3 = dominoes[20:30]
    player4 = dominoes[30:40]
    remaining_pieces = dominoes[40:]
    return player1, player2, player3, player4, remaining_pieces

# Distribute the pieces
player1, player2, player3, player4, remaining_pieces = distribute_pieces(dominoes)

# Print each player's domino pieces
print("Player 1:", player1)
print("Player 2:", player2)
print("Player 3:", player3)
print("Player 4:", player4)
print("Remaining pieces:", remaining_pieces)



# Initialize the game board with the first piece from the remaining pieces
board = [remaining_pieces.pop()] 



def play_domino(player, board):
    # Get the first and last domino values
    first_domino = board[0]
    last_domino = board[-1]
    
    for piece in player:
        # Check if piece can be connected to the start of the board
        if (piece.value1 == first_domino.value1 or 
            piece.value2 == first_domino.value1):
            player.remove(piece)
            board.insert(0, piece)  # Insert at the beginning
            return piece
        # Check if piece can be connected to the end of the board
        elif (piece.value1 == last_domino.value2 or 
              piece.value2 == last_domino.value2):
            player.remove(piece)
            board.append(piece)  # Add to the end
            return piece
    return None










 
    