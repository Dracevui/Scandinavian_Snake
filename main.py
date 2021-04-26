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


def update_score(score, hi_score):  # Replaces the high score if the current score surpasses the current one
    if score > hi_score:
        hi_score = score
    return hi_score


class Fruit:
    def __init__(self, parent_screen, pizza):
        self.pizza = pizza
        self.parent_screen = parent_screen
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self, cell_size):  # Draws fruit onscreen
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        self.parent_screen.blit(self.pizza, fruit_rect)

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

        # Directions
        self.north = False
        self.south = False
        self.east = False
        self.west = False

        # Body Assets
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

    def draw_snake(self):  # Draws the snake on screen
        for index, block in enumerate(self.body):  # Gives an index number to the block we are looking at
            x_pos = block.x * CELL_SIZE
            y_pos = block.y * CELL_SIZE
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            if index == 0:  # Refers to the first block ie the head
                self.update_head_graphics(block_rect)

            elif index == len(self.body) - 1:  # Refers to the last block ie the tail
                self.update_tail_graphics(block_rect)

            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:  # Draws vertical body
                    self.parent_screen.blit(self.body_vertical, block_rect)
                if previous_block.y == next_block.y:  # Draws horizontal body
                    self.parent_screen.blit(self.body_horizontal, block_rect)
                else:
                    self.update_corner_graphics(previous_block, next_block, block_rect)
                
    def update_head_graphics(self, rect):  # Updates the head graphic depending on the direction you're facing
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(0, -1):
            self.parent_screen.blit(self.head_down, rect)
        if head_relation == Vector2(0, 1):
            self.parent_screen.blit(self.head_up, rect)
        if head_relation == Vector2(1, 0):
            self.parent_screen.blit(self.head_left, rect)
        if head_relation == Vector2(-1, 0):
            self.parent_screen.blit(self.head_right, rect)

    def update_corner_graphics(self, previous_block, next_block, rect):  # Updates the corner graphics when turning
        if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
            self.parent_screen.blit(self.body_tl, rect)
        if previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
            self.parent_screen.blit(self.body_bl, rect)
        if previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
            self.parent_screen.blit(self.body_tr, rect)
        if previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
            self.parent_screen.blit(self.body_br, rect)

    def update_tail_graphics(self, rect):  # Updates the tail graphic depending on the direction you're facing
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(0, -1):
            self.parent_screen.blit(self.tail_down, rect)
        if tail_relation == Vector2(0, 1):
            self.parent_screen.blit(self.tail_up, rect)
        if tail_relation == Vector2(1, 0):
            self.parent_screen.blit(self.tail_left, rect)
        if tail_relation == Vector2(-1, 0):
            self.parent_screen.blit(self.tail_right, rect)

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
        self.FONT = pygame.font.SysFont('Impact', 50)

        # User Event Timers
        pygame.time.set_timer(self.SCREEN_UPDATE, 100)

        # Colours
        self.RED = (255, 0, 0)
        self.GREEN = (83, 255, 121)
        self.WHITE = (255, 255, 255)

        # Game Variables
        self.running = True
        self.game_active = True
        self.score = 0
        self.high_score = 0

        # Class Imports
        self.assets = Assets()
        self.fruit = Fruit(self.DUMMY_WINDOW, self.assets.pizza)
        self.snake = Snake(self.DUMMY_WINDOW)
        pygame.display.set_icon(self.assets.icon)

    def display_score(self):
        score = self.FONT.render(f"Score: {self.score}", True, self.WHITE)
        hi_score = self.FONT.render(f"High Score: {self.high_score}", True, self.WHITE)
        self.high_score = update_score(self.score, self.high_score)

        self.DUMMY_WINDOW.blit(score, (800, 935))
        if not self.game_active:
            self.DUMMY_WINDOW.blit(hi_score, (365, 750))

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
        self.fruit.draw_fruit(CELL_SIZE)
        self.snake.draw_snake()

    def check_collision(self):  # Checks to see if the head of the snake has collided with the fruit
        if self.fruit.pos == self.snake.body[0]:
            self.assets.crunch.play()
            self.fruit.randomise()
            self.snake.add_block()
            self.score += 1

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
            self.display_score()
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
            self.display_score()
            self.scale_window()
            self.CLOCK.tick(self.FPS)


if __name__ == '__main__':
    game = Game()
    game.main()
