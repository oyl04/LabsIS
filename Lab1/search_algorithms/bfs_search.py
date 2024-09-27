from collections import deque

CONST_INF = 1e9


def bfs_search(maze, start_positions):
    width, height = len(maze[0]), len(maze)
    dist = [[CONST_INF] * width for _ in range(height)]

    queue = deque()
    for (x, y) in start_positions:
        dist[x][y] = 0
        queue.append((x, y))

    while len(queue) > 0:
        x, y = queue.popleft()

        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nx = x + dx
            ny = y + dy

            if not (0 <= nx < height and 0 <= ny < width):
                continue
            if maze[nx][ny] == '#':
                continue
            if dist[nx][ny] != CONST_INF:
                continue
            dist[nx][ny] = dist[x][y] + 1
            queue.append((nx, ny))

    return dist


def check_can_block(maze, position):
    width, height = len(maze[0]), len(maze)
    current_maze = [[maze[x][y] for y in range(width)] for x in range(height)]
    current_maze[position[0]][position[1]] = '#'
    bfs = bfs_search(current_maze, [(1, 1)])

    for x in range(height):
        for y in range(width):
            if current_maze[x][y] != '#' and bfs[x][y] == CONST_INF:
                return False
    return True
