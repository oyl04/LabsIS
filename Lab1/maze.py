import random
import pygame

from search_algorithms.bfs_search import check_can_block
from settings import CELL_SIZE, FOOD_ICON


class Maze:
    def __init__(self, width, height, level):
        self.width = width
        self.height = height
        self.level = level
        self.maze = self.generate_maze()

        # Завантаження іконки їжі
        self.food_icon = pygame.image.load(FOOD_ICON).convert_alpha()
        self.food_positions = self.generate_food()

    def generate_maze(self):
        maze = [['#'] * self.width for _ in range(self.height)]
        print(len(maze), len(maze[0]))
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                maze[i][j] = ' '
        prob = 0.1 + self.level * 0.05
        for i in range(2, self.height - 2):
            for j in range(2, self.width - 2):
                if random.random() < prob:
                    if check_can_block(maze, (i, j)) is True:
                        maze[i][j] = '#'
        return maze

    def generate_food(self):
        # Генерація їжі на порожніх місцях лабіринту
        food_positions = set()
        prob_food = 0.1 + self.level * 0.1
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] == ' ' and random.random() < prob_food:
                    self.maze[i][j] = 'f'
                if self.maze[i][j] == 'f':
                    food_positions.add((i, j))
        return food_positions

    def draw(self, screen):
        for x in range(self.height):
            for y in range(self.width):
                if self.maze[x][y] == 'f':
                    screen.blit(self.food_icon, (y * CELL_SIZE, x * CELL_SIZE))
                elif self.maze[x][y] == '#':
                    pygame.draw.rect(screen, (0, 0, 0), (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif self.maze[x][y] == ' ':
                    pygame.draw.rect(screen, (255, 255, 255), (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
