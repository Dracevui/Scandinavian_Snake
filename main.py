import pygame
import sys
import math
import random
from pygame.math import Vector2

CELL_SIZE = 40
CELL_NUMBER = 25


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
    def __init__(self, parent_screen, fruit):
        self.fruit = fruit
        self.parent_screen = parent_screen
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self, cell_size, colour):  # Draws fruit onscreen
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        self.parent_screen.blit(self.fruit, fruit_rect)
        # pygame.draw.rect(self.parent_screen, colour, fruit_rect)

    def randomise(self):  # Randomises the position of the fruit after being eaten
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.body = [Vector2(5, 10), Vector2(4, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.north = False
        self.south = False
        self.east = False
        self.west = False

    def draw_snake(self, colour):  # Draws the snake on screen
        for block in self.body:
            x_pos = block.x * CELL_SIZE
            y_pos = block.y * CELL_SIZE
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.parent_screen, colour, block_rect)

    def move_snake(self):  # Moves the snake according to user input
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def move_north(self):  # Moves snake up
        if not self.south:
            self.direction = Vector2(0, -1)
            self.north = True
            self.south = False
            self.east = False
            self.west = False

    def move_south(self):  # Moves snake down
        if not self.north:
            self.direction = Vector2(0, 1)
            self.north = False
            self.south = True
            self.east = False
            self.west = False

    def move_east(self):  # Moves snake right
        if not self.west:
            self.direction = Vector2(1, 0)
            self.north = False
            self.south = False
            self.east = True
            self.west = False

    def move_west(self):  # Moves snake left
        if not self.east:
            self.direction = Vector2(-1, 0)
            self.north = False
            self.south = False
            self.east = False
            self.west = True

    def add_block(self):  # Adds block to the current snake
        self.new_block = True

    def walk_through_walls(self):  # Makes the snake come out the other side when they hit a wall
        if self.body[0].x >= CELL_NUMBER - 1:
            self.body[0].x -= CELL_NUMBER
        if self.body[0].x < 0:
            self.body[0].x += CELL_NUMBER
        if self.body[0].y >= CELL_NUMBER - 1:
            self.body[0].y -= CELL_NUMBER
        if self.body[0].y < 0:
            self.body[0].y += CELL_NUMBER


class Assets:  # The class that handles loading in game assets
    def __init__(self):
        # Graphics
        self.background = pygame.transform.scale(
            (pygame.image.load("Graphics/water_background.png")), (CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER)
        )
        self.game_over = pygame.image.load("Graphics/game_over.png").convert_alpha()
        self.press_spacebar_surface = pygame.image.load("Graphics/press_spacebar2.png").convert_alpha()
        self.icon = pygame.image.load("Graphics/icon.png").convert_alpha()
        self.resume_surface = pygame.image.load("Graphics/resume_button.png").convert_alpha()
        self.pizza = pygame.image.load("Graphics/pizza_bubble.png").convert_alpha()
        
        # Sound
        self.bgm = pygame.mixer.Sound("Sound/bgm.wav")
        self.crunch = pygame.mixer.Sound("Sound/crunch.wav")
        self.crash = pygame.mixer.Sound("Sound/crash.mp3")

    def play_bgm(self):  # Plays the background music
        self.bgm.play(-1)


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
        pygame.time.set_timer(self.SCREEN_UPDATE, 100)

        # Colours
        self.RED = (255, 0, 0)
        self.GREEN = (83, 255, 121)

        # Game Variables
        self.running = True
        self.game_active = True

        # Class Imports
        self.assets = Assets()
        self.fruit = Fruit(self.DUMMY_WINDOW, self.assets.pizza)
        self.snake = Snake(self.DUMMY_WINDOW)
        pygame.display.set_icon(self.assets.icon)

    def scale_window(self):  # Scales the game window and assets to fit the user's monitor dimensions
        frame = pygame.transform.scale(self.DUMMY_WINDOW, self.SCREEN_DIMENSIONS)
        self.WINDOW.blit(frame, frame.get_rect())
        pygame.display.flip()

    def update(self):  # Updates the screen when something happens
        self.snake.move_snake()
        self.check_collision()
        self.snake.walk_through_walls()
        self.check_fail()

    def draw_elements(self):  # Draws the specified elements onscreen
        self.fruit.draw_fruit(CELL_SIZE, self.RED)
        self.snake.draw_snake(self.GREEN)

    def check_collision(self):  # Checks to see if the head of the snake has collided with the fruit
        if self.fruit.pos == self.snake.body[0]:
            self.assets.crunch.play()
            self.fruit.randomise()
            self.snake.add_block()

    def check_fail(self):  # Checks to see if the snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.assets.crash.play()
                self.game_over_screen()

    def game_over_screen(self):  # Draws the game over screen
        self.game_active = False
        while not self.game_active:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                    self.running = False
                    game_quit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.game_active = True

            self.DUMMY_WINDOW.blit(self.assets.background, (0, 0))
            self.DUMMY_WINDOW.blit(self.assets.game_over, (268, 268))
            self.DUMMY_WINDOW.blit(self.assets.press_spacebar_surface, (260, 21))
            self.scale_window()

    def main(self):  # The main game loop
        self.assets.play_bgm()
        while self.running:
            self.DUMMY_WINDOW.blit(self.assets.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit()

                if event.type == self.SCREEN_UPDATE:
                    self.update()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.move_north()
                    if event.key == pygame.K_DOWN:
                        self.snake.move_south()
                    if event.key == pygame.K_LEFT:
                        self.snake.move_west()
                    if event.key == pygame.K_RIGHT:
                        self.snake.move_east()

            self.draw_elements()
            self.scale_window()
            self.CLOCK.tick(self.FPS)


if __name__ == '__main__':
    game = Game()
    game.main()
