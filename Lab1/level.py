from maze import Maze
from settings import GHOST_SPEED, PACMAN_SPEED, WIDTH, HEIGHT, CELL_SIZE


class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.maze = Maze(int(WIDTH / CELL_SIZE), int(HEIGHT / CELL_SIZE),
                         self.level_num)  # Maze(WIDTH/CELL_SIZE, HEIGHT/CELL_SIZE, self.level_num)
        self.pacman_speed = PACMAN_SPEED
        self.ghost_speed = GHOST_SPEED + (self.level_num - 1) * 0.05
        self.ghosts = self.generate_ghosts()
        self.pacman = self.generate_pacman()

    def generate_ghosts(self):
        ghosts = [
            {'x': 1, 'y': 1, 'behavior': 'x_first', 'icon': 'assets/ghost1.png'},
            {'x': 1, 'y': self.maze.width - 2, 'behavior': 'y_first', 'icon': 'assets/ghost2.png'},
            {'x': self.maze.height - 2, 'y': 1, 'behavior': 'bfs', 'icon': 'assets/ghost3.png'},
            {'x': self.maze.height - 2, 'y': self.maze.width - 2, 'behavior': 'bfs_radius', 'icon': 'assets/ghost4.png'}
        ]
        return ghosts

    def generate_pacman(self):
        position = self.get_pacman_position()
        return {'x': position[0], 'y': position[1], 'speed': self.pacman_speed, 'icon': 'assets/pacman.png'}

    def is_food_collected(self):
        return len(self.maze.food_positions) == 0

    def next_level(self):
        self.level_num += 1
        self.maze = Maze(int(WIDTH / CELL_SIZE), int(HEIGHT / CELL_SIZE), self.level_num)
        self.ghosts = self.generate_ghosts()
        self.pacman = self.generate_pacman()

    def get_pacman_position(self):
        positions = []
        best_dist = -1e9
        best_position = None
        for i in range(len(self.maze.maze)):
            for j in range(len(self.maze.maze[i])):
                if self.maze.maze[i][j] == ' ':
                    if best_position is None:
                        best_position = (i, j)
                    cur_dist = 1e9
                    for ghost in self.ghosts:
                        dist = abs(ghost['x'] - i) + abs(ghost['y'] - j)
                        if dist < cur_dist:
                            cur_dist = dist
                    if cur_dist > best_dist:
                        best_dist = cur_dist
                        best_position = (i, j)
        return best_position
