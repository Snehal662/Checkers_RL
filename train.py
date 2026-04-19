import sys
print(sys.path)
from board import Board
from agent import Agent

def train(episodes=50000):
    agent = Agent()

    for episode in range(episodes):
        board = Board()
        current_player = 1

        while not board.is_game_over():
            state = board.get_state()
            valid_moves = board.get_valid_moves(current_player)

            if not valid_moves:
                break

            action = agent.choose_action(state, valid_moves)

            board.make_move(action)

            next_state = board.get_state()
            next_valid_moves = board.get_valid_moves(-current_player)

            reward = 0

            if board.is_game_over():
                winner = board.get_winner()
                if winner == current_player:
                    reward = 1
                elif winner == -current_player:
                    reward = -1

            agent.update(state, action, reward,
                         next_state, next_valid_moves)

            current_player *= -1

        if episode % 1000 == 0:
            print("Episode:", episode)

    agent.save()
    print("Training Complete!")


if __name__ == "__main__":
    train()