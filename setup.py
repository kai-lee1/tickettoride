from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from board import Board
    
def setup(board: Board):
    board.add_city("London", 2633, 431)
    board.add_city("Copenhagen", 2822, 355)
    board.add_connection("London", "Copenhagen", "3R")
