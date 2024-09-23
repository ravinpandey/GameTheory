import sys
from OthelloPosition import OthelloPosition
from OthelloAction import OthelloAction
from AlphaBeta import AlphaBeta

def get_best_action(othello_position):
    """
    This function calculates the best move for the current player using AlphaBeta pruning.
    Ensures the move is either "pass" or in the correct format "(row,col)".
    """
    alpha_beta = AlphaBeta()  # Initialize AlphaBeta algorithm
    move_str = alpha_beta.evaluate(othello_position)

    # Validate the move string to ensure it's either "pass" or "(row,col)"
    if move_str == "pass":
        return "pass"
    elif move_str.startswith("(") and move_str.endswith(")"):
        row_col = move_str.strip("()")
        row, col = map(int, row_col.split(','))
        return move_str
    else:
        raise ValueError(f"Invalid move string: {move_str}")

def main():
    # Read the command line arguments: board position and time limit
    if len(sys.argv) < 3:
        raise ValueError("Insufficient arguments. Usage: python Othello.py <position> <time_limit>")
    
    position = sys.argv[1]  # The 65-character board position
    #position = "BOOOOOOOXOOEOOOXXOOOOOOOXOOOOOOOOOOOOOXOXOOOOEEOEOOOOEXOOOOEEEEOE"
    time_limit = int(sys.argv[2])  # The time limit in seconds
    
    # Initialize the Othello position with the provided board state
    othello_position = OthelloPosition(position)
    
    # Get the best action (this will be a move string)
    move_str = get_best_action(othello_position)

    # Output only the move, in the required format (either "pass" or "(row,col)")
    print(move_str, flush=True)

if __name__ == "__main__":
    main()
