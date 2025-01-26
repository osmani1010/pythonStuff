class DominoTile:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"[{self.left}|{self.right}]"

import random

class DominoDeck:
    def __init__(self):
        self.tiles = [DominoTile(left, right) for left in range(10) for right in range(left, 10)]

    def shuffle(self):
        random.shuffle(self.tiles)

    def deal(self, num_players, num_tiles):
        hands = [self.tiles[i * num_tiles:(i + 1) * num_tiles] for i in range(num_players)]
        self.tiles = self.tiles[num_players * num_tiles:]  # Remaining tiles
        return hands

# Example usage:
#deck = DominoDeck()
#deck.shuffle()
#hands = deck.deal(4, 10)
#print(hands)

class DominoGame:
    def __init__(self, num_players):
        self.deck = DominoDeck()
        self.deck.shuffle()
        self.hands = self.deck.deal(num_players, 10)
        self.board = []

    def play_tile(self, player_index, tile_index):
        tile = self.hands[player_index].pop(tile_index)
        self.board.append(tile)

        
        if player_index < 0 or player_index >= len(self.hands):
            print("Invalid player index.")
            return False

    # Validate tile i
    
        if tile_index < 0 or tile_index >= len(self.hands[player_index]):
            print("Invalid tile index.")
            return False

    # Get the tile and check validity
        tile = self.hands[player_index][tile_index]
        if not self.is_valid_move(tile):
            print(f"Tile {tile} cannot be played.")
            return False

    # Remove the tile from the player's hand
        self.hands[player_index].pop(tile_index)

    # Flip the tile if necessary and add to the board
        if not self.can_play_tile_without_flipping(tile):
            tile.flip()
        self.board.append(tile)
        return True

    def show_board(self):
        return self.board


#Determines if a tile can be played on the current board.
    



    def can_play_tile_without_flipping(self, tile):
        right_end = self.board[-1].value2
        return tile.value1 == right_end



def main():
    num_players = 4
    game = DominoGame(num_players)

    while True:
        for i in range(num_players):
            print(f"Player {i+1}'s turn. Hand: {game.hands[i]}")
            tile_index = int(input("Select tile index to play: "))
            game.play_tile(i, tile_index)
            print(f"Board: {game.show_board()}")

if __name__ == "__main__":
    main()