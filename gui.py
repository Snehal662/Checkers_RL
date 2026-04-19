import tkinter as tk
from board import Board
from agent import Agent
import pickle 

SQUARE_SIZE = 80
BOARD_SIZE = 8


class CheckersGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RL Checkers 8x8")

        self.board = Board()        # CREATE FIRST
        self.agent = Agent()

        self.current_player = 1
        self.selected_piece = None

        # Debug check (IMPORTANT)
        print("Rows:", len(self.board.board))
        print("Cols:", len(self.board.board[0]))

        self.canvas = tk.Canvas(
            root,
            width=SQUARE_SIZE * BOARD_SIZE,
            height=SQUARE_SIZE * BOARD_SIZE
        )
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()

    # -------------------------
    # Draw Board
    # -------------------------
    def draw_board(self):
        self.canvas.delete("all")

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):

                x1 = c * SQUARE_SIZE
                y1 = r * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE

                color = "#EEEED2" if (r + c) % 2 == 0 else "#769656"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                # SAFE ACCESS
                if r < len(self.board.board) and c < len(self.board.board[0]):
                    piece = self.board.board[r][c]
                else:
                    continue

                if piece == 1:
                    self.canvas.create_oval(
                        x1 + 15, y1 + 15,
                        x2 - 15, y2 - 15,
                        fill="red"
                    )
                elif piece == -1:
                    self.canvas.create_oval(
                        x1 + 15, y1 + 15,
                        x2 - 15, y2 - 15,
                        fill="black"
                    )

    # -------------------------
    # Handle Click
    # -------------------------
    def on_click(self, event):

        if self.current_player != 1:
            return

        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE

        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return

        if self.selected_piece is None:
            if self.board.board[row][col] == 1:
                self.selected_piece = (row, col)
        else:
            move = (self.selected_piece, (row, col))
            valid_moves = self.board.get_valid_moves(1)

            if move in valid_moves:
                self.board.make_move(move)
                self.selected_piece = None
                self.draw_board()

                if self.check_game_over():
                    return

                self.current_player = -1
                self.root.after(500, self.ai_move)
            else:
                self.selected_piece = None

    # -------------------------
    # AI Move
    # -------------------------
    def ai_move(self):

        state = self.board.get_state()
        moves = self.board.get_valid_moves(-1)

        if not moves:
            return

        move = self.agent.choose_action(state, moves)

        if move is None:
            return

        self.board.make_move(move)
        self.draw_board()

        if self.check_game_over():
            return

        self.current_player = 1

    # -------------------------
    # Game Over
    # -------------------------
    def check_game_over(self):

        if self.board.is_game_over():

            winner = self.board.get_winner()

            if winner == 1:
                result = "You Win!"
            elif winner == -1:
                result = "AI Wins!"
            else:
                result = "Draw!"

            self.canvas.create_text(
                SQUARE_SIZE * 4,
                SQUARE_SIZE * 4,
                text=result,
                font=("Arial", 30),
                fill="blue"
            )

            print("Winner:", winner)
            return True

        return False


if __name__ == "__main__":
    root = tk.Tk()
    game = CheckersGUI(root)
    root.mainloop()