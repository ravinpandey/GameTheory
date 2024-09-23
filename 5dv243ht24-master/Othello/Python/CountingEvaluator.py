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
        [-10, -20, -5, -5, -5, -5, -20, -10],
        [10, -5, 5, 0, 0, 5, -5, 10],
        [5, -5, 0, 0, 0, 0, -5, 5],
        [5, -5, 0, 0, 0, 0, -5, 5],
        [10, -5, 5, 0, 0, 5, -5, 10],
        [-10, -20, -5, -5, -5, -5, -20, -10],
        [100, -10, 10, 5, 5, 10, -10, 100]
    ])

    corners = [(1, 1), (1, 8), (8, 1), (8, 8)]  # Adjusting for 1-based indexing with padding

    def evaluate(self, othello_position):
        black_squares = 0
        white_squares = 0
        black_corners = 0
        white_corners = 0
        black_positional = 0
        white_positional = 0

        # Evaluate based on pieces, corners, and positional advantage
        for i in range(1, 9):  # Iterate over the inner 8x8 grid
            row = othello_position.board[i]  # Fetch row once to avoid repeated indexing
            for j in range(1, 9):
                item = row[j]
                if item == 'W':  # White pieces
                    white_squares += 1
                    white_positional += self.positional_weights[i - 1][j - 1]  # Adjust for 0-based index
                    if (i, j) in self.corners:
                        white_corners += 1
                elif item == 'B':  # Black pieces
                    black_squares += 1
                    black_positional += self.positional_weights[i - 1][j - 1]
                    if (i, j) in self.corners:
                        black_corners += 1

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

        # Heuristic calculation with weights applied to each factor
        piece_difference = white_squares - black_squares
        corner_difference = 25 * (white_corners - black_corners)  # Corners are weighted heavily
        mobility_difference = 5 * (white_mobility - black_mobility)  # Mobility is important, but less than corners
        positional_difference = white_positional - black_positional  # Positional weighting

        # Combine different factors to get the final evaluation score
        return piece_difference + corner_difference + mobility_difference + positional_difference
