import numpy as np
#hand, score. we can add the destination tickets later
class Player:
    def __init__(self, board):
        """
        Initializes a new instance of the Player class.
        """
        self.board = board
        self.hand: np.ndarray = np.array([])
        self.score: np.ndarray = np.array([])
    
    def draw_card (self):
        self.hand = np.append(self.hand, self.board.draw())
    
