import random
import pickle


class Agent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.q_table = {}  # {(state, action): value}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    # Get Q value
    def get_q(self, state, action):
        return self.q_table.get((state, action), 0.0)

    # Choose action (epsilon-greedy)
    def choose_action(self, state, valid_moves):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(valid_moves)

        q_values = [self.get_q(state, move) for move in valid_moves]
        max_q = max(q_values)

        best_moves = [move for move in valid_moves
                      if self.get_q(state, move) == max_q]

        return random.choice(best_moves)

    # Update Q-table
    def update(self, state, action, reward, next_state, next_valid_moves):
        old_q = self.get_q(state, action)

        if next_valid_moves:
            future_q = max([self.get_q(next_state, a)
                           for a in next_valid_moves])
        else:
            future_q = 0

        new_q = old_q + self.alpha * (
            reward + self.gamma * future_q - old_q
        )

        self.q_table[(state, action)] = new_q

    # Save model
    def save(self, filename="q_table.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.q_table, f)

    # Load model
    def load(self, filename="q_table.pkl"):
        with open(filename, "rb") as f:
            self.q_table = pickle.load(f)