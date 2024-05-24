import networkx as nx
import numpy as np
from setup import setup
import logging
from player import Player

class Board:
    def __init__(self):
        """
        Initializes a new instance of the Board class.
        """
        self.network: nx.Graph = nx.Graph()
        self.players: np.ndarray = np.array([])
        self.deck: np.ndarray = np.array([])
        self.discard: np.ndarray = np.array([])
        self.face_up: np.ndarray = np.array([])
        self.followed_player = None
        self.turn = 0
        self.able_to_draw = 0

        setup(self)
        

        self.populate_deck()
        
    def make_players(self, num: int) -> None:
        """
        Makes the players for the game.
        
        Parameters:
            num (int): The number of players.
        """
        self.players = np.array([])
        for i in range(num):
            self.players = np.append(self.players, Player(self))
        
        self.followed_player = self.players[0]

    def shuffle_in_discard(self) -> None:
        """
        Shuffles the cards in the discard pile and adds them back to the deck.
        """
        np.random.shuffle(self.discard)
        self.deck = np.concatenate([self.deck, self.discard])
        self.discard = np.array([])
    
    def add_city(self, name: str, x: float, y: float) -> None:
        """
        Adds a city to the `board.`
        
        Parameters:
            main (Main): The main instance.
            name (str): The name of the city.
            x (float): The x-coordinate of the city.
            y (float): The y-coordinate of the city.
        """
        self.network.add_node(name, coords=(x, y), name=name)

    def add_connection(self, city1: str, city2: str, cost: str) -> None:
        """
        Adds a connection between two cities.
        
        Parameters:
            city1 (str): The first city.
            city2 (str): The second city.
            weight (float): The weight of the connection.
        """
        if city1 not in self.network.nodes or city2 not in self.network.nodes:
            raise ValueError("One or more cities do not exist on the board.")
        vector = tuple([self.network.nodes[city1]['coords'][0] - self.network.nodes[city2]['coords'][0], -self.network.nodes[city1]['coords'][1] + self.network.nodes[city2]['coords'][1]])
        self.network.add_edge(city1, city2, player=None, cost=cost, c1=self.network.nodes[city1]['coords'], c2=self.network.nodes[city2]['coords'], v=tuple(vector / np.linalg.norm(vector)))
    
    def populate_deck(self):
        for i in range(144):
            match (i % 9):
                case 0:
                    self.deck = np.append(self.deck, "L")
                    #logging.info(self.deck[i] + str(i))
                case 1:
                    self.deck = np.append(self.deck, "R")
                case 2:
                    self.deck = np.append(self.deck, "O")
                case 3:
                    self.deck = np.append(self.deck, "Y")
                case 4:
                    self.deck = np.append(self.deck, "G")
                case 5:
                    self.deck = np.append(self.deck, "U")
                case 6:
                    self.deck = np.append(self.deck, "P")
                case 7:
                    self.deck = np.append(self.deck, "B")
                case 8:
                    self.deck = np.append(self.deck, "W")
                case _:
                    pass
        np.random.shuffle(self.deck)
        np.vectorize(lambda n: self.turn_up(), signature='()->()')(list(range(5)))
    
    def turn_up(self):
        if self.face_up.size < 5:
            self.face_up = np.append(self.face_up, self.deck[0])
            self.deck = np.delete(self.deck, 0)
        else:
            logging.info("There are already 5 face-up cards.")

    def draw(self):
        top = self.deck[0]
        self.deck = np.delete(self.deck, 0)
        return top
    
    def pick(self, index: int): #possibly doesn't work 
        if self.face_up.size > index:
            top = self.face_up[index]
            self.face_up = np.delete(self.face_up, index)
            self.turn_up()
            return top
        else:
            logging.info("The index is out of range.")
            return None
        

    def claim_route(self, player: int, city1: str, city2: str):
        if city1 not in self.network.nodes or city2 not in self.network.nodes:
            logging.info("One or more cities do not exist on the board.")
        elif self.network.has_edge(city1, city2):
            self.network.edges[city1, city2]['player'] = player
            logging.info(f"Route {city1} - {city2} claimed by player {player}.")
        else:
            logging.info("The cities are not connected.")

    # def end_turn(self):
    #     if(self.board.draw_counter < 2):
    #         self.turn += 1
    #         self.followed_player = self.players[self.turn % len(self.players)]
    #         logging.info(f"Player {self.turn % len(self.players)}'s turn.")
            
    


    