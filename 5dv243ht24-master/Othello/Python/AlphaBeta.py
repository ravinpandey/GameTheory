import numpy as np
import time
import hashlib
from OthelloAlgorithm import OthelloAlgorithm
from CountingEvaluator import CountingEvaluator
from OthelloAction import OthelloAction

class AlphaBeta(OthelloAlgorithm):
    """
    Alpha-Beta pruning with Transposition Tables and time constraints.
    Returns both the updated board state and the best move string.
    """
    OthelloAlgorithm.DefaultDepth = 3

    def __init__(self, search_depth=5, evaluator=None):
        self.search_depth = search_depth
        self.evaluator = evaluator if evaluator else CountingEvaluator()
        self.transposition_table = {}  # Initialize the transposition table
        self.start_time = None         # Track start time as a class-level variable
        self.time_limit = None         # Track time limit as a class-level variable

    def set_evaluator(self, AdvancedEvaluator):
        self.evaluator = AdvancedEvaluator  # Set a different evaluator

    def set_search_depth(self, depth):
        self.search_depth = depth  # Adjust the search depth for the algorithm

    def board_hash(self, position):
        """Generate a hash for the board position to store in the transposition table."""
        return hashlib.md5(position.board.tobytes()).hexdigest()

    def time_exceeded(self):
        """Check if the time limit has been exceeded."""
        return time.time() - self.start_time > self.time_limit - 0.1  # Safety margin of 0.1s

    def quick_evaluate(self, position):
        """A simpler evaluation function used for faster evaluation in deeper levels."""
        return np.count_nonzero(position.board == 'W') - np.count_nonzero(position.board == 'B')

    def alpha_beta(self, position, depth, alpha, beta, maximizing_player):
        """
        Alpha-Beta pruning algorithm with Transposition Tables and time constraints.
        """
        # Frequent time check at each recursion level
        if self.time_exceeded():
            return None, None
        
        # Generate a unique hash for the current board state
        board_key = self.board_hash(position)

        # Check if the board state is already in the transposition table
        if board_key in self.transposition_table:
            cached_value = self.transposition_table[board_key]
            if cached_value['depth'] >= depth:  # Use cached value only if it's from a deeper or equal search
                return cached_value['score'], cached_value['move']

        # Terminal or depth condition
        if depth == 0 or position.is_game_over():
            # Use simpler evaluation if depth is deeper to save time
            eval_score = self.quick_evaluate(position) if depth > 2 else self.evaluator.evaluate(position)
            self.transposition_table[board_key] = {'score': eval_score, 'move': None, 'depth': depth}
            return eval_score, None

        legal_moves = position.get_moves()
        if not legal_moves:  # No legal moves available
            eval_score = self.quick_evaluate(position)
            self.transposition_table[board_key] = {'score': eval_score, 'move': OthelloAction(0, 0, is_pass_move=True), 'depth': depth}
            return eval_score, OthelloAction(0, 0, is_pass_move=True)

        # Prioritize moves with quick evaluation for better Alpha-Beta pruning
        legal_moves.sort(key=lambda move: self.quick_evaluate(position.make_move(move)), reverse=True)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in legal_moves:
                if self.time_exceeded():
                    return max_eval, best_move  # Early exit if time is up

                new_position = position.make_move(move)
                eval_score, _ = self.alpha_beta(new_position, depth - 1, alpha, beta, False)

                if eval_score is None:  # Time exceeded check
                    return max_eval, best_move

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break

            self.transposition_table[board_key] = {'score': max_eval, 'move': best_move, 'depth': depth}
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in legal_moves:
                if self.time_exceeded():
                    return min_eval, best_move  # Early exit if time is up

                new_position = position.make_move(move)
                eval_score, _ = self.alpha_beta(new_position, depth - 1, alpha, beta, True)

                if eval_score is None:  # Time exceeded check
                    return min_eval, best_move

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break

            self.transposition_table[board_key] = {'score': min_eval, 'move': best_move, 'depth': depth}
            return min_eval, best_move

    def iterative_deepening(self, position, max_depth):
        """
        Perform Iterative Deepening with a time limit and Transposition Tables.
        The search depth is increased incrementally until the maximum depth is reached or time runs out.
        """
        best_move = None

        for depth in range(1, max_depth + 1):
            if self.time_exceeded():
                break  # Stop if time has exceeded

            remaining_time = self.time_limit - (time.time() - self.start_time)
            if remaining_time < 0.1:  # Stop deeper searches if less than 100ms remaining
                break

            eval_score, move = self.alpha_beta(position, depth, float('-inf'), float('inf'), position.maxPlayer)

            if eval_score is None:
                return best_move  # Return the best move found so far if time runs out

            if move is not None:
                best_move = move  # Update best move for this depth

        return best_move

    def evaluate(self, position, time_limit=5):
        """
        Evaluate the best move using Iterative Deepening with a time limit.
        Initializes the start time and time limit for time management.
        """
        self.start_time = time.time()  # Set the start time when evaluation begins
        self.time_limit = time_limit   # Set the time limit

        # Perform iterative deepening
        best_move = self.iterative_deepening(position, self.search_depth)

        if best_move is not None and not best_move.is_pass_move:
            return f"({best_move.row},{best_move.col})"
        else:
            return "pass"
