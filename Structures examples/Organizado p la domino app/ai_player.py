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
    
    # def _can_play_piece(self, piece, first_domino, last_domino):
    #     # Check if piece can be played at the start of the board
    #     # (should match first_domino.value1)
    #     # or at the end of the board (should match last_domino.value2)
    #     return (piece.value1 == first_domino.value1 or
    #             piece.value2 == first_domino.value1 or
    #             piece.value1 == last_domino.value2 or
    #             piece.value2 == last_domino.value2)    
    