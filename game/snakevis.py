import pygame
import random

class SnakeVisual:
    def __init__(self, initial_snake_positions=None):
        self.snake_size = 1
        self.grid_size = 35
        self.cell_size = 15
        self.bkg_color = (161, 219, 192)
        self.agt_color = (0, 0, 0)
        self.grid_color = (255, 255, 255)
        self.food_position = None
        self.food_eaten = False
        self.init_val = True
        self.current_direction = 'RIGHT'
        self.score = 0

        if initial_snake_positions is None:
            initial_snake_positions = [(17, 17), (16, 17), (15, 17)]
        self.snake = initial_snake_positions

    def game_over(self):
        print("Game Over! Your Score: ", self.score)
        self.running = False

    def initialize_game(self, grid_size=None, cell_size=None):
        pygame.init()

        if grid_size is not None and cell_size is not None:
            self.grid_size = grid_size
            self.cell_size = cell_size

        self.screen = pygame.display.set_mode((self.grid_size * self.cell_size, self.grid_size * self.cell_size))
        self.clock = pygame.time.Clock()
        self.screen.fill(self.bkg_color)

    def generate_food(self):
        if self.init_val == False:
            self.score += 1
        while True:
            food_x = random.randint(1, self.grid_size - 2)
            food_y = random.randint(1, self.grid_size - 2)
            if (food_x, food_y) not in self.snake:
                break
        pygame.draw.rect(self.screen, self.agt_color, (food_x * self.cell_size, food_y * self.cell_size, self.cell_size, self.cell_size))
        self.food_position = (food_x, food_y)
        self.food_eaten = False
        self.init_val = False

    def draw_environment(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if x == 0 or y == 0 or x == self.grid_size - 1 or y == self.grid_size - 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, self.grid_color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size), 1)

        self.draw_snake()

        if self.food_position:
            food_x, food_y = self.food_position
            pygame.draw.rect(self.screen, self.agt_color, (food_x * self.cell_size, food_y * self.cell_size, self.cell_size, self.cell_size))

    def draw_snake(self):
        for segment in self.snake:
            pygame.draw.rect(self.screen, self.agt_color, (segment[0] * self.cell_size, segment[1] * self.cell_size, self.cell_size * self.snake_size, self.cell_size))

    def move_snake(self, direction):
        head = self.snake[0]
        if direction == 'UP':
            new_head = (head[0], head[1] - 1)
        elif direction == 'DOWN':
            new_head = (head[0], head[1] + 1)
        elif direction == 'LEFT':
            new_head = (head[0] - 1, head[1])
        elif direction == 'RIGHT':
            new_head = (head[0] + 1, head[1])

        # self collision
        if new_head in self.snake[1:]:
            self.game_over()
            return

        # wall collision
        if new_head[0] <= 0 or new_head[0] >= self.grid_size - 1 or new_head[1] <= 0 or new_head[1] >= self.grid_size - 1:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if not self.food_eaten:
            self.snake.pop()

    def check_food_collision(self):
        head = self.snake[0]
        if head == self.food_position:
            self.food_eaten = True
            # add segment to snake if it eats food
            self.snake.append(self.snake[-1]) 

    def run_snake(self, grid_size=None, cell_size=None):
        self.initialize_game(grid_size, cell_size)
        direction = 'RIGHT'
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.current_direction in ['LEFT', 'RIGHT']:
                        if event.key == pygame.K_UP:
                            direction = 'UP'
                        elif event.key == pygame.K_DOWN:
                            direction = 'DOWN'
                    elif self.current_direction in ['UP', 'DOWN']:
                        if event.key == pygame.K_LEFT:
                            direction = 'LEFT'
                        elif event.key == pygame.K_RIGHT:
                            direction = 'RIGHT'
            
            self.current_direction = direction
            self.move_snake(direction)
            self.screen.fill(self.bkg_color)
            self.draw_environment()
            self.check_food_collision()
            pygame.display.flip()

            if self.food_eaten or self.init_val:
                self.generate_food()
                self.init_val = False

            self.clock.tick(5)

        pygame.quit()
