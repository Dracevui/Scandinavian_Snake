import pygame
import sys
import math
from pygame.math import Vector2


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
        self.x = 5
        self.y = 4
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self, cell_size, colour):  # Draws fruit onscreen
        fruit_rect = pygame.Rect(self.pos.x, self.pos.y, cell_size, cell_size)
        pygame.draw.rect(self.parent_screen, colour, fruit_rect)


class Game:
    def __init__(self):
        # Game Initialisation
        pygame.init()
        pygame.display.set_caption("Hiss Noises")

        # Game Constants
        self.CELL_SIZE = 40
        self.CELL_NUMBER = 20
        self.DUMMY_WINDOW = pygame.Surface((self.CELL_SIZE * self.CELL_NUMBER, self.CELL_SIZE * self.CELL_NUMBER))
        self.SCREEN_DIMENSIONS = screen_dimensions(self.CELL_SIZE * self.CELL_NUMBER, self.CELL_SIZE * self.CELL_NUMBER)
        self.WINDOW = pygame.display.set_mode(self.SCREEN_DIMENSIONS)
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60

        # Colours
        self.RED = (255, 0, 0)

        # Game Variables
        self.running = True

        # Class Imports
        self.fruit = Fruit(self.DUMMY_WINDOW)

    def scale_window(self):  # Scales the game window and assets to fit the user's monitor dimensions
        frame = pygame.transform.scale(self.DUMMY_WINDOW, self.SCREEN_DIMENSIONS)
        self.WINDOW.blit(frame, frame.get_rect())
        pygame.display.flip()

    def main(self):  # The main game loop
        while self.running:
            self.DUMMY_WINDOW.fill((175, 215, 70))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit()

            self.fruit.draw_fruit(self.CELL_SIZE, self.RED)
            self.scale_window()
            self.CLOCK.tick(self.FPS)


if __name__ == '__main__':
    game = Game()
    game.main()
