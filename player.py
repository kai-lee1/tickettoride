import numpy as np
from board import Board
#hand, score. we can add the destination tickets later
class Player:
    def __init__(self, board: Board):
        """
        Initializes a new instance of the Player class.
        """
        self.board: Board = board
        self.hand: np.ndarray = np.array([])
        self.score: np.ndarray = np.array([])
    
    def draw_card (self):
        self.hand = np.append(self.hand, self.board.draw())
        