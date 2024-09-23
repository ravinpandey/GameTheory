from OthelloEvaluator import OthelloEvaluator

"""
  A simple evaluator that just counts the number of black and white squares 
  Author: Ola Ringdahl
"""

class CountingEvaluator(OthelloEvaluator):
    def evaluate(self, othello_position):
        black_squares = 0
        white_squares = 0
        for row in othello_position.board:
            for item in row:
                if item == 'W':  # White pieces
                    white_squares += 1
                if item == 'B':  # Black pieces
                    black_squares += 1
        return white_squares - black_squares
    

class AdvancedEvaluator(OthelloEvaluator):
    # Positional weights based on strategic value of the board positions
    positional_weights = [
        [100, -10, 10, 5, 5, 10, -10, 100],
        [-10, -20, -5, -5, -5, -5, -20, -10],
        [10, -5, 5, 0, 0, 5, -5, 10],
        [5, -5, 0, 0, 0, 0, -5, 5],
        [5, -5, 0, 0, 0, 0, -5, 5],
        [10, -5, 5, 0, 0, 5, -5, 10],
        [-10, -20, -5, -5, -5, -5, -20, -10],
        [100, -10, 10, 5, 5, 10, -10, 100]
    ]

    def evaluate(self, othello_position):
        black_squares = 0
        white_squares = 0
        black_corners = 0
        white_corners = 0
        black_mobility = 0
        white_mobility = 0
        black_positional = 0
        white_positional = 0

        # Define corners (adjusting to the inner 8x8 grid)
        corners = [(1, 1), (1, 8), (8, 1), (8, 8)]  # Adjusting for 1-based indexing with padding

        # Evaluate based on pieces, corners, and positional advantage
        for i in range(1, 9):  # Iterate over the inner 8x8 grid
            for j in range(1, 9):
                item = othello_position.board[i][j]
                if item == 'W':  # White pieces
                    white_squares += 1
                    white_positional += self.positional_weights[i - 1][j - 1]  # Adjust for 0-based index in positional_weights
                    if (i, j) in corners:
                        white_corners += 1
                elif item == 'B':  # Black pieces
                    black_squares += 1
                    black_positional += self.positional_weights[i - 1][j - 1]  # Adjust for 0-based index in positional_weights
                    if (i, j) in corners:
                        black_corners += 1

        # Get the moves for both players
        if othello_position.maxPlayer:  # If it's White's turn
            white_mobility = len(othello_position.get_moves())  # Get White's legal moves

            # Temporarily switch to Black's turn to count Black's moves
            othello_position.maxPlayer = False
            black_mobility = len(othello_position.get_moves())  # Get Black's legal moves
            othello_position.maxPlayer = True  # Switch back to White
        else:  # If it's Black's turn
            black_mobility = len(othello_position.get_moves())  # Get Black's legal moves

            # Temporarily switch to White's turn to count White's moves
            othello_position.maxPlayer = True
            white_mobility = len(othello_position.get_moves())  # Get White's legal moves
            othello_position.maxPlayer = False  # Switch back to Black

        # Heuristic calculation with weights applied to each factor
        piece_difference = white_squares - black_squares
        corner_difference = 25 * (white_corners - black_corners)  # Corners are weighted heavily
        mobility_difference = 5 * (white_mobility - black_mobility)  # Mobility is important, but less than corners
        positional_difference = white_positional - black_positional  # Positional weighting

        # Combine different factors to get the final evaluation score
        return piece_difference + corner_difference + mobility_difference + positional_difference
