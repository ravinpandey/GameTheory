from OthelloAlgorithm import OthelloAlgorithm
from CountingEvaluator import CountingEvaluator
from CountingEvaluator import AdvancedEvaluator 
from OthelloAction import OthelloAction
from OthelloEvaluator import OthelloEvaluator
#from logger_config import logger  # Import the logger

class AlphaBeta(OthelloAlgorithm):
    """
    Implementation of the Alpha-Beta pruning algorithm.
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

    def evaluate(self, position):
        def alpha_beta(position, depth, alpha, beta, maximizing_player):
            # Terminal or depth condition
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
                    eval_score, _ = alpha_beta(new_position, depth - 1, alpha, beta, False)
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
                    eval_score, _ = alpha_beta(new_position, depth - 1, alpha, beta, True)
                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_move = move
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
                return min_eval, best_move

        # Call the alpha-beta pruning algorithm starting with the full depth
        score, best_move = alpha_beta(position, self.search_depth, float('-inf'), float('inf'), position.maxPlayer)

        # Handle case where best_move is None (which should never happen because pass moves are handled)
        if best_move is not None and not best_move.is_pass_move:
            move_str = f"({best_move.row},{best_move.col})"
        else:
            move_str = "pass"

        return move_str
