import snakevis as sv
import random
import pygame
import numpy as np

class GameAgent:
    def __init__(self, state_size, action_size, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.state_size = state_size
        self.action_size = action_size
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        # Calculate the total number of states
        self.q_table = np.zeros(state_size + (action_size,))
        self.actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    def get_state(self, game):
        head_x, head_y = game.snake[0]
        if game.food_position:
            food_x, food_y = game.food_position
        else:
            # If food hasn't been generated yet, return a default state
            food_x, food_y = -1, -1  # Or any other value that represents the absence of food
        return (head_x, head_y, food_x, food_y)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(range(self.action_size))
        return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_error

    def train(self, game, episodes):
        for episode in range(episodes):
            state = self.get_state(game)
            total_reward = 0
            game.running = True
            while game.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                action = self.choose_action(state)
                direction = self.actions[action]
                reward = game.move_snake(direction)
                next_state = self.get_state(game)
                self.update_q_table(state, action, reward, next_state)
                state = next_state
                total_reward += reward

                game.draw_environment()
                pygame.display.flip()
                game.clock.tick(10)

            print(f"Episode {episode + 1}: Total Reward: {total_reward}")


if __name__ == "__main__":
    grid_size = 10
    cell_size = 20
    state_size = (grid_size, grid_size, grid_size, grid_size)  # (head_x, head_y, food_x, food_y)
    action_size = 4  # ['UP', 'DOWN', 'LEFT', 'RIGHT']

    game = sv.SnakeVisual(grid_size=grid_size, cell_size=cell_size)
    agent = GameAgent(state_size, action_size, alpha=0.1, gamma=0.9, epsilon=0.1)

    agent.train(game, episodes=1000)

    pygame.quit()