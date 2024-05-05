import networkx as nx
import numpy as np

class Board:
    def __init__(self):
        self.network: nx.Graph = nx.Graph()
        self.players: np.ndarray = np.array([])
        self.deck: np.ndarray = np.array([])
        self.discard: np.ndarray = np.array([])

    def add_city(self, city: str) -> None:
        self.network.add_node(city)

    def add_route(self, city1: str, city2: str, cost: str) -> None:
        if not self.network.has_node(city1) or not self.network.has_node(city2):
            raise ValueError("One of the cities does not exist")
        self.network.add_edge(city1, city2, cost=cost, owner=None)

    def shuffle_in_discard(self) -> None:
        np.random.shuffle(self.discard)
        self.deck = np.concatenate([self.deck, self.discard])
        self.discard = np.array([])
