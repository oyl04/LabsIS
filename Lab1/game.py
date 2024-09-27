import time

import pygame
from pacman import Pacman, Direction
from ghost import Ghost
from level import Level
from settings import WIDTH, HEIGHT, FPS, CELL_SIZE

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

PACMAN_MODE = 'auto'


def display_game_over(screen):
    font = pygame.font.SysFont(None, 55)
    game_over_text = font.render('Game Over', True, (255, 0, 0))
    screen.blit(game_over_text,
                (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(2)  # Даем игроку 2 секунды для прочтения сообщения


def main():
    level = Level(1)
    pacman = Pacman(level.pacman['x'], level.pacman['y'], level.pacman['speed'], PACMAN_MODE)
    ghosts = [Ghost(g['x'], g['y'], level.ghost_speed, g['behavior'], g['icon']) for g in level.ghosts]

    running = True
    game_over = False
    last_pressed = Direction(0, 0)

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                last_pressed = Direction(0, -1)
            elif keys[pygame.K_RIGHT]:
                last_pressed = Direction(0, 1)
            elif keys[pygame.K_UP]:
                last_pressed = Direction(-1, 0)
            elif keys[pygame.K_DOWN]:
                last_pressed = Direction(1, 0)

            level.maze.draw(screen)
            pacman.draw(level.maze.maze, screen)

            for ghost in ghosts:
                ghost.draw(level.maze.maze, screen)

            for ghost in ghosts:
                ghost.move(pacman, level.maze.maze)

            pacman.move(level.maze, last_pressed, ghosts)

            if level.is_food_collected():
                level.next_level()
                pacman = Pacman(level.pacman['x'], level.pacman['y'], level.pacman['speed'], PACMAN_MODE)
                ghosts = [Ghost(g['x'], g['y'], level.ghost_speed, g['behavior'], g['icon']) for g in level.ghosts]

            # Проверяем, если Пакмен встретился с призраком
            for ghost in ghosts:
                if (ghost.x, ghost.y) == (pacman.x, pacman.y):
                    game_over = True

        else:
            display_game_over(screen)

            level = Level(1)
            pacman = Pacman(level.pacman['x'], level.pacman['y'], level.pacman['speed'], PACMAN_MODE)
            ghosts = [Ghost(g['x'], g['y'], level.ghost_speed, g['behavior'], g['icon']) for g in level.ghosts]

            running = True
            game_over = False
            last_pressed = Direction(0, 0)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
