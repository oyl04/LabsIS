import random
from math import ceil

import pygame

from search_algorithms.bfs_search import bfs_search
from settings import PACMAN_ICON, CELL_SIZE


class Direction:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Pacman:
    def __init__(self, x, y, speed, behavior):
        self.x = x
        self.y = y
        self.speed = speed
        self.icon = pygame.image.load(PACMAN_ICON).convert_alpha()
        self.rect = self.icon.get_rect()
        self.direction = Direction(0, 0)
        self.status = 0
        self.behavior = behavior

    def move(self, maze, last_pressed, ghosts):
        if maze.food_positions.__contains__((self.x, self.y)):
            maze.food_positions.remove((self.x, self.y))
        maze_table = maze.maze
        maze_table[self.x][self.y] = ' '
        self.status += self.speed
        if self.status >= 1:
            self.status = 0
            if maze_table[self.x + self.direction.x][self.y + self.direction.y] != '#':
                self.x += self.direction.x
                self.y += self.direction.y
            self.change_direction(maze, last_pressed, ghosts)

    def change_direction(self, maze, last_pressed, ghosts):
        if self.behavior == 'play':
            self.direction = last_pressed
        elif self.behavior == 'auto':
            maze_table = maze.maze
            width, height = len(maze_table[0]), len(maze_table)
            radius = 2
            ghost_positions = [(g.x, g.y) for g in ghosts]
            bfs = bfs_search(maze_table, ghost_positions)
            if bfs[self.x][self.y] <= radius:
                Directions = [Direction(1, 0), Direction(-1, 0), Direction(0, 1), Direction(0, -1)]
                Directions = list(filter(lambda direction: self.check_direction(maze_table, direction), Directions))
                if len(Directions) > 0:
                    best_direction = Directions[0]
                    for direction in Directions:
                        if bfs[self.x + direction.x][self.y + direction.y] > bfs[self.x + best_direction.x][
                            self.y + best_direction.y]:
                            best_direction = direction
                    best_directions = []
                    for direction in Directions:
                        if bfs[self.x + direction.x][self.y + direction.y] == \
                                bfs[self.x + best_direction.x][self.y + best_direction.y] or bfs[self.x + direction.x][
                            self.y + direction.y] > radius:
                            best_directions.append(direction)
                    self.direction = random.choice(best_directions)
            else:
                directions = [Direction(1, 0), Direction(-1, 0), Direction(0, 1), Direction(0, -1)]
                positions_food = [(x, y) for x, y in maze.food_positions]
                bfs_food = bfs_search(maze_table, positions_food)
                best_direction = self.get_best_direction(maze_table, directions, bfs_food)
                if best_direction is not None:
                    self.direction = best_direction

    def draw(self, maze, screen):
        if maze[self.x + self.direction.x][self.y + self.direction.y] != '#':
            screen.blit(self.icon, (int((self.y + self.direction.y * self.status) * CELL_SIZE),
                                    int((self.x + self.direction.x * self.status) * CELL_SIZE)))
        else:
            screen.blit(self.icon, (self.y * CELL_SIZE, self.x * CELL_SIZE))

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

    def check_direction(self, maze, cur_direction):
        if maze[self.x + cur_direction.x][self.y + cur_direction.y] != '#':
            return True
        return False
