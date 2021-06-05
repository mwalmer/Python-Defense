import pygame
import os

WIDTH, HEIGHT = 640, 640
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Defense")

WHITE = (255, 255, 255)

FPS = 60

GRASS_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'grass_tile.png'))
GRASS_TILE = pygame.image.load(os.path.join('assets', 'tiles', 'dirt_tile.png'))


def draw_window():
    WIN.fill(WHITE)
    for x in range(0, 20):
        for y in range(0, 20):
            WIN.blit(GRASS_TILE, (x * 32, y * 32))
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window()
    pygame.quit()


if __name__ == '__main__':
    main()
