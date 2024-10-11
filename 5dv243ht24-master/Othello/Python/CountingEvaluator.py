import numpy as np
from OthelloEvaluator import OthelloEvaluator

class CountingEvaluator(OthelloEvaluator):
    def evaluate(self, othello_position):
        # Use numpy to count 'B' and 'W' efficiently in the numpy array
        black_squares = np.count_nonzero(othello_position.board == 'B')
        white_squares = np.count_nonzero(othello_position.board == 'W')
        return white_squares - black_squares

class AdvancedEvaluator(OthelloEvaluator):
    positional_weights = np.array([
        [100, -10, 10, 5, 5, 10, -10, 100],
        [-10, -25, -5, -5, -5, -5, -25, -10],  # "X-squares" heavily penalized
        [10, -5, 5, 0, 0, 5, -5, 10],
        [5, -5, 0, 0, 0, 0, -5, 5],
        [5, -5, 0, 0, 0, 0, -5, 5],
        [10, -5, 5, 0, 0, 5, -5, 10],
        [-10, -25, -5, -5, -5, -5, -25, -10],  # "X-squares" penalized again
        [100, -10, 10, 5, 5, 10, -10, 100]
    ])

    # Corners, X-squares (dangerous near-corner positions), and C-squares (edges near corners)
    corners = [(1, 1), (1, 8), (8, 1), (8, 8)]  
    x_squares = [(2, 2), (2, 7), (7, 2), (7, 7)]  # Adjusting for 1-based indexing with padding
    c_squares = [(1, 2), (1, 7), (2, 1), (2, 8), (7, 1), (7, 8), (8, 2), (8, 7)]

    def evaluate(self, othello_position):
        black_squares = 0
        white_squares = 0
        black_corners = 0
        white_corners = 0
        black_positional = 0
        white_positional = 0
        black_x_squares = 0
        white_x_squares = 0
        empty_squares = 0

        # Evaluate based on pieces, corners, X-squares, and positional advantage
        for i in range(1, 9):  # Iterate over the inner 8x8 grid
            row = othello_position.board[i]  # Fetch row once to avoid repeated indexing
            for j in range(1, 9):
                item = row[j]
                if item == 'W':  # White pieces
                    white_squares += 1
                    white_positional += self.positional_weights[i - 1][j - 1]  # Adjust for 0-based index
                    if (i, j) in self.corners:
                        white_corners += 1
                    elif (i, j) in self.x_squares:
                        white_x_squares += 1  # Track X-squares for additional penalties
                elif item == 'B':  # Black pieces
                    black_squares += 1
                    black_positional += self.positional_weights[i - 1][j - 1]
                    if (i, j) in self.corners:
                        black_corners += 1
                    elif (i, j) in self.x_squares:
                        black_x_squares += 1  # Track X-squares for penalties
                else:
                    empty_squares += 1  # Count empty spaces to assess game stage

        # Dynamically adjust weights based on how many empty squares are left (i.e., game phase)
        if empty_squares > 40:  # Early game
            mobility_weight = 10
            positional_weight = 5
            corner_weight = 10
            x_square_penalty_weight = 20
            piece_weight = 2
        elif empty_squares > 20:  # Mid-game
            mobility_weight = 7
            positional_weight = 4
            corner_weight = 15
            x_square_penalty_weight = 15
            piece_weight = 3
        else:  # Late game
            mobility_weight = 5
            positional_weight = 2
            corner_weight = 25
            x_square_penalty_weight = 10
            piece_weight = 10

        # Get the moves for both players without repeatedly switching turns
        current_max_player = othello_position.maxPlayer
        white_mobility, black_mobility = 0, 0

        # Cache the move count for white and black based on the current player
        if current_max_player:
            white_mobility = len(othello_position.get_moves())  # White's legal moves
            othello_position.maxPlayer = False  # Temporarily switch to Black
            black_mobility = len(othello_position.get_moves())
            othello_position.maxPlayer = True  # Switch back
        else:
            black_mobility = len(othello_position.get_moves())  # Black's legal moves
            othello_position.maxPlayer = True  # Temporarily switch to White
            white_mobility = len(othello_position.get_moves())
            othello_position.maxPlayer = False  # Switch back

        # Heuristic calculation with dynamic weights applied
        piece_difference = piece_weight * (white_squares - black_squares)
        corner_difference = corner_weight * (white_corners - black_corners)
        mobility_difference = mobility_weight * (white_mobility - black_mobility)
        positional_difference = positional_weight * (white_positional - black_positional)
        x_square_penalty = x_square_penalty_weight * (black_x_squares - white_x_squares)

        # Combine different factors to get the final evaluation score
        evaluation_score = (
            piece_difference + 
            corner_difference + 
            mobility_difference + 
            positional_difference - 
            x_square_penalty
        )

        return evaluation_score
