import time
from OthelloAlgorithm import OthelloAlgorithm
from CountingEvaluator import CountingEvaluator
from OthelloAction import OthelloAction

class AlphaBeta(OthelloAlgorithm):
    """
    Alpha-Beta pruning algorithm with Iterative Deepening.
    Returns both the updated board state and the best move string.
    """
    OthelloAlgorithm.DefaultDepth = 3

    def __init__(self, search_depth=5, evaluator=None):
        self.search_depth = search_depth
        self.evaluator = evaluator if evaluator else CountingEvaluator()

    def set_evaluator(self, AdvancedEvaluator):
        self.evaluator = AdvancedEvaluator  # Set a different evaluator

    def set_search_depth(self, depth):
        self.search_depth = depth  # Adjust the search depth for the algorithm

    def alpha_beta(self, position, depth, alpha, beta, maximizing_player):
        """
        Alpha-Beta pruning algorithm.
        """
        if depth == 0 or position.is_game_over():
            return self.evaluator.evaluate(position), None

        legal_moves = position.get_moves()

        if not legal_moves:  # No legal moves available
            return self.evaluator.evaluate(position), OthelloAction(0, 0, is_pass_move=True)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in legal_moves:
                new_position = position.make_move(move)
                eval_score, _ = self.alpha_beta(new_position, depth - 1, alpha, beta, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in legal_moves:
                new_position = position.make_move(move)
                eval_score, _ = self.alpha_beta(new_position, depth - 1, alpha, beta, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def iterative_deepening(self, position, max_depth, time_limit):
        """
        Perform Iterative Deepening with a time limit. The search depth is increased
        incrementally until the maximum depth is reached or time runs out.
        """
        start_time = time.time()
        best_move = None

        for depth in range(1, max_depth + 1):
            # Check if time limit exceeded
            if time.time() - start_time > time_limit:
                break

            # Run Alpha-Beta with the current depth
            eval_score, move = self.alpha_beta(position, depth, float('-inf'), float('inf'), position.maxPlayer)

            # Store the best move found so far
            if move is not None:
                best_move = move

        return best_move

    def evaluate(self, position, time_limit=5):
        """
        Evaluate the best move using Iterative Deepening with a time limit.
        The search depth increases progressively until the time limit is reached.
        """
        # Perform iterative deepening with the set search depth and time limit
        best_move = self.iterative_deepening(position, self.search_depth, time_limit)

        if best_move is not None and not best_move.is_pass_move:
            move_str = f"({best_move.row},{best_move.col})"
        else:
            move_str = "pass"

        return move_str
