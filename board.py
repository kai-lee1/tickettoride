import networkx as nx
import numpy as np

class Board:
    def __init__(self):
        """
        Initializes a new instance of the Board class.
        """
        self.network: nx.Graph = nx.Graph()
        self.players: np.ndarray = np.array([])
        self.deck: np.ndarray = np.array([])
        self.discard: np.ndarray = np.array([])

    def add_city(self, city: str) -> None:
        """
        Adds a city to the board network.

        Args:
            city (str): The name of the city to add.
        """
        self.network.add_node(city)

    def add_route(self, city1: str, city2: str, cost: str) -> None:
        """
        Adds a route between two cities on the board network.

        Args:
            city1 (str): The name of the first city.
            city2 (str): The name of the second city.
            cost (str): The cost of the route.

        Raises:
            ValueError: If either city does not exist on the board network.
        """
        if not self.network.has_node(city1) or not self.network.has_node(city2):
            raise ValueError("One of the cities does not exist")
        self.network.add_edge(city1, city2, cost=cost, owner=None)

    def shuffle_in_discard(self) -> None:
        """
        Shuffles the cards in the discard pile and adds them back to the deck.
        """
        np.random.shuffle(self.discard)
        self.deck = np.concatenate([self.deck, self.discard])
        self.discard = np.array([])
