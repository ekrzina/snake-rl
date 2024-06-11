import snakevis as sv
import random
import pygame
import numpy as np
from collections import deque

class ExperienceReplayBuffer:
    def __init__(self, buffer_size):
        self.buffer = deque(maxlen=buffer_size)
    
    def add_experience(self, experience):
        self.buffer.append(experience)
    
    def sample_batch(self, batch_size):
        if len(self.buffer) < batch_size:
            batch_size = len(self.buffer)
        return random.sample(self.buffer, batch_size)

class GameAgent:
    def __init__(self, state_size, action_size, alpha=0.1, gamma=0.9, epsilon=0.1, replay_buffer_size=1000, batch_size=32):
            self.state_size = state_size
            self.action_size = action_size
            self.alpha = alpha
            self.gamma = gamma 
            self.epsilon = epsilon
            self.q_table = np.zeros(state_size + (action_size,))
            self.actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
            self.replay_buffer = ExperienceReplayBuffer(replay_buffer_size)
            self.batch_size = batch_size

    def get_state(self, game):
        head_x, head_y = game.snake[0]
        if game.food_position:
            food_x, food_y = game.food_position
        else:
            food_x, food_y = -1, -1
        
        # Direction to food
        food_dir_x = 1 if food_x > head_x else -1 if food_x < head_x else 0
        food_dir_y = 1 if food_y > head_y else -1 if food_y < head_y else 0

        # Distance to wall
        dist_to_top_wall = head_y
        dist_to_bottom_wall = game.grid_size - 1 - head_y
        dist_to_left_wall = head_x
        dist_to_right_wall = game.grid_size - 1 - head_x

        # check for immediate obstacles (body or walls)
        body_up = 1 if (head_x, head_y - 1) in game.snake or head_y - 1 < 0 else 0
        body_down = 1 if (head_x, head_y + 1) in game.snake or head_y + 1 >= game.grid_size else 0
        body_left = 1 if (head_x - 1, head_y) in game.snake or head_x - 1 < 0 else 0
        body_right = 1 if (head_x + 1, head_y) in game.snake or head_x + 1 >= game.grid_size else 0

        return (
            food_dir_x, food_dir_y,
            dist_to_top_wall, dist_to_bottom_wall, dist_to_left_wall, dist_to_right_wall,
            body_up, body_down, body_left, body_right
        )

    def choose_action(self, state):
        state_idx = tuple(int(s) for s in state)
        # if smaller than epsilon, explore (random), otherwise exploit
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(range(self.action_size))
            return action
        return np.argmax(self.q_table[state_idx])

    def update_q_network(self, batch):
            for experience in batch:
                state, action, reward, next_state = experience
                state_idx = tuple(int(s) for s in state)
                next_state_idx = tuple(int(s) for s in next_state)
                best_next_action = np.argmax(self.q_table[next_state_idx])
                td_target = reward + self.gamma * self.q_table[next_state_idx][best_next_action]
                td_error = td_target - self.q_table[state_idx][action]
                self.q_table[state_idx][action] += self.alpha * td_error

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
                self.replay_buffer.add_experience((state, action, reward, next_state))
                state = next_state
                total_reward += reward
                
                # sample mini-batch from replay buffer
                batch = self.replay_buffer.sample_batch(self.batch_size)
                self.update_q_network(batch)

                game.draw_environment()
                pygame.display.flip()
                game.clock.tick(10)

            print(f"Episode {episode + 1}: Total Reward: {total_reward}")

if __name__ == "__main__":
    grid_size = 10
    cell_size = 20
    state_size = (3, 3, grid_size, grid_size, grid_size, grid_size, 2, 2, 2, 2)
    action_size = 4  # ['UP', 'DOWN', 'LEFT', 'RIGHT']

    game = sv.SnakeVisual(grid_size=grid_size, cell_size=cell_size)
    agent = GameAgent(state_size, action_size, alpha=0.15, gamma=0.8, epsilon=0.2)

    agent.train(game, episodes=5000)
    np.save('q_table.npy', agent.q_table)
    pygame.quit()
