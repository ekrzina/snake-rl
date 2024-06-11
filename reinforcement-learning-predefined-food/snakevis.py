import numpy as np
import pygame

class SnakeVisual:
    def __init__(self, grid_size=35, cell_size=15):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.bkg_color = (161, 219, 192)
        self.agt_color = (0, 0, 0)
        self.grid_color = (255, 255, 255)
        self.current_direction = 'RIGHT'
        self.food_position = None
        self.food_positions = []
        self.food_position_recovery = []
        self.food_eaten = False
        self.current_direction = 'RIGHT'
        self.score = 0
        self.running = False

        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.initialize_game()

    def game_over(self):
        print("Game Over! Your Score: ", self.score)
        self.running = False

        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.score = 0
        self.food_positions = self.food_position_recovery
        self.food_position = None
        self.draw_environment()
        self.generate_food()

    def initialize_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.grid_size * self.cell_size, self.grid_size * self.cell_size))
        self.clock = pygame.time.Clock()
        self.screen.fill(self.bkg_color)
        self.running = True

        np.random.seed(967)
        while len(self.food_positions) <= 50:
            food_x = np.random.randint(1, self.grid_size - 1)
            food_y = np.random.randint(1, self.grid_size - 1)
            if (food_x, food_y) not in self.food_positions:
                self.food_positions.append((food_x, food_y))
        self.food_positions = np.array(self.food_positions)
        self.food_position_recovery = self.food_positions

        self.generate_food()

    def generate_food(self):
        if self.food_positions.size > 0:
            self.food_position = self.food_positions[0]
            self.food_positions = np.delete(self.food_positions, 0, axis=0)
            self.food_eaten = False

    def draw_environment(self):
        self.screen.fill(self.bkg_color)
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if x == 0 or y == 0 or x == self.grid_size - 1 or y == self.grid_size - 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, self.grid_color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size), 1)
        self.draw_snake()
        if self.food_position is not None:
            food_x, food_y = self.food_position
            pygame.draw.rect(self.screen, self.agt_color, (food_x * self.cell_size, food_y * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.flip()

    def draw_snake(self):
        for segment in self.snake:
            pygame.draw.rect(self.screen, self.agt_color, (segment[0] * self.cell_size, segment[1] * self.cell_size, self.cell_size, self.cell_size))

    def move_snake(self, direction):
        # Update the current direction
        self.current_direction = direction
        
        head = self.snake[0]
        if direction == 'UP':
            new_head = (head[0], head[1] - 1)
        elif direction == 'DOWN':
            new_head = (head[0], head[1] + 1)
        elif direction == 'LEFT':
            new_head = (head[0] - 1, head[1])
        elif direction == 'RIGHT':
            new_head = (head[0] + 1, head[1])

        # collision check
        if new_head in self.snake[1:] or new_head[0] <= 0 or new_head[0] >= self.grid_size - 1 or new_head[1] <= 0 or new_head[1] >= self.grid_size - 1:
            self.game_over()
            return -50
        
        if new_head == tuple(self.food_position):
            self.food_eaten = True
            self.score += 1
            self.generate_food()
            self.snake.insert(0, new_head)
            return 50
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()
            # reward for each step survived
            return 1


    def check_food_collision(self):
        if self.snake[0] == self.food_position:
            self.food_eaten = True
            self.generate_food()