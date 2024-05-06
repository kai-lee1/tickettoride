import networkx as nx
import numpy as np
from setup import setup

class Board:
    def __init__(self):
        """
        Initializes a new instance of the Board class.
        """
        self.network: nx.Graph = nx.Graph()
        self.players: np.ndarray = np.array([])
        self.deck: np.ndarray = np.array([])
        self.discard: np.ndarray = np.array([])

        setup(self)        

    def shuffle_in_discard(self) -> None:
        """
        Shuffles the cards in the discard pile and adds them back to the deck.
        """
        np.random.shuffle(self.discard)
        self.deck = np.concatenate([self.deck, self.discard])
        self.discard = np.array([])
    
    def add_city(self, name: str, x: float, y: float) -> None:
        """
        Adds a city to the board.
        
        Parameters:
            main (Main): The main instance.
            name (str): The name of the city.
            x (float): The x-coordinate of the city.
            y (float): The y-coordinate of the city.
        """
        self.network.add_node(name, coords=(x, y))
