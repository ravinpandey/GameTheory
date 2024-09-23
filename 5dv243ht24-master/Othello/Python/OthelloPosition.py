import numpy as np
from OthelloAction import OthelloAction

class OthelloPosition(object):
    """
    This class represents the board positions and handles the application of moves.
    """

    def __init__(self, board_str=""):
        """
        Initializes the board with a given string, or creates an empty board if none is provided.
        :param board_str: A string of length 65 representing the board (1 char for player, 64 for board).
        """
        self.BOARD_SIZE = 8
        self.maxPlayer = True  # True represents White, False represents Black
        self.board = np.array([['E' for col in range(self.BOARD_SIZE + 2)] for row in range(self.BOARD_SIZE + 2)])
        
        if board_str and len(board_str) == 65:  # Ensure the board string is exactly 65 characters long
            # First character indicates current player (B or W)
            self.maxPlayer = board_str[0] == 'W'
            # Remaining 64 characters represent the 8x8 board
            for i in range(1, 65):
                col = ((i - 1) % 8) + 1
                row = (i - 1) // 8 + 1
                self.board[row][col] = 'B' if board_str[i] == 'X' else 'W' if board_str[i] == 'O' else 'E'
        else:
            # If no valid board_str is passed, initialize a new game state
            self.initialize()  # Initialize the starting position

        self.board_history = []  # Store previous board states to detect cycles

    def initialize(self):
        """
        Initializes the starting position on the board and returns the board string.
        """
        self.board[self.BOARD_SIZE // 2][self.BOARD_SIZE // 2] = 'W'
        self.board[self.BOARD_SIZE // 2 + 1][self.BOARD_SIZE // 2 + 1] = 'W'
        self.board[self.BOARD_SIZE // 2][self.BOARD_SIZE // 2 + 1] = 'B'
        self.board[self.BOARD_SIZE // 2 + 1][self.BOARD_SIZE // 2] = 'B'
        self.maxPlayer = True
        self.board_history = []  # Reset board history when game starts
        return self.get_board_string()  # Now returns the 65-character board string

    def get_board_string(self):
        """
        Converts the current board and player's turn back to a 65-character string.
        :return: A string representing the current player and the board.
        """
        player_turn = 'W' if self.maxPlayer else 'B'
        board_str = ''.join(['X' if cell == 'B' else 'O' if cell == 'W' else 'E' for row in self.board[1:9] for cell in row[1:9]])
        return player_turn + board_str

    def make_move(self, action):
        """
        Perform the move suggested by the OthelloAction and return the new board position.
        :param action: The move to make as an OthelloAction.
        :return: The OthelloPosition resulting from making the move.
        """
        if action.is_pass_move:
            new_position = self.clone()
            new_position.maxPlayer = not self.maxPlayer
            return new_position

        row, col = action.row, action.col
        new_position = self.clone()

        # Place the player's disc on the board
        new_position.board[row][col] = 'W' if self.maxPlayer else 'B'

        # Flip the opponent's discs in all valid directions
        new_position.__flip_discs(row, col)

        # Switch the player
        new_position.maxPlayer = not self.maxPlayer

        return new_position

    def get_moves(self):
        """
        Get all possible moves for the current player.
        :return: A list of OthelloAction representing all possible moves.
        """
        moves = []
        for i in range(1, self.BOARD_SIZE + 1):
            for j in range(1, self.BOARD_SIZE + 1):
                if self.__is_candidate(i, j) and self.__is_move(i, j):
                    move = OthelloAction(i, j)
                    moves.append(move)
        if not moves:
            moves.append(OthelloAction(0, 0, is_pass_move=True))
        return moves

    def __flip_discs(self, row, col):
        """
        Flip the opponent's discs in all directions from the (row, col).
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            self.__flip_in_direction(row, col, dr, dc)

    def __flip_in_direction(self, row, col, dr, dc):
        """
        Flip opponent's discs in a specific direction, if valid flipping sequence exists.
        """
        opponent = 'B' if self.maxPlayer else 'W'
        player = 'W' if self.maxPlayer else 'B'
        r, c = row + dr, col + dc
        discs_to_flip = []

        while 1 <= r <= self.BOARD_SIZE and 1 <= c <= self.BOARD_SIZE and self.board[r][c] == opponent:
            discs_to_flip.append((r, c))
            r += dr
            c += dc

        if 1 <= r <= self.BOARD_SIZE and 1 <= c <= self.BOARD_SIZE and self.board[r][c] == player:
            for flip_r, flip_c in discs_to_flip:
                self.board[flip_r][flip_c] = player

    def __is_candidate(self, row, col):
        """
        Check if a position is a candidate for a move (empty and has neighboring opponent discs).
        :param row: The row of the board position.
        :param col: The column of the board position.
        :return: True if it is a candidate for a move.
        """
        if self.board[row][col] != 'E':  # The cell must be empty to be a candidate
            return False
        return self.__has_neighbour(row, col)

    def __is_move(self, row, col):
        """
        Check if placing a disc at (row, col) is a valid move.
        :param row: The row of the board position.
        :param col: The column of the board position.
        :return: True if placing a disc at (row, col) is a valid move.
        """
        if row < 1 or row > self.BOARD_SIZE or col < 1 or col > self.BOARD_SIZE:
            return False
        return self.__check_move_in_all_directions(row, col)

    def __has_neighbour(self, row, col):
        """
        Check if the position has neighboring discs.
        :param row: The row of the board position.
        :param col: The column of the board position.
        :return: True if it has neighboring discs.
        """
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if self.board[row + dr][col + dc] != 'E':
                    return True
        return False

    def __check_move_in_all_directions(self, row, col):
        """
        Check if placing a disc at (row, col) will flip opponent discs in any direction.
        :param row: The row of the board position.
        :param col: The column of the board position.
        :return: True if placing a disc at (row, col) is a valid move.
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            if self.__can_flip_in_direction(row, col, dr, dc):
                return True
        return False

    def __can_flip_in_direction(self, row, col, dr, dc):
        """
        Check if placing a disc at (row, col) will flip opponent discs in the given direction.
        :param row: The row of the board position.
        :param col: The column of the board position.
        :param dr: Row direction.
        :param dc: Column direction.
        :return: True if placing a disc will flip opponent discs in the given direction.
        """
        opponent = 'B' if self.maxPlayer else 'W'
        player = 'W' if self.maxPlayer else 'B'
        r, c = row + dr, col + dc
        discs_to_flip = []

        while 1 <= r <= self.BOARD_SIZE and 1 <= c <= self.BOARD_SIZE and self.board[r][c] == opponent:
            discs_to_flip.append((r, c))
            r += dr
            c += dc

        if 1 <= r <= self.BOARD_SIZE and 1 <= c <= self.BOARD_SIZE and self.board[r][c] == player:
            return True

        return False

    def is_repeated_state(self):
        """
        Check if the current board state has already occurred.
        :return: True if this board state has been seen before, False otherwise.
        """
        current_board_string = self.get_board_string()
        if current_board_string in self.board_history:
            return True
        self.board_history.append(current_board_string)
        return False

    def is_game_over(self):
        """
        Check if the game is over. The game ends when neither player has a valid move.
        :return: True if the game is over, False otherwise.
        """
        current_player_moves = self.get_moves()

        # Switch to the other player
        self.maxPlayer = not self.maxPlayer
        other_player_moves = self.get_moves()
        self.maxPlayer = not self.maxPlayer

        return len(current_player_moves) == 1 and current_player_moves[0].is_pass_move and \
               len(other_player_moves) == 1 and other_player_moves[0].is_pass_move

    def clone(self):
        """
        Clone the current board and state.
        :return: A new OthelloPosition object identical to the current one.
        """
        new_position = OthelloPosition()
        new_position.board = np.copy(self.board)
        new_position.maxPlayer = self.maxPlayer
        return new_position

    def print_board(self):
        """
        Print and log the current board state.
        """
        board_str = "\n".join([" ".join(self.board[row][1:9]) for row in range(1, 9)])
        print(board_str, flush=True)

    def to_move(self):
        """
        Check which player's turn it is.
        :return: True if it's White's turn, False if it's Black's turn.
        """
        return self.maxPlayer
