import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

if __name__ == '__main__':
    running = True
    pygame.init()
    background = GRAY
    while running:
        screen = pygame.display.set_mode((640, 240))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == pygame.K_r:
                    background = RED
                elif event.key == pygame.K_g:
                    background = GREEN
        screen.fill(background)
        pygame.display.update()
        caption = 'background color = ' + str(background)
        pygame.display.set_caption(caption)
    pygame.quit()

