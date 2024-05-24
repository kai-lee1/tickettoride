import numpy as np
#hand, score. we can add the destination tickets later
class Player:
    def __init__(self, board):
        """
        Initializes a new instance of the Player class.
        """
        self.board = board
        self.hand: np.ndarray = np.array([])
        self.score: int = 0
    
    def draw_card (self):
        self.hand = np.append(self.hand, self.board.draw())
        
    def pick_card (self, index: int):
        self.hand = np.append(self.hand, self.board.pick(index))
    
    def claim_route (self, route: str):
        self.score += self.board.claim_route(self)
        
        
    
    
        

    
