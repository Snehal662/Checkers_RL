class Board:
    def __init__(self):
        self.size = 8
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.initialize_board()
    def initialize_board(self):
        for row in range(3):
            for col in range(self.size):
                if (row + col) % 2 == 1:
                    self.board[row][col] = -1
        for row in range(5, 8):
            for col in range(self.size):
                if (row + col) % 2 == 1:
                    self.board[row][col] = 1
    def get_valid_moves(self, player):
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == player:
                    direction = -1 if player == 1 else 1
                    for dc in [-1, 1]:
                        new_r = r + direction
                        new_c = c + dc
                        if 0 <= new_r < 8 and 0 <= new_c < 8:
                            if self.board[new_r][new_c] == 0:
                                moves.append(((r, c), (new_r, new_c)))
                    for dc in [-2, 2]:
                        new_r = r + 2 * direction
                        new_c = c + dc
                        mid_r = r + direction
                        mid_c = c + (dc // 2)
                        if 0 <= new_r < 8 and 0 <= new_c < 8:
                            if self.board[new_r][new_c] == 0:
                                if self.board[mid_r][mid_c] == -player:
                                    moves.append(((r, c), (new_r, new_c)))
        return moves
    def print_board(self):
        print("\nBoard:")
        for row in self.board:
            print(row)
        print()
    def make_move(self, move):
        (r1, c1), (r2, c2) = move
        player = self.board[r1][c1]
        self.board[r1][c1] = 0
        self.board[r2][c2] = player
        if abs(r2 - r1) == 2:
            mid_r = (r1 + r2) // 2
            mid_c = (c1 + c2) // 2
            self.board[mid_r][mid_c] = 0
    def get_state(self):
        return tuple(tuple(row) for row in self.board)
    def is_game_over(self):
        if not self.get_valid_moves(1) and not self.get_valid_moves(-1):
            return True
        human_pieces = sum(row.count(1) for row in self.board)
        ai_pieces = sum(row.count(-1) for row in self.board)
        if human_pieces == 0 or ai_pieces == 0:
            return True
        return False
    def get_winner(self):
        human_pieces = sum(row.count(1) for row in self.board)
        ai_pieces = sum(row.count(-1) for row in self.board)
        if human_pieces > ai_pieces:
            return 1
        elif ai_pieces > human_pieces:
            return -1
        else:
            return 0