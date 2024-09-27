import pygame
import random

from pacman import Direction
from search_algorithms.bfs_search import bfs_search
from settings import CELL_SIZE, GHOST1_ICON, GHOST2_ICON, WIDTH, HEIGHT


class Ghost:
    def __init__(self, x, y, speed, behavior, icon_path):
        self.x = x
        self.y = y
        self.speed = speed
        self.behavior = behavior
        self.icon = pygame.image.load(icon_path).convert_alpha()
        self.direction = Direction(0, 0)
        self.status = 0

    def move(self, pacman, maze):
        self.status += self.speed
        if self.behavior == 'x_first':
            self.move_x_first(pacman, maze)
        elif self.behavior == 'y_first':
            self.move_y_first(pacman, maze)
        elif self.behavior == 'bfs':
            self.move_bfs(pacman, maze)
        elif self.behavior == 'bfs_radius':
            self.move_radius(pacman, maze)

    def get_best_direction(self, maze, directions, bfs):
        directions = list(filter(lambda pos_direction: self.check_direction(maze, pos_direction), directions))
        if len(directions) > 0:
            best_direction = directions[0]
            for direction in directions:
                if bfs[self.x + direction.x][self.y + direction.y] < \
                        bfs[self.x + best_direction.x][self.y + best_direction.y]:
                    best_direction = direction
            best_final_directions = []
            for direction in directions:
                if bfs[self.x + direction.x][self.y + direction.y] == \
                        bfs[self.x + best_direction.x][self.y + best_direction.y]:
                    best_final_directions.append(direction)
            return random.choice(best_final_directions)
        return None

    def move_x_first(self, pacman, maze):
        if self.status >= 1:
            if self.check_direction(maze, self.direction):
                self.x += self.direction.x
                self.y += self.direction.y
            self.status = 0
            wanted_direction = [Direction(1, 0), Direction(-1, 0)]
            bfs = bfs_search(maze, [(pacman.x, pacman.y)])
            best_direction = self.get_best_direction(maze, wanted_direction, bfs)
            if best_direction is not None and bfs[self.x + best_direction.x][self.y + best_direction.y] < bfs[self.x][
                self.y]:
                self.direction = best_direction
                return
            possible_directions = [Direction(1, 0), Direction(-1, 0), Direction(0, 1), Direction(0, -1)]

            best_direction = self.get_best_direction(maze, possible_directions, bfs)
            if best_direction is not None:
                self.direction = best_direction

    def move_y_first(self, pacman, maze):
        if self.status >= 1:
            if self.check_direction(maze, self.direction):
                self.x += self.direction.x
                self.y += self.direction.y
            self.status = 0
            wanted_directions = [Direction(0, 1), Direction(0, -1)]
            bfs = bfs_search(maze, [(pacman.x, pacman.y)])
            best_direction = self.get_best_direction(maze, wanted_directions, bfs)
            if best_direction is not None and bfs[self.x + best_direction.x][self.y + best_direction.y] < bfs[self.x][
                self.y]:
                self.direction = best_direction
                return
            possible_directions = [Direction(1, 0), Direction(-1, 0), Direction(0, 1), Direction(0, -1)]

            best_direction = self.get_best_direction(maze, possible_directions, bfs)
            if best_direction is not None:
                self.direction = best_direction

    def move_bfs(self, pacman, maze):
        if self.status >= 1:
            if self.check_direction(maze, self.direction):
                self.x += self.direction.x
                self.y += self.direction.y
            self.status = 0
            bfs = bfs_search(maze, [(pacman.x, pacman.y)])
            possible_directions = [Direction(1, 0), Direction(-1, 0), Direction(0, 1), Direction(0, -1)]
            best_direction = self.get_best_direction(maze, possible_directions, bfs)
            if best_direction is not None:
                self.direction = best_direction

    def move_radius(self, pacman, maze):
        width, height = len(maze[0]), len(maze)
        radius = min(width, height) // 4
        if self.status >= 1:
            if self.check_direction(maze, self.direction):
                self.x += self.direction.x
                self.y += self.direction.y
            self.status = 0
            bfs = bfs_search(maze, [(pacman.x, pacman.y)])
            if abs(self.x - pacman.x) <= radius and abs(self.y - pacman.y) <= radius:
                possible_directions = [Direction(1, 0), Direction(-1, 0), Direction(0, 1), Direction(0, -1)]
                best_direction = self.get_best_direction(maze, possible_directions, bfs)
                if best_direction is not None:
                    self.direction = best_direction
            else:
                position = None
                if pacman.x - radius >= 0:
                    position = (pacman.x - radius, pacman.y)
                elif pacman.y - radius >= 0:
                    position = (pacman.x, pacman.y - radius)
                elif pacman.x + radius < height:
                    position = (pacman.x + radius, pacman.y)
                elif pacman.y + radius < width:
                    position = (pacman.x, pacman.y + radius)
                if position is not None:
                    new_bfs = bfs_search(maze, [position])
                    possible_directions = [Direction(1, 0), Direction(-1, 0), Direction(0, 1), Direction(0, -1)]
                    best_direction = self.get_best_direction(maze, possible_directions, new_bfs)
                    if best_direction is not None:
                        self.direction = best_direction

    def check_direction(self, maze, cur_direction):
        if maze[self.x + cur_direction.x][self.y + cur_direction.y] != '#':
            return True
        return False

    def draw(self, maze, screen):
        if self.check_direction(maze, self.direction):
            screen.blit(self.icon, (int((self.y + self.direction.y * self.status) * CELL_SIZE),
                                    int((self.x + self.direction.x * self.status) * CELL_SIZE)))
        else:
            screen.blit(self.icon, (self.y * CELL_SIZE, self.x * CELL_SIZE))
