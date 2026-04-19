import pickle
with open("q_table.pkl", "rb") as f:
    q_table = pickle.load(f)
print("Q-table loaded successfully!")
from board import Board
import random
board = Board()
current_player = 1
while not board.is_game_over():
    board.print_board()
    moves = board.get_valid_moves(current_player)
    if not moves:
        break
    move = random.choice(moves)
    board.make_move(move)
    current_player *= -1
board.print_board()
print("Winner:", board.get_winner())