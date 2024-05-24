from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from board import Board
    
def setup(board: Board):
    board.add_city("London", 2633, 431)
    board.add_city("Copenhagen", 2822, 355)
    board.add_city("Berlin", 2826, 414)
    board.add_city("Paris", 2700, 500)
    board.add_city("Madrid", 2600, 630)
    board.add_city("Tehran", 3450, 750)
    board.add_connection("London", "Copenhagen", "R R R R")
    board.add_connection("London", "Berlin", "Y Y Y")
    board.add_connection("Tehran", "Madrid", "G G G G G G G G G G")
    board.add_connection("Paris", "Madrid", "O O O")
    board.add_connection("Berlin", "Paris", "L L L")
    board.add_connection("Berlin", "Madrid", "B B B B B")
    board.add_connection("Berlin", "Copenhagen", "P P")
    
    
