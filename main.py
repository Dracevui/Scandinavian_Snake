import pygame
import sys
import math
import random
from pygame.math import Vector2

CELL_SIZE = 40
CELL_NUMBER = 20


def screen_dimensions(width, height):  # Lets me easily change the dimensions of the game window
    monitor = pygame.display.Info()
    base_x, base_y = 1920, 1080
    target_x = width / base_x
    target_y = height / base_y
    final_x, final_y = math.ceil(monitor.current_w * target_x), math.ceil(monitor.current_h * target_y)
    return final_x, final_y


def game_quit():  # Quits the game when called upon
    pygame.quit()
    sys.exit()


class Fruit:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self, cell_size, colour):  # Draws fruit onscreen
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(self.parent_screen, colour, fruit_rect)

    def randomise(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10), ]
        self.direction = Vector2(0, 0)
        self.new_block = False

    def draw_snake(self, colour):
        for block in self.body:
            x_pos = block.x * CELL_SIZE
            y_pos = block.y * CELL_SIZE
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.parent_screen, colour, block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class Game:
    def __init__(self):
        # Game Initialisation
        pygame.init()
        pygame.display.set_caption("Hiss Noises")

        # Game Constants
        self.DUMMY_WINDOW = pygame.Surface((CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
        self.SCREEN_DIMENSIONS = screen_dimensions(CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER)
        self.WINDOW = pygame.display.set_mode(self.SCREEN_DIMENSIONS)
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60
        self.SCREEN_UPDATE = pygame.USEREVENT

        # User Event Timers
        pygame.time.set_timer(self.SCREEN_UPDATE, 150)

        # Colours
        self.RED = (255, 0, 0)
        self.GREEN = (83, 255, 121)

        # Game Variables
        self.running = True

        # Class Imports
        self.fruit = Fruit(self.DUMMY_WINDOW)
        self.snake = Snake(self.DUMMY_WINDOW)

    def scale_window(self):  # Scales the game window and assets to fit the user's monitor dimensions
        frame = pygame.transform.scale(self.DUMMY_WINDOW, self.SCREEN_DIMENSIONS)
        self.WINDOW.blit(frame, frame.get_rect())
        pygame.display.flip()

    def update(self):
        self.snake.move_snake()
        self.check_collision()

    def draw_elements(self):
        self.fruit.draw_fruit(CELL_SIZE, self.RED)
        self.snake.draw_snake(self.GREEN)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomise()
            self.snake.add_block()

    def main(self):  # The main game loop
        while self.running:
            self.DUMMY_WINDOW.fill((175, 215, 70))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit()

                if event.type == self.SCREEN_UPDATE:
                    self.update()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN:
                        self.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT:
                        self.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        self.snake.direction = Vector2(1, 0)

            self.draw_elements()
            self.scale_window()
            self.CLOCK.tick(self.FPS)


if __name__ == '__main__':
    game = Game()
    game.main()
