import pygame
import sys
import math


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


def scale_window():  # Scales the game window and assets to fit the user's monitor dimensions
    frame = pygame.transform.scale(DUMMY_WINDOW, SCREEN_DIMENSIONS)
    WINDOW.blit(frame, frame.get_rect())
    pygame.display.flip()


def main():  # The main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()

        DUMMY_WINDOW.fill((175, 215, 70))
        scale_window()
        CLOCK.tick(FPS)


# Game Initialisation
pygame.init()
pygame.display.set_caption("Hiss Noises")

# Constants
WINDOW_W, WINDOW_H = 400, 500
DUMMY_WINDOW = pygame.Surface((WINDOW_W, WINDOW_H))
SCREEN_DIMENSIONS = screen_dimensions(WINDOW_W, WINDOW_H)
WINDOW = pygame.display.set_mode(SCREEN_DIMENSIONS)
CLOCK = pygame.time.Clock()
FPS = 60

# Game Variables


if __name__ == '__main__':
    main()
